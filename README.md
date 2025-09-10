# Whisper Runner

Fast, accurate Voice Memos transcription using Whisper with Metal acceleration.

## Quick Setup & Run

Copy and paste this into your terminal:
to run
```bash
./transcribe.sh
```

to install...

```bash
git clone [your-repo-url] whisper-runner
cd whisper-runner
./setup.sh
```


That's it! Your Voice Memos will be transcribed with real-time output.

## What You Get

- **Real-time transcription display** as each file processes
- **Date-organized output** in `outputs/MM-DD-YYYY-HHMMSS-transcript.md`  
- **Metal acceleration** on Apple Silicon (fast!)
- **Smart error handling** keeps problematic files for inspection
- **Clean workflow** - copies, transcribes, cleans up automatically

## Output Example

```markdown
# 2025-09-09

## 20250909 191541-3C834D62.m4a

Hey, so I'm thinking about ways to continue to increase some pressure and to call urgency...

## 20250909 185555-F1F0B8D8.m4a  

So email should go something along the lines of like, Hey, I've talked to you about this before...
```

## Tech Stack

- **Python** with UV dependency management
- **whisper-cli** with Large v3 Turbo quantized model (~547MB)
- **Metal acceleration** for M1/M2 Macs
- **FFmpeg** for audio format conversion

## Files

- `setup.sh` - One-time setup (installs whisper.cpp + downloads model)
- `transcribe` - Main command (shell wrapper) 
- `transcribe.py` - Core Python logic