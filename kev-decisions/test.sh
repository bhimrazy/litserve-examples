#!/bin/sh
set -eu

echo "==> HTTP client: example requests"
uv run python client.py

echo ""
echo "==> TypeSafe SDK client: same requests, typed answers"
uv run python client_sdk.py

echo ""
echo "==> Benchmark: prefix cache and packed requests"
uv run python benchmark.py --ci

echo ""
echo "==> All checks passed"
