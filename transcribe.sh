#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper that calls the Python transcription script
uv run python transcribe.py "$@"

# Find and open the most recent transcript file in VS Code
LATEST_TRANSCRIPT=$(find ./outputs -name "*-transcript.md" -type f -exec ls -t {} + | head -n 1)

if [ -n "$LATEST_TRANSCRIPT" ]; then
    echo "🚀 Opening transcript in VS Code: $LATEST_TRANSCRIPT"
    code "$LATEST_TRANSCRIPT"
else
    echo "⚠️  No transcript file found to open"
fi