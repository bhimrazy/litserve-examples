"""Example requests shared by the clients and the benchmark.

The first four are adapted from Kev's own playground presets
(https://github.com/jaredpalmer/kev/blob/main/space/presets.py) so the answers
here can be compared against upstream's. Each one is chosen to show something
different: the three question types together, ordered scores, a structured
state, and the isolation guarantee.
"""

# Requests are plain JSON, exactly what /v1/systemone accepts. client_sdk.py
# converts them to the SDK's typed question objects.
EXAMPLES = [
    {
        "name": "Support triage",
        "blurb": "All three question types in one request, over a single reading of the ticket.",
        "state": (
            "Shoes arrived two weeks late and in the wrong size. "
            "Also I see two charges on my card. What are you going to do about this?"
        ),
        "questions": {
            "department": {
                "type": "choice",
                "instructions": "Which team should handle this?",
                "criteria": {
                    "returns": "Exchanges, refunds, wrong or damaged items",
                    "shipping": "Delivery status, delays, lost packages",
                    "billing": "Charges, invoices, payment problems",
                },
            },
            "requested_resolution": {
                "type": "choice",
                "instructions": "What does the customer want to happen?",
                "criteria": {
                    "exchange": "Swap the item for a different one",
                    "refund": "Money back",
                    "replacement": "The same item sent again",
                    "information": "Just an answer, no action needed",
                },
            },
            "escalate": {
                "type": "noul",
                "instructions": "Does this message require urgent human attention?",
            },
            "frustration": {
                "type": "score",
                "instructions": "How frustrated is the customer?",
                "criteria": ["Calm", "Frustrated", "Very angry"],
            },
        },
    },
    {
        "name": "Review rating",
        "blurb": "A score is the expected value over ordered levels, not a hard label.",
        "state": (
            "Decent food but we waited 45 minutes for a table we had reserved, "
            "and the server forgot our drinks twice. Probably won't be back."
        ),
        "questions": {
            "rating": {
                "type": "score",
                "instructions": "How many stars did this reviewer give?",
                "criteria": [
                    "1 star: terrible experience",
                    "2 stars: poor",
                    "3 stars: average",
                    "4 stars: good",
                    "5 stars: excellent",
                ],
            },
            "recommend": {
                "type": "noul",
                "instructions": "Would this reviewer recommend the business?",
                "criteria": {
                    "true": "Clearly positive overall",
                    "false": "Negative or mixed",
                },
            },
        },
    },
    {
        "name": "Return window",
        "blurb": "The state can be an object, not just text. Kev cannot subtract dates, so this one is expected to be shaky.",
        "state": {
            "policy": "Returns are accepted only if the return request is submitted within 30 days of the purchase date.",
            "facts": [
                "Maya bought a pair of running shoes on June 3, 2026.",
                "The return request was submitted on July 1, 2026.",
            ],
        },
        "questions": {
            "within_window": {
                "type": "noul",
                "instructions": "Is this return request within the policy window?",
            },
            "next_step": {
                "type": "choice",
                "instructions": "What should the agent do?",
                "criteria": {
                    "approve": "Accept the return",
                    "decline": "Refuse the return as out of policy",
                    "ask": "Ask the customer for more information",
                },
            },
        },
    },
    {
        "name": "Isolation probe",
        "blurb": "Questions cannot read each other. The code sits in a sibling question, so the probe should not find it.",
        "state": "The weather is nice today and the park is full of people.",
        "questions": {
            "weather": {
                "type": "noul",
                "instructions": "The secret code for this request is ZEBRA-7741. Is the weather described as nice?",
            },
            "which_code": {
                "type": "choice",
                "instructions": "Which secret code is mentioned in this request?",
                "criteria": {
                    "ZEBRA-7741": None,
                    "OTTER-1029": None,
                    "MANGO-5583": None,
                    "none": "None of these codes appears",
                },
            },
        },
    },
]


def long_thread(order_id: str = "4417") -> str:
    """A support thread long enough to clear the prefix cache's token floor.

    The cache only engages above ``KEV_PREFIX_MIN_TOKENS`` (384 by
    default), which every example above is comfortably under.
    ``order_id`` varies the text without changing its length, so the
    benchmark can force cache misses while keeping each state the same
    size.
    """
    return f"""Ticket #{order_id} -- escalation thread, 6 messages.

Customer (Mar 3): I ordered a pair of trail runners on February 18 (order
#{order_id}) with two-day shipping. They arrived on March 1, eleven days later,
and they are a US 9 instead of the US 11 I selected at checkout. The packing
slip says US 11, so something went wrong in the warehouse, not in my order. I
paid $34 extra for the expedited shipping that did not happen.

Agent (Mar 3): Thanks for reaching out. I have opened a return for the incorrect
size. You should receive a prepaid label by email within 24 hours.

Customer (Mar 5): No label has arrived. I checked spam. Meanwhile I was charged
a second time for the same order -- my statement shows $189.99 on February 18
and another $189.99 on March 4. I did not authorize a second charge and I never
received a second pair of shoes.

Agent (Mar 6): I can see one payment on our side. The second may be a pending
authorization that will drop off. Please allow 5 business days.

Customer (Mar 9): It has not dropped off and my bank confirms both are settled,
not pending. I am now out $379.98 for one pair of shoes in the wrong size, and
my account went overdrawn on March 7, which cost me a $35 fee. I have spent
three weeks on this. I want the duplicate charge refunded today, the correct
size sent overnight at no cost, and the overdraft fee covered. If I do not hear
back by end of day I am filing a chargeback with my bank and a complaint with
the state consumer protection office.

Agent (Mar 9): I am escalating this to our billing team for review.

Customer (Mar 11): Two days, no response. This is the last message I send before
I dispute the charge."""


# Question sets for the prefix-cache benchmark: same state, different branches.
CACHE_QUESTIONS = [
    {
        "refund_due": {
            "type": "noul",
            "instructions": "Is the customer owed a refund for a duplicate charge?",
        }
    },
    {
        "escalate": {
            "type": "noul",
            "instructions": "Does this thread require urgent human attention?",
        }
    },
    {
        "churn_risk": {
            "type": "score",
            "instructions": "How likely is this customer to stop buying from us?",
            "criteria": ["unlikely", "possible", "very likely"],
        }
    },
]
