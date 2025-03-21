from pathlib import Path

import hydra
import numpy as np
import torch
from omegaconf import OmegaConf
from torch.utils.data import DataLoader, TensorDataset
from tqdm.rich import tqdm

from cpgpt.data.components.cpgpt_dataset import CpGPTDataset, cpgpt_data_collate
from cpgpt.data.components.dna_llm_embedder import DNALLMEmbedder
from cpgpt.log.utils import get_class_logger
from cpgpt.model.cpgpt_module import CpGPTLitModule

from .utils import SaveOutput, patch_attention


class CpGPTInferencer:
    """A class for performing inference with CpGPT models.

    This class provides functionality to load CpGPT models, process input data,
    and perform inference on methylation data. It handles device management,
    model loading, and data processing for efficient inference.

    Attributes:
        logger: A logger instance for the class.
        device: The device (CPU or CUDA) to be used for computations.

    """

    def __init__(self) -> None:
        """Initialize the CpGPTInferencer.

        Sets up logging and determines the appropriate device (CPU/CUDA) for computations.
        """
        self.logger = get_class_logger(self.__class__)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}.")
        if self.device == "cpu":
            self.logger.warning("Using CPU for inference. This may be slow.")

    def load_cpgpt_config(
        self,
        config_path: str,
    ) -> OmegaConf:
        """Load a yaml file containing the configuration for a CpGPT model.

        Args:
            config_path (str): Path to the yaml configuration file.

        Returns:
            OmegaConf: An omega dictionary with the model configuration.

        """
        config = OmegaConf.load(config_path)
        self.logger.info("Loaded CpGPT model config.")

        return config

    def load_cpgpt_model(
        self,
        config: OmegaConf,
        model_ckpt_path: str | None = None,
        strict_load: bool = True,
    ) -> CpGPTLitModule:
        """Load a CpGPT model from a checkpoint file and return the model.

        If no checkpoint path is provided, the model will be returned
        with randomly initialized weights.

        Args:
            config (OmegaConf): Hydra config containing the model definition.
            model_ckpt_path (str, optional): Path to the checkpoint file. If not provided,
                random initialization is used.
            strict_load (bool, optional): If True, requires exact key matching
                when loading the checkpoint.

        Returns:
            CpGPTLitModule: The instantiated (and optionally checkpoint-loaded) model.

        """
        # Instantiate the model
        model: CpGPTLitModule = hydra.utils.instantiate(config.model)
        self.logger.info("Instantiated CpGPT model from config.")

        # Load to device
        model.to(self.device)
        self.logger.info(f"Using device: {self.device}.")

        # Load checkpoint if a valid path is provided
        if model_ckpt_path is not None:
            ckpt_path_obj = Path(model_ckpt_path)
            if not ckpt_path_obj.exists():
                msg = f"Checkpoint file not found: {model_ckpt_path}"
                self.logger.error(msg)
                raise FileNotFoundError(msg)

            self.logger.info(f"Loading checkpoint from: {model_ckpt_path}")
            checkpoint = torch.load(ckpt_path_obj, map_location=self.device, weights_only=False)
            state_dict = checkpoint["state_dict"]
            cleaned_state_dict = {
                k.replace("net._orig_mod.", "net."): v for k, v in state_dict.items()
            }
            model.load_state_dict(cleaned_state_dict, strict=strict_load)
            self.logger.info("Checkpoint loaded into the model.")
        else:
            self.logger.info("No checkpoint path provided; using random initialization.")

        return model

    @torch.inference_mode()
    @torch.autocast(device_type="cuda", dtype=torch.float16)
    def get_attention_weights(
        self,
        model: CpGPTLitModule,
        sample: tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        layer_index: int = -1,
        aggregate_heads: str = "mean",
        return_type: str = "torch",
    ) -> torch.Tensor | np.ndarray:
        """Extract attention weights from a specific layer of the model.

        Args:
            model (CpGPTLitModule): The loaded CpGPT model
            sample (Tuple[torch.Tensor, ...]): Input sample containing:
                - methylation data
                - DNA embeddings
                - chromosome indices
                - positions
            layer_index (int, optional): Index of attention layer. Defaults to -1 (last layer)
            aggregate_heads (str, optional): How to aggregate attention heads:
                - "mean": Average across heads
                - "max": Take maximum attention
                - "none": Keep separate heads
                Defaults to "mean"
            return_type (str, optional): Output format ("torch" or "numpy"). Defaults to "torch"

        Returns:
            Union[torch.Tensor, np.ndarray]: Attention weights tensor/array

        Raises:
            ValueError: If aggregate_heads or return_type are invalid

        """
        self.logger.info(f"Getting attention weights for layer index: {layer_index}.")
        model = model.to(self.device)
        model.eval()

        save_output = SaveOutput()
        target_layer = model.net.transformer_encoder.layers[layer_index].self_attn
        patch_attention(target_layer)
        hook_handle = target_layer.register_forward_hook(save_output)

        # Prepare input
        input_tensors = self._process_batch(
            sample,
            model.hparams.training["binarize_input"],
            model,
        )
        input_tensors = {k: v.unsqueeze(0) for k, v in input_tensors.items()}

        shapes_str = ", ".join([f"{k}={v.shape}" for k, v in input_tensors.items()])
        self.logger.debug(f"Input shapes: {shapes_str}.")

        self.logger.debug("Running model inference.")
        _ = model.net.encode_sample(**input_tensors)

        hook_handle.remove()

        # Process attention weights
        attention_weights = torch.nan_to_num(save_output.outputs[0][0], nan=0)
        if aggregate_heads == "mean":
            attention_weights = attention_weights.mean(dim=0)
        elif aggregate_heads == "max":
            attention_weights = attention_weights.max(dim=0)[0]
        elif aggregate_heads != "none":
            msg = "aggregate_heads must be either 'mean', 'max' or 'none'"
            raise ValueError(msg)

        save_output.clear()

        self.logger.info(f"Attention weights shape: {attention_weights.shape}.")

        if return_type == "numpy":
            attention_weights = attention_weights.detach().cpu().numpy()
        elif return_type == "torch":
            pass
        else:
            msg = "return_type must be either 'torch' or 'numpy'"
            raise ValueError(msg)

        return attention_weights

    @torch.inference_mode()
    @torch.autocast(device_type="cuda", dtype=torch.float16)
    def embed_sample(
        self,
        model: CpGPTLitModule,
        data: CpGPTDataset,
        batch_size: int = 1,
        num_workers: int = 4,
        return_type: str = "torch",
    ) -> torch.Tensor | np.ndarray:
        """Generate sample embeddings for the entire dataset.

        Args:
            model (CpGPTLitModule): The CpGPT Lightning model.
            data (CpGPTDataset): The dataset to generate embeddings for.
            batch_size (int): Batch size for processing. Default is 1.
            num_workers (int): Number of workers for data loading. Default is 4.
            return_type (str): Type of returned array. Options are "torch" or "numpy".
                Default is "torch".

        Returns:
            Union[torch.Tensor, np.ndarray]: Sample embeddings for the entire dataset.

        Raises:
            ValueError: If an invalid return_type is provided.

        """
        self.logger.info("Generating sample embeddings for the entire dataset.")
        model = model.to(self.device)
        model.eval()

        if return_type not in ["torch", "numpy"]:
            msg = "return_type must be either 'torch' or 'numpy'"
            raise ValueError(msg)

        dataloader = DataLoader(
            data,
            batch_size=batch_size,
            shuffle=False,
            collate_fn=cpgpt_data_collate,
            num_workers=num_workers,
        )

        all_sample_embedding = []
        for batch in tqdm(dataloader, desc="Generating embeddings"):
            input_tensors = self._process_batch(
                batch,
                model.hparams.training["binarize_input"],
                model,
            )
            sample_embedding = model.net.encode_sample(**input_tensors)
            if return_type == "numpy":
                sample_embedding = sample_embedding.detach().cpu().numpy()
            all_sample_embedding.append(sample_embedding)

        self.logger.info("Embeddings generated successfully.")
        if return_type == "torch":
            return torch.cat(all_sample_embedding, dim=0)
        return np.concatenate(all_sample_embedding, axis=0)

    @torch.inference_mode()
    @torch.autocast(device_type="cuda", dtype=torch.float16)
    def reconstruct_betas(
        self,
        model: CpGPTLitModule,
        sample_embedding: torch.Tensor,
        genomic_locations: list[str],
        embedder: DNALLMEmbedder,
        dna_llm: str,
        dna_context_len: int,
        species: str = "homo_sapiens",
        batch_size: int = 4,
        return_type: str = "torch",
    ) -> tuple[torch.Tensor, torch.Tensor] | tuple[np.ndarray, np.ndarray]:
        """Reconstruct beta values from sample embeddings.

        Args:
            model (CpGPTLitModule): The loaded CpGPT model
            sample_embedding (torch.Tensor): Sample embedding tensor
            genomic_locations (List[str]): List of genomic locations
            embedder (DNALLMEmbedder): DNA embedder instance
            dna_llm (str): Name of DNA language model
            dna_context_len (int): Context length for DNA sequences
            species (str, optional): Species name. Defaults to "homo_sapiens"
            batch_size (int, optional): Batch size for processing. Defaults to 4
            return_type (str, optional): Output format ("torch" or "numpy"). Defaults to "torch"

        Returns:
            Union[Tuple[torch.Tensor, torch.Tensor], Tuple[np.ndarray, np.ndarray]]:
                Tuple containing:
                - reconstructed_betas: Reconstructed methylation values
                - uncertainties: Uncertainty estimates for each value

        Note:
            Uses batched processing for memory efficiency

        """
        if return_type not in ["torch", "numpy"]:
            msg = "return_type must be either 'torch' or 'numpy'"
            raise ValueError(msg)

        self.logger.info(
            f"Reconstructing beta values for {len(genomic_locations)} genomic locations.",
        )
        model = model.to(self.device)
        model.eval()

        sample_embedding = sample_embedding.to(self.device)

        dna_embeddings = self._get_dna_embeddings(
            embedder,
            species,
            dna_llm,
            dna_context_len,
            genomic_locations,
        ).to(self.device)

        all_reconstructed_betas, all_uncertainties = [], []
        sequence_embeddings = model.net.encode_sequence(dna_embeddings)

        # Create a DataLoader for batching
        dataset = TensorDataset(sample_embedding)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        for batch in tqdm(dataloader, desc="Reconstructing from sample embeddings"):
            batch_sample_embedding = batch[0]  # Extract the tensor from the batch tuple
            batch_sequence_embeddings = sequence_embeddings.unsqueeze(0).repeat(
                batch_sample_embedding.size(0),
                1,
                1,
            )
            reconstructed_betas, uncertainties = model.net.query_methylation(
                batch_sample_embedding,
                batch_sequence_embeddings,
                m_or_beta="beta",
            )
            if return_type == "numpy":
                reconstructed_betas = reconstructed_betas.detach().cpu().numpy()
                uncertainties = uncertainties.detach().cpu().numpy()
            all_reconstructed_betas.append(reconstructed_betas)
            all_uncertainties.append(uncertainties)

        self.logger.info("Reconstruction completed.")
        if return_type == "torch":
            return torch.cat(all_reconstructed_betas, dim=0), torch.cat(all_uncertainties, dim=0)
        return np.concatenate(all_reconstructed_betas, axis=0), np.concatenate(
            all_uncertainties,
            axis=0,
        )

    @torch.inference_mode()
    @torch.autocast(device_type="cuda", dtype=torch.float16)
    def query_condition(
        self,
        model: CpGPTLitModule,
        sample_embedding: torch.Tensor,
        batch_size: int = 4,
        return_type: str = "torch",
    ) -> torch.Tensor | np.ndarray:
        """Predict using the task-specific decoder given sample embeddings.

        Args:
            model (CpGPTLitModule): The CpGPT Lightning model.
            sample_embedding (torch.Tensor): Pre-computed sample embeddings.
            batch_size (int): Batch size for processing. Default is 4.
            return_type (str): Type of returned array. Options are "torch" or "numpy".
                Default is "torch".

        Returns:
            Union[torch.Tensor, np.ndarray]: Predictions from the task-specific decoder.

        Raises:
            AttributeError: If the model does not have a task-specific decoder.
            ValueError: If neither sample_embedding nor data is provided, or if an invalid
                return_type is provided.

        """
        if return_type not in ["torch", "numpy"]:
            msg = "return_type must be either 'torch' or 'numpy'"
            raise ValueError(msg)

        self.logger.info("Predicting using the task-specific decoder.")
        model = model.to(self.device)
        model.eval()

        all_predictions = []
        sample_embedding = sample_embedding.to(self.device)

        # Create a DataLoader for batching
        dataset = TensorDataset(sample_embedding)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        for batch in tqdm(dataloader, desc="Predicting from sample embeddings"):
            batch_sample_embedding = batch[0]  # Extract the tensor from the batch tuple
            pred_conditions = model.net.query_condition(batch_sample_embedding)
            if return_type == "numpy":
                pred_conditions = pred_conditions.detach().cpu().numpy()
            all_predictions.append(pred_conditions)

        self.logger.info("Prediction completed.")
        if return_type == "torch":
            return torch.cat(all_predictions, dim=0)
        return np.concatenate(all_predictions, axis=0)

    def generate_sample_embedding(
        self,
        model: CpGPTLitModule,
        num_samples: int = 10,
        obsm: torch.Tensor | None = None,
        guidance_scale: float = 1.0,
        batch_size: int = 16,
        return_type: str = "torch",
    ) -> torch.Tensor | np.ndarray:
        """Generate sample embeddings using the diffusion model.

        Args:
            model (CpGPTLitModule): The loaded CpGPT model
            num_samples (int, optional): Number of samples to generate. Defaults to 10
            obsm (Optional[torch.Tensor], optional): Observation matrix for conditioning.
                Defaults to None
            guidance_scale (float, optional): Scale factor for classifier guidance.
                Defaults to 1.0
            batch_size (int, optional): Batch size for processing. Defaults to 16
            return_type (str, optional): Output format ("torch" or "numpy"). Defaults to "torch"

        Returns:
            Union[torch.Tensor, np.ndarray]: Generated sample embeddings

        Note:
            Uses classifier guidance when obsm is provided
            Processes samples in batches for memory efficiency

        """
        if return_type not in ["torch", "numpy"]:
            msg = "return_type must be either 'torch' or 'numpy'"
            raise ValueError(msg)

        self.logger.info("Generating realistic sample embeddings from pure noise.")
        model = model.to(self.device)
        model.eval()

        if obsm is not None and obsm.dim() != 1:
            msg = "The observation matrix (obsm) must be 1-dimensional."
            raise ValueError(msg)

        # Expand obsm to match the number of samples if obsm is not None
        if obsm is not None:
            obsm = obsm.unsqueeze(1).expand(num_samples, -1).to(self.device)

        # Initialize embeddings with Gaussian noise
        sample_embedding_t = torch.randn(num_samples, model.net.d_embedding, device=self.device)

        num_timesteps = model.hparams.training["diffusion_params"]["num_timesteps"]
        pbar = tqdm(
            reversed(range(num_timesteps)),
            desc="Generating sample embeddings",
            total=num_timesteps,
        )

        # Create a DataLoader for batching
        dataset = TensorDataset(sample_embedding_t)
        DataLoader(dataset, batch_size=batch_size, shuffle=False)

        all_sample_embeddings = []

        for t in pbar:
            timestep = torch.full((num_samples,), t, device=self.device, dtype=torch.long)
            for i in range(0, num_samples, batch_size):
                batch_indices = slice(i, min(i + batch_size, num_samples))
                batch_sample_embedding_t = sample_embedding_t[batch_indices]
                batch_timestep = timestep[batch_indices]

                # Predict noise given the current sample embedding and timestep
                with torch.inference_mode():
                    pred_noise = model.net.predict_noise(batch_sample_embedding_t, batch_timestep)

                # Classifier-based guidance
                if obsm is not None:
                    with torch.enable_grad():
                        batch_sample_embedding_t.requires_grad = True
                        pred_conditions = model.net.query_condition(batch_sample_embedding_t)
                        losses = model.calculate_losses(
                            pred_conditions=pred_conditions,
                            obsm=obsm[batch_indices],
                        )
                        losses["condition_loss"].backward()
                        grad = batch_sample_embedding_t.grad
                        batch_sample_embedding_t = batch_sample_embedding_t - guidance_scale * grad
                        batch_sample_embedding_t = batch_sample_embedding_t.detach()
                        pbar.set_postfix({"condition_loss": losses["condition_loss"].item()})

                # Compute the previous sample embedding
                sample_embedding_t[batch_indices] = model.p_sample(
                    batch_sample_embedding_t,
                    batch_timestep,
                    pred_noise,
                )

            if return_type == "numpy":
                all_sample_embeddings.append(sample_embedding_t.detach().cpu().numpy())

        self.logger.info("Sample embeddings generated successfully.")
        if return_type == "torch":
            return sample_embedding_t
        return np.concatenate(all_sample_embeddings, axis=0)

    @torch.inference_mode()
    def _process_batch(
        self,
        batch: dict,
        binarize_input: bool,
        model: CpGPTLitModule,
    ) -> dict[str, torch.Tensor]:
        """Process a batch of data for embedding generation.

        Args:
            batch (Dict): A dictionary containing methylation data ('meth'),
                DNA embeddings ('dna_embeddings'), chromosomes ('chroms'),
                positions ('positions'), and other information.
            binarize_input (bool): Whether to binarize the input data.
            model (CpGPTLitModule): The CpGPT Lightning model.

        Returns:
            Dict[str, torch.Tensor]: Dictionary containing the processed tensors moved to device

        """
        processed_dict = {
            "meth": batch["meth"],
            "sequence_embeddings": model.net.encode_sequence(
                batch["dna_embeddings"].to(self.device),
            ),
            "chroms": batch["chroms"],
            "positions": batch["positions"],
        }

        # Process methylation data
        processed_dict["mask_na"] = torch.isnan(processed_dict["meth"])
        processed_dict["meth"] = torch.nan_to_num(processed_dict["meth"], nan=0)
        if binarize_input:
            processed_dict["meth"] = torch.bernoulli(processed_dict["meth"])

        # Move everything to device
        return {k: v.to(self.device) for k, v in processed_dict.items()}

    def _get_dna_embeddings(
        self,
        embedder: DNALLMEmbedder,
        species: str,
        dna_llm: str,
        dna_context_len: int,
        genomic_locations: list[str],
    ) -> torch.Tensor:
        """Retrieve DNA embeddings for the given genomic locations.

        Args:
            embedder (DNALLMEmbedder): The dataset containing embedding information.
            species (str): The species for which to retrieve embeddings.
            dna_llm (str): The DNA LLM to use.
            dna_context_len (int): The DNA context length.
            genomic_locations (List[str]): List of genomic locations to retrieve embeddings for.

        Returns:
            torch.Tensor: Tensor containing DNA embeddings for the specified locations.

        Raises:
            ValueError: If the species or DNA LLM is not found in the embedder.

        """
        if species not in embedder.ensembl_metadata_dict:
            msg = f"Species {species} not found in the embedder."
            raise ValueError(msg)
        if dna_llm not in embedder.ensembl_metadata_dict[species]:
            msg = f"DNA LLM {dna_llm} not found in the embedder for species {species}."
            raise ValueError(msg)

        embeddings_file = (
            Path(embedder.dependencies_dir)
            / "dna_embeddings"
            / species
            / dna_llm
            / f"{dna_context_len}bp_dna_embeddings.mmap"
        )
        current_embeddings = embedder.ensembl_metadata_dict[species][dna_llm][dna_context_len]
        embedding_size = embedder.llm_embedding_size_dict[dna_llm]

        embeddings = np.memmap(
            embeddings_file,
            dtype="float32",
            mode="r",
            shape=(len(current_embeddings), embedding_size),
        )

        embedding_indices = [current_embeddings[location] for location in genomic_locations]
        return torch.tensor(embeddings[embedding_indices], dtype=torch.float32).to(self.device)
