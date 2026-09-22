"""Measure the two things this server does to avoid redundant prefill.

Both numbers are ratios on purpose. Absolute latency depends entirely on the
box -- a shared CPU CI runner and an M-series Mac are orders of magnitude
apart -- but the ratio between two requests measured back to back on the same
box is stable enough to be worth asserting on.

  prefix cache     Kev reads the state before it reads any question, so a
                   repeated state can skip straight to its branches. Needs a
                   state above KEV_PREFIX_MIN_TOKENS, hence the long thread.

  packed requests  Asking N questions in one request reads the state once.
                   Asking them separately reads it N times.

Both are measured on the long thread, because both gains come from not
re-reading the state. On a short state there is nothing to amortize and packing
actually loses: the four-question triage example below runs about 0.9x, since
one long block-causal sequence costs more than four tiny independent ones.
"""

import argparse
import os
import platform
import statistics
import time

import httpx
import torch
from queries import CACHE_QUESTIONS, EXAMPLES, long_thread

URL = "http://127.0.0.1:8000/v1/systemone"
REPS = 3
# Deliberately loose. The point is to catch the optimization silently breaking,
# not to police a few percent of drift on a noisy runner.
MIN_SPEEDUP = 1.3


def system_info() -> list[tuple[str, str]]:
    """The box the numbers came from, so a pasted table stays interpretable.

    The client cannot ask the server what it loaded -- there is no info
    route, and adding one would widen an API whose whole point is that
    it is exactly TypeSafe's. Everything here is therefore read locally,
    which is accurate because the server runs on the same host in both
    the CI job and the README's setup. ``server.log`` has the
    authoritative device line.
    """
    if torch.cuda.is_available():
        device = f"cuda, {torch.cuda.get_device_name(0)}"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    try:
        memory = os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") / 1e9
        host = f"{platform.system()} {platform.machine()}, {os.cpu_count()} vCPU, {memory:.1f} GB"
    except (ValueError, OSError):  # SC_PHYS_PAGES is not portable
        host = f"{platform.system()} {platform.machine()}, {os.cpu_count()} vCPU"

    return [
        ("host", host),
        (
            "runtime",
            f"python {platform.python_version()}, torch {torch.__version__}, "
            f"{torch.get_num_threads()} threads",
        ),
        ("device", f"{device} (auto-selected; the server shares this host)"),
        ("run", os.environ.get("KEV_RUN", "jaredpalmer/kev-0.8b")),
    ]


def timed(client: httpx.Client, state, questions: dict) -> float:
    """Round-trip one request, in milliseconds."""
    start = time.perf_counter()
    response = client.post(
        URL, json={"state": state, "model": "kev-latest", "questions": questions}
    )
    response.raise_for_status()
    return (time.perf_counter() - start) * 1000


def prefix_cache(client: httpx.Client) -> tuple[float, float]:
    """Time the same request shape against a cold state and a cached one."""
    questions = CACHE_QUESTIONS[0]

    # Every state is new, so each of these misses. Distinct ids keep the states
    # the same length while making each one a different cache key.
    cold = [timed(client, long_thread(f"800{i}"), questions) for i in range(REPS)]

    # Prime one state, then repeat it: same tokens, same branches, now cached.
    warm_state = long_thread("9001")
    timed(client, warm_state, questions)
    warm = [timed(client, warm_state, questions) for _ in range(REPS)]

    return statistics.median(cold), statistics.median(warm)


def packed_vs_separate(client: httpx.Client) -> tuple[float, float]:
    """Time one request carrying every question against one request per
    question.

    Every state here is fresh, so neither side gets any help from the
    prefix cache and the comparison is purely one state read against N
    of them. That is the cost an N-question workload pays when the
    questions arrive as independent calls -- a cold cache, or separate
    workers.
    """
    questions = {
        name: spec for group in CACHE_QUESTIONS for name, spec in group.items()
    }

    separate = [
        sum(
            timed(client, long_thread(f"60{rep}{i}"), {name: spec})
            for i, (name, spec) in enumerate(questions.items())
        )
        for rep in range(REPS)
    ]
    packed = [timed(client, long_thread(f"61{rep}0"), questions) for rep in range(REPS)]

    return statistics.median(separate), statistics.median(packed)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ci",
        action="store_true",
        help=f"exit non-zero if a speedup drops below {MIN_SPEEDUP}x",
    )
    args = parser.parse_args()

    with httpx.Client(timeout=300) as client:
        # First request of the process pays for lazily initialised kernels.
        timed(client, EXAMPLES[0]["state"], CACHE_QUESTIONS[0])

        cold, warm = prefix_cache(client)
        separate, packed = packed_vs_separate(client)

    print("\nsystem")
    for key, value in system_info():
        print(f"  {key:<8} {value}")

    # Questions per second, not requests per second: the packed comparison moves
    # the same questions either way, so counting requests would score the packed
    # side as slower for doing the identical work in fewer calls.
    rows = [
        ("prefix cache", "uncached", cold, "cached", warm, len(CACHE_QUESTIONS[0])),
        (
            "packed request",
            "separate",
            separate,
            "packed",
            packed,
            len(CACHE_QUESTIONS),
        ),
    ]

    def line(
        label: str, name: str, elapsed: float, questions: int, tail: str = ""
    ) -> str:
        rate = questions / (elapsed / 1000)
        return (
            f"{label:<16}{name:<10}{elapsed:>8.0f}ms{rate:>9.2f} q/s{tail:>10}".rstrip()
        )

    print()
    failures = []
    for label, slow_name, slow, fast_name, fast, questions in rows:
        speedup = slow / fast
        # Label on the first line of the pair, speedup on the second.
        print(line(label, slow_name, slow, questions))
        print(line("", fast_name, fast, questions, f"{speedup:.2f}x"))
        if speedup < MIN_SPEEDUP:
            failures.append(f"{label}: {speedup:.2f}x below {MIN_SPEEDUP}x")

    print(
        f"\nmedian of {REPS} runs. q/s counts questions answered, since the packed\n"
        "comparison moves the same questions either way. Ratios, not absolute\n"
        "times, are what carries across machines."
    )

    if args.ci and failures:
        raise SystemExit("benchmark regression -- " + "; ".join(failures))


if __name__ == "__main__":
    main()
