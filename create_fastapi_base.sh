#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "Creating Python virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing FastAPI..."
python -m pip install "fastapi[standard]"

echo "Writing starter FastAPI app to main.py..."
cat > main.py <<'PY'
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
PY

echo ""
echo "FastAPI base project is ready."
echo ""
echo "Run it with:"
echo "  source .venv/bin/activate"
echo "  fastapi dev main.py"
echo ""
echo "Then open:"
echo "  http://127.0.0.1:8000"
echo "  http://127.0.0.1:8000/docs"
