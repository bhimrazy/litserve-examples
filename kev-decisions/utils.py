import os
import sys
from pathlib import Path

import torch

KEV_INSTALL_HINT = (
    "Could not import `kev`.\n\n"
    "Kev is not pip-installable today: its pyproject.toml declares no package-discovery\n"
    "config, so setuptools rejects the flat layout. Clone it and set KEV_HOME:\n\n"
    "    git clone https://github.com/jaredpalmer/kev\n"
    "    export KEV_HOME=$PWD/kev\n"
)


def ensure_kev_importable() -> None:
    """Add a local Kev checkout to ``sys.path``.

    Looks at ``$KEV_HOME``, then ``./kev`` and ``../kev``.

    Raises:
        SystemExit: If no checkout is found, with cloning instructions.
    """
    try:
        import kev.api  # noqa: F401

        return
    except ModuleNotFoundError:
        pass

    for path in (Path(p).expanduser() for p in (os.environ.get("KEV_HOME"), "./kev", "../kev") if p):
        if (path / "kev" / "api.py").is_file():
            sys.path.insert(0, str(path.resolve()))
            return

    raise SystemExit(KEV_INSTALL_HINT)


def sync_device(device: str) -> None:
    """Block until queued GPU work finishes, so timings are real.

    Args:
        device: The accelerator LitServe assigned, e.g. ``"mps"`` or ``"cuda:0"``.
    """
    if device.startswith("mps"):
        torch.mps.synchronize()
    elif device.startswith("cuda"):
        torch.cuda.synchronize()
