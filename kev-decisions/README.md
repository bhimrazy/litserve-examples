<h1 align="center">Kev Decisions API</h1>

## 🎯 Overview

A typed-decision API that combines:

- 🚀 **LitServe** - High-performance API infrastructure
- 🔌 **System One Spec** - Drop-in compatible with TypeSafe's `/v1/systemone`
- ⚡ **Kev** - Calibrated decisions in one prefill pass, no token decoding

Most model APIs generate text and hope it parses. A *decision model* does the opposite: it
reads some unstructured state once and returns a probability distribution over the answers
you defined, in a single forward pass with no decoding at all.

[Kev](https://github.com/jaredpalmer/kev) is Jared Palmer's open-source (Apache-2.0)
reconstruction of [TypeSafe's Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev):
a LoRA adapter plus a small pointer head on a frozen Qwen base. This example serves it over
LitServe on the same `POST /v1/systemone` route Jev uses, so Jev clients work unchanged.

Ask three kinds of question:

| Type | Returns | Use for |
| --- | --- | --- |
| `noul` | `p(true)` | yes/no gates |
| `choice` | one option + a probability per option | routing, categorisation |
| `score` | expected level over ordered criteria | severity, urgency, quality |

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- `pip` (or [`uv`](https://docs.astral.sh/uv/))
- ~1.9 GB download on first run: Kev's adapter (~65 MB) plus the Qwen3.5-0.8B base

### Setup

```bash
# Clone repository
git clone https://github.com/bhimrazy/litserve-examples.git
cd litserve-examples/kev-decisions

# Install dependencies
pip install -r requirements.txt
```

> [!NOTE]
> Kev is not published to PyPI, so `requirements.txt` installs it from git at a pinned
> commit. Do not `pip install kev` — PyPI's `kev` is an unrelated key-value store ORM.

### Run

```bash
# Start server
python server.py

# In another terminal
python client.py
```

Pick a different checkpoint with `--run` or `KEV_RUN`:

```bash
python server.py --run jaredpalmer/kev-4b
```

## 📡 API

One endpoint, matching TypeSafe's [documented schema](https://docs.typesafe.ai/api) exactly:
`POST /v1/systemone` takes `state`, `model` and `questions`, and returns `model`, `answers`
and `usage`. There are no model-listing, health or batch routes — that is the whole surface.

```bash
curl -X POST http://127.0.0.1:8000/v1/systemone \
  -H 'content-type: application/json' \
  -d '{
    "state": "Shoes arrived late and in the wrong size.",
    "model": "kev-latest",
    "questions": {
      "escalate": {"type": "noul", "instructions": "Needs urgent human attention?"}
    }
  }'
```

### Using TypeSafe's SDK

The wire format is Jev's, so TypeSafe's own SDK (`pip install typesafe-sdk`) should work
against this server by pointing it at `http://127.0.0.1:8000`. Two caveats, both untested
here: the SDK's `base_url` override is not documented, and its examples pass `state` as a
dict (`{"document": "..."}`) while Kev's own examples pass a plain string. Verify before
relying on SDK compatibility. `client.py` uses `httpx` instead, so it needs no API key.

## 🧠 Choosing a model

| Model | Base | Notes |
| --- | --- | --- |
| `kev-0.8b` *(default)* | Qwen3.5-0.8B | Smallest of the current generation |
| `kev-4b` | Qwen3.5-4B | Upstream's recommended starting point |
| `kev-9b` | Qwen3.5-9B | Highest accuracy |

On Apple Silicon the previous-generation `kev-0.6b` is roughly 2.7x faster than `kev-0.8b`
(~123 ms vs ~329 ms on a 5-question request) because Qwen3.5's Gated DeltaNet layers have no
fast Apple kernels yet; an MLX backend is upstream's stated next step. The 4B and 9B models
fit a 32 GB Mac in bf16.

## ⚠️ Accuracy and calibration

Read this before pointing anything important at the default model.

`kev-0.8b` scores about **0.83 on held-out examples from its training sources but only
~0.65 on new sources**, and its probabilities are poorly calibrated out of domain. It suits
routing and triage close to its training distribution, or as a base to fine-tune on a few
hundred of your own labelled examples. It is not a reliable general zero-shot judge — use
`kev-4b` (~0.79 on new sources) when accuracy matters.

At the top end, `kev-9b` trails Jev by 3.5 accuracy points out of distribution (0.822 vs
0.857) with comparable calibration (4.0% vs 3.7% confident errors).

This is a fast-moving ecosystem: Jev launched on 15 September 2026 and Kev and a dozen other
reconstructions appeared within days. Treat upstream as young code.

## 🏗️ How it works

```
client.py  ->  POST /v1/systemone  ->  server.py (LitServe)
                                          |
                                          +-- utils.py  device sync
                                          +-- cache.py  LRU state-prefix cache
                                          +-- kev.api   request model, record, answers
```

`server.py` is a thin `LitAPI`: `decode_request` turns the request into a Kev record via
Kev's own pydantic model (so validation errors match upstream), `predict` runs one prefill
pass, and `encode_response` returns the three documented keys.

Two details worth knowing:

**The prefix cache.** Kev reads the state once, then answers each question from its own
branch, so everything up to the first question has activations independent of the questions.
`cache.py` keeps those prefixes in a small LRU, and a repeated state pays only for its
branches. The reuse is exact, not approximate. Tune with `KEV_PREFIX_CACHE` (entries, `0`
disables) and `KEV_PREFIX_MIN_TOKENS`. Upstream holds this in a module global; here it lives
on the `LitAPI` instance so each worker gets its own.

**Batching is off.** LitServe batches by stacking independent requests into one forward
pass, but Kev already packs every question of a request into a single block-causal sequence.
Stacking two users' states would break the prefix key and force ragged padding for no gain,
so each request gets its own pass.

## 🔗 Links

- [Kev](https://github.com/jaredpalmer/kev) · [checkpoints](https://huggingface.co/collections/jaredpalmer/kev)
- [TypeSafe's Jev announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev) · [API docs](https://docs.typesafe.ai/api)
- [LitServe docs](https://lightning.ai/docs/litserve)
