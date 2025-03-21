import torch
from torch import nn


class SaveOutput:
    """A class to save and manage outputs from a module.

    This class is designed to be used as a hook in PyTorch modules to capture and store their
    outputs.
    """

    def __init__(self) -> None:
        """Initialize an empty list to store outputs."""
        self.outputs = []

    def __call__(
        self,
        module: nn.Module,
        module_in: torch.Tensor,
        module_out: tuple[torch.Tensor, torch.Tensor],
    ) -> None:
        """Capture and store the output of a module.

        Args:
            module (nn.Module): The module being processed.
            module_in (torch.Tensor): The input to the module.
            module_out (tuple[torch.Tensor, torch.Tensor]): The output from the module.

        """
        self.outputs.append(module_out[1])

    def clear(self) -> None:
        """Clear all stored outputs."""
        self.outputs = []


def patch_attention(m: nn.Module) -> None:
    """Patch the forward method of an attention module to always return attention weights.

    Args:
        m (nn.Module): The attention module to be patched.

    Returns:
        None. The module is modified in-place.

    """
    forward_orig = m.forward

    def wrap(
        *args: list[torch.Tensor],
        **kwargs: dict[str, bool | float | None],
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Wrapper function for the original forward method.

        This wrapper ensures that attention weights are always computed and returned.

        Args:
            *args: Variable length list of tensors (query, key, value).
            **kwargs: Keyword arguments for the attention module.
                Supported keys include:
                - need_weights (bool): Whether to return attention weights
                - average_attn_weights (bool): Whether to average attention weights
                - key_padding_mask (Optional[Tensor]): Mask for padded elements
                - attn_mask (Optional[Tensor]): Mask to prevent attention to positions

        Returns:
            tuple[torch.Tensor, torch.Tensor]: A tuple containing:
                - output tensor of shape (batch_size, seq_len, hidden_size)
                - attention weights tensor of shape (batch_size, num_heads, seq_len, seq_len)

        """
        kwargs["need_weights"] = True
        kwargs["average_attn_weights"] = False
        return forward_orig(*args, **kwargs)

    m.forward = wrap
