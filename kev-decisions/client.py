import httpx
from queries import EXAMPLES

URL = "http://127.0.0.1:8000/v1/systemone"


def render(name: str, answer: dict) -> str:
    """One line per answer, showing the distribution rather than just the
    pick."""
    if answer["type"] == "noul":
        return f"  {name}: {answer['noul']:.2f}"
    if answer["type"] == "choice":
        odds = " ".join(f"{k} {v:.2f}" for k, v in answer["probabilities"].items())
        return f"  {name}: {answer['choice']} (confidence {answer['confidence']:.2f}) [{odds}]"
    legend = answer["legend"]
    odds = " ".join(f"{legend[k]} {v:.2f}" for k, v in answer["probabilities"].items())
    return f"  {name}: {answer['score']:.2f} (confidence {answer['confidence']:.2f}) [{odds}]"


def main() -> None:
    with httpx.Client(timeout=120) as client:
        for example in EXAMPLES:
            print(f"\n{example['name']}: {example['blurb']}")
            response = client.post(
                URL,
                json={
                    "state": example["state"],
                    "model": "kev-latest",
                    "questions": example["questions"],
                },
            )
            response.raise_for_status()
            result = response.json()

            for name, answer in result["answers"].items():
                print(render(name, answer))
            print(f"  usage: {result['usage']}")


if __name__ == "__main__":
    main()
