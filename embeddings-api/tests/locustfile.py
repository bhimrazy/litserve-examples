from locust import HttpUser, TaskSet, task, between
from benchmark import INPUT_TEXT


class EmbeddingsTest(TaskSet):
    @task
    def test_embeddings_endpoint(self):
        num_inputs = 2
        payload = {
            "input": [str(INPUT_TEXT)] * num_inputs,
            "model": "jinaai/jina-embeddings-v2-small-en",
            "encoding_format": "float",
        }
        self.client.post("/v1/embeddings", json=payload)


class EmbeddingsUser(HttpUser):
    tasks = [EmbeddingsTest]
    wait_time = between(1, 3)  # Adjust wait time as needed

# Run the test with the following command:
# locust -f locustfile.py