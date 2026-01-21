#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Running Kelp Automated Deal Flow Demo"

cd "$PROJECT_ROOT"
python -m src.main --company entertainment-complex

echo "✅ Demo completed"
