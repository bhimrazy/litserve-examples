"""
Benchmarking the embeddings API

Adapted from https://github.com/Lightning-AI/LitServe/blob/main/tests/parity_fastapi/benchmark.py
"""

import asyncio
import logging
import time
from typing import Dict, Tuple

import httpx
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

SERVER_URL = "http://localhost:{}/v1/embeddings"

INPUT_TEXT = """
LitServe, developed by Lightning AI, is an advanced serving engine designed to deploy AI models with exceptional speed and flexibility. 
Built on FastAPI, it offers optimized features specifically for machine learning and deep learning applications, such as batching, streaming, and GPU autoscaling. 
These enhancements enable faster inference and reduced overhead compared to standard FastAPI setups, often doubling the performance for AI workloads.
Its key capabilities include seamless support for large language models (LLMs), computer vision models, NLP, speech processing, and classical machine learning algorithms. 
LitServe is highly scalable, supporting multi-model systems and enabling efficient resource utilization through features like auto-scaling workers and zero-server scaling. 
It also integrates easily with frameworks like PyTorch, TensorFlow, and JAX, making it versatile for diverse AI projects.
Users can self-host LitServe for full control or opt for a managed deployment via Lightning AI's platform, which offers enterprise-grade features like authentication, VPC support, and one-click scalability. 
"""


async def send_embedding_request(
    client: httpx.AsyncClient, port: int = 8000, num_inputs: int = 1
) -> Tuple[float, int]:
    """Send a request to the embeddings API and return the response time and status code."""
    payload = {
        "input": [str(INPUT_TEXT)] * num_inputs,
        "model": "jinaai/jina-embeddings-v2-small-en",
        "encoding_format": "float",
    }
    start_time = time.time()
    try:
        response = await client.post(SERVER_URL.format(port), json=payload)
        status_code = response.status_code
    except httpx.RequestError as e:
        logging.error(f"Request failed: {e}")
        status_code = 500  # Internal Server Error
    end_time = time.time()
    return end_time - start_time, status_code


async def benchmark(
    num_of_inputs: int = 1,
    num_requests: int = 100,
    concurrency: int = 100,
    port: int = 8000,
    run_id: int = 0,
) -> Dict[str, float]:
    """Run a benchmark on the given send_request function."""
    start_time = time.time()  # Start the benchmark timer

    async with httpx.AsyncClient() as client:
        tasks = [
            send_embedding_request(client, port, num_of_inputs)
            for _ in range(num_requests)
        ]

        response_times = []
        status_codes = []

        for task in tqdm(
            asyncio.as_completed(tasks),
            total=num_requests,
            desc=f"Benchmarking Run {run_id}",
        ):
            response_time, status_code = await task
            response_times.append(response_time)
            status_codes.append(status_code)

    end_time = time.time()
    total_benchmark_time = end_time - start_time  # in seconds

    # Calculate benchmark metrics
    avg_response_time = sum(response_times) / num_requests
    success_requests = status_codes.count(200)
    failed_requests = num_requests - success_requests
    success_rate = success_requests / num_requests * 100
    rps = num_requests / total_benchmark_time

    metrics = {
        "Total Requests": num_requests,
        "Concurrency": concurrency,
        "Total Benchmark Time (s)": total_benchmark_time,
        "Avg Response Time (ms)": avg_response_time * 1000,
        "Success Requests": success_requests,
        "Failed Requests": failed_requests,
        "Success Rate (%)": success_rate,
        "Requests Per Second (RPS)": rps,
    }

    # Log the metrics
    logging.info("-" * 50)
    for key, value in metrics.items():
        logging.info(f"{key}: {value}")
    logging.info("-" * 50)

    return metrics


async def run_benchmark(runs: int = 10, warmup: int = 1, **config) -> None:
    """Run the benchmark multiple times and calculate the average metrics."""
    results = []
    for i in range(runs + warmup):
        results.append(await benchmark(run_id=i, **config))

    # Calculate the average of the benchmark metrics
    results = results[warmup:]  # exclude the warmup runs
    avg_metrics = {
        "Total Runs": runs,
        "Warmup Runs": warmup,
    }
    for key in results[0].keys():
        avg_metrics[key] = sum(result[key] for result in results) / runs

    print("Average Benchmark Metrics")
    print("-" * 50)

    for key, value in avg_metrics.items():
        print(f"{key}: {value}")
    print("-" * 50)


if __name__ == "__main__":
    num_of_inputs = 1
    word_count = len(INPUT_TEXT.split())
    print(
        f"Running benchmark with {num_of_inputs} inputs, each with approx word count: {word_count}"
    )
    asyncio.run(
        run_benchmark(
            runs=10,
            warmup=1,
            num_of_inputs=num_of_inputs,
            num_requests=100,
            concurrency=100,
            port=8000,
        )
    )
