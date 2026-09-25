#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

uv venv .venv
source .venv/bin/activate

uv pip install -r requirements.txt
