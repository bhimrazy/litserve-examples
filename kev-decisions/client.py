import httpx

URL = "http://127.0.0.1:8000/v1/systemone"

STATE = (
    "Subject: charged twice for my order\n\n"
    "Hi - I placed order #4417 last Tuesday and my card shows two charges for $89.99. "
    "I've emailed twice with no reply and my account is now overdrawn. "
    "I need this refunded today or I'm disputing it with my bank."
)

QUESTIONS = {
    # noul -> binary; the answer is p(true)
    "billing": {
        "type": "noul",
        "instructions": "Is this ticket about a billing problem?",
    },
    # choice -> one option, plus a probability per option name
    "tone": {
        "type": "choice",
        "instructions": "What is the customer's tone?",
        "criteria": {"calm": None, "frustrated": None, "angry": None},
    },
    # score -> expected level over ordered criteria
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this ticket?",
        "criteria": ["can wait", "this week", "today"],
    },
}

response = httpx.post(
    URL,
    json={"state": STATE, "model": "kev-latest", "questions": QUESTIONS},
    timeout=120,
)
response.raise_for_status()
result = response.json()

for name, answer in result["answers"].items():
    print(f"{name}: {answer}")
print(f"\nusage: {result['usage']}")
