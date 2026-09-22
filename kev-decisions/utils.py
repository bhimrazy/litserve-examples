import torch


def sync_device(device: str) -> None:
    """Block until queued GPU work finishes, so timings are real.

    Args:
        device: The accelerator LitServe assigned, e.g. ``"mps"`` or ``"cuda:0"``.
    """
    if device.startswith("mps"):
        torch.mps.synchronize()
    elif device.startswith("cuda"):
        torch.cuda.synchronize()
