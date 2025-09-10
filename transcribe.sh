#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper that calls the Python transcription script
uv run python transcribe.py "$@"