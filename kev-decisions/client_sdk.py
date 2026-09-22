"""The same requests through TypeSafe's SDK instead of raw HTTP.

The server speaks TypeSafe's /v1/systemone wire format, so the official
client works against it unchanged -- the only thing that differs from
talking to the hosted API is base_url. Answers come back as typed
objects grouped by kind, which is the reason to reach for the SDK over
httpx.
"""

from queries import EXAMPLES
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

BASE_URL = "http://127.0.0.1:8000"
TYPES = {"noul": Noul, "choice": Choice, "score": Score}


def as_questions(raw: dict) -> dict:
    """Turn the JSON question specs in queries.py into SDK question objects."""
    return {
        name: TYPES[spec["type"]](
            instructions=spec["instructions"], criteria=spec.get("criteria")
        )
        for name, spec in raw.items()
    }


def main() -> None:
    # api_key is required by the SDK but ignored by this server, which has no auth.
    client = TypeSafeClient(
        api_key="local", base_url=BASE_URL, model="kev-latest", timeout=120
    )

    for example in EXAMPLES:
        print(f"\n{example['name']}")
        response = client.system_one(
            state=example["state"], questions=as_questions(example["questions"])
        )

        # Grouped by kind, so each branch below gets a concrete type.
        for name, answer in response.nouls.items():
            print(f"  {name}: {answer.noul:.2f}")
        for name, answer in response.choices.items():
            print(f"  {name}: {answer.choice} (confidence {answer.confidence:.2f})")
        for name, answer in response.scores.items():
            print(f"  {name}: {answer.score:.2f} (confidence {answer.confidence:.2f})")
        print(
            f"  usage: input={response.usage.input_tokens} output={response.usage.output_tokens}"
        )


if __name__ == "__main__":
    main()
