import logging
import subprocess
import time
from functools import wraps

import psutil
import requests
import torch
from benchmark import run_benchmark

logging.basicConfig(level=logging.INFO)
device = "cuda" if torch.cuda.is_available() else "cpu"
device = "mps" if torch.backends.mps.is_available() else device

CONF = {
    "cpu": {"num_requests": 50},
    "mps": {"num_requests": 50},
    "cuda": {"num_requests": 100},
}


def run_python_script(file_name, wait_time=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Running the python script: {file_name}")
            process = subprocess.Popen(
                ["python", file_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logging.info("Waiting for the server to start...")
            time.sleep(wait_time)

            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error occurred: {e}")
                raise
            finally:
                logging.info("Terminating the server...")
                parent = psutil.Process(process.pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                gone, still_alive = psutil.wait_procs(children, timeout=3)
                for p in still_alive:
                    logging.warning(f"Force killing process {p.pid}")
                    p.kill()
                parent.terminate()
                parent.wait(3)
                if parent.is_running():
                    logging.warning(f"Force killing process {parent.pid}")
                    parent.kill()

        return wrapper

    return decorator


def check_health(port):
    url = f"http://localhost:{port}/health"
    for _ in range(10):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return True
        except requests.RequestException:
            time.sleep(1)


@run_python_script("embeddings-api/tests/fastapi_server.py")
def run_fastapi_benchmark(num_of_runs, warmup):
    port = 8001
    logging.info(f"Running the benchmark on port {port}")
    check_health(port)
    run_benchmark(
        runs=num_of_runs, warmup=warmup, port=port, num_of_inputs=1, **CONF[device]
    )


@run_python_script("embeddings-api/server.py")
def run_litserve_benchmark(num_of_runs, warmup):
    port = 8000
    logging.info(f"Running the benchmark on port {port}")
    check_health(port)
    run_benchmark(
        runs=num_of_runs, warmup=warmup, port=port, num_of_inputs=1, **CONF[device]
    )


@run_python_script("embeddings-api/tests/litserve_server_with_multi_worker.py")
def run_litserve_multi_worker_benchmark(num_of_runs, warmup):
    port = 8002
    logging.info(f"Running the benchmark on port {port}")
    check_health(port)
    run_benchmark(
        runs=num_of_runs, warmup=warmup, port=port, num_of_inputs=1, **CONF[device]
    )


def main():
    num_of_runs = 10
    warmup = 2

    logging.info(f"Running the benchmark on device: {device}")
    logging.info(f"Number of runs: {num_of_runs}")
    logging.info(f"Warmup: {warmup}")

    logging.info("Running the benchmark on FastAPI server")
    run_fastapi_benchmark(num_of_runs, warmup)

    logging.info("Running the benchmark on LitServe server")
    run_litserve_benchmark(num_of_runs, warmup)

    logging.info("Running the benchmark on LitServe server with multi worker")
    run_litserve_multi_worker_benchmark(num_of_runs, warmup)


if __name__ == "__main__":
    main()
