"""
curl http://127.0.0.1:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      "प्रधानमन्त्री केपी शर्मा ओली र अमेरिकी प्रविधि व्यवसायी इलन मस्कबीच भर्चुअल संवाद भएको छ ।",
      "Un bellissimo tramonto sulla spiaggia",
      "浜辺に沈む美しい夕日",
      "A beautiful sunset over the beach",
      "Ένα όμορφο ηλιοβασίλεμα πάνω από την παραλία",
      "https://i.ibb.co/nQNGqL0/beach1.jpg"
    ],
    "model": "jina-clip-v2",
    "encoding_format": "float"
  }'
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="lit")

input_data = [
    "प्रधानमन्त्री केपी शर्मा ओली र अमेरिकी प्रविधि व्यवसायी इलन मस्कबीच भर्चुअल संवाद भएको छ ।",  # Nepali
    "Un bellissimo tramonto sulla spiaggia",  # French
    "浜辺に沈む美しい夕日",  # Japanese
    "A beautiful sunset over the beach",  # English
    "Ένα όμορφο ηλιοβασίλεμα πάνω από την παραλία",  # Greek
    "https://i.ibb.co/nQNGqL0/beach1.jpg",  # Image URL
]

response = client.embeddings.create(
    model="jina-clip-v2",
    input=input_data,
    encoding_format="float",
)

print(response)
