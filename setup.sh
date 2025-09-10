#!/usr/bin/env bash
set -euo pipefail

echo "🎤 Setting up Whisper Runner..."

# Create directories
mkdir -p models outputs

# Install whisper.cpp via Homebrew
echo "📦 Installing whisper.cpp..."
if ! command -v whisper-cpp &> /dev/null; then
    brew install whisper-cpp
else
    echo "✅ whisper.cpp already installed"
fi

# Download large-v3-turbo q5_0 quantized model (~547MB, best accuracy/speed balance)
MODEL_NAME="ggml-large-v3-turbo-q5_0.bin"
echo "📥 Downloading Whisper large-v3-turbo q5_0 model..."
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$MODEL_NAME"
if [[ ! -f "models/$MODEL_NAME" ]]; then
    curl -L -o "models/$MODEL_NAME" "$MODEL_URL"
    echo "✅ Model downloaded to models/$MODEL_NAME"
else
    echo "✅ Model already exists"
fi

echo "🚀 Setup complete! Run ./transcribe.sh to process your Voice Memos."