# server.py
import argparse
import os
import threading

import litserve as ls
from cache import PrefixCache
from fastapi import HTTPException
from kev.api import SystemOneRequest, output_tokens, to_answers, to_record
from kev.checkpoint import load, resolve_run
from utils import sync_device

DEFAULT_RUN = os.environ.get("KEV_RUN", "jaredpalmer/kev-0.8b")
# Per-branch cap mirrors Jev's, bounded by the base model's window.
MAX_STATE = MAX_BRANCH = 8192


class KevSystemOneAPI(ls.LitAPI):
    """Typed, calibrated decisions from a Kev checkpoint.

    Batching stays off. LitServe batches by stacking independent
    requests into one forward pass, but Kev already packs every question
    of a request into a single block-causal sequence and reuses a cached
    state prefix across requests. Stacking two users' states would break
    that prefix key and force ragged padding for no gain, so each
    request gets its own pass.
    """

    def __init__(self, run: str = DEFAULT_RUN, **kwargs):
        super().__init__(**kwargs)
        self.run = run

    def setup(self, device):
        """Load the checkpoint and this worker's serving state."""
        self.device = device
        if device.startswith("mps"):
            # Upstream's measured serving default on Apple GPUs.
            os.environ.setdefault("KEV_ATTN", "sdpa")

        self.tok, self.model = load(resolve_run(self.run), device)
        self.lock = threading.Lock()
        self.cache = PrefixCache()
        print(f"serving {self.run} on {device}")

    def decode_request(self, request: SystemOneRequest, context: dict):
        """Turn the request into a Kev record, keeping the question metadata.

        Annotating Kev's own pydantic model lets FastAPI validate the
        body exactly as upstream does, so a malformed request gets the
        same 422 here as there.
        """
        record, meta = to_record(request)
        context.update({"model": request.model, "meta": meta})
        return record

    def predict(self, record, context: dict):
        """Score every question in one prefill pass, with no token decoding."""
        try:
            enc = self.model.encode(
                self.tok, record, max_state=MAX_STATE, max_branch=MAX_BRANCH
            )
        except ValueError as e:  # state or a branch exceeds the window
            raise HTTPException(422, str(e)) from e

        with self.lock:
            probs, _ = self.cache.probs(self.model, enc)
            sync_device(self.device)

        context["input_tokens"] = len(enc["ids"])
        # Kev returns a tensor per question; to_answers wants plain floats.
        return [p.tolist() for p in probs]

    def encode_response(self, probs, context: dict) -> dict:
        """Build the documented response: model, answers, usage.

        Nothing else.
        """
        answers = to_answers(probs, context["meta"])
        return {
            "model": context["model"],
            "answers": answers,
            "usage": {
                "input_tokens": context["input_tokens"],
                "output_tokens": output_tokens(self.tok, answers),
            },
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Serve a Kev decision model over LitServe."
    )
    parser.add_argument(
        "--run", default=DEFAULT_RUN, help="Hub id or local run directory"
    )
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    api = KevSystemOneAPI(run=args.run, api_path="/v1/systemone")
    server = ls.LitServer(api, accelerator="auto")

    server.run(port=args.port)
