#!/usr/bin/env python3
"""
Voice Memos Transcription with Whisper
Clean, simple Python implementation
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import sys

# Configuration
MODEL_NAME = "ggml-large-v3-turbo-q5_0.bin"
MODEL_PATH = f"./models/{MODEL_NAME}"
VOICE_MEMOS_DIR = Path.home() / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
AUDIO_DIR = Path("./audio_input")
OUTPUTS_DIR = Path("./outputs")

def copy_voice_memos():
    """Copy Voice Memos to working directory"""
    print("📁 Copying Voice Memos to audio_input/...")
    
    AUDIO_DIR.mkdir(exist_ok=True)
    
    # Use rsync to copy only audio files
    cmd = [
        "rsync", "-av",
        "--include=*.m4a", "--include=*.mp3", "--include=*.wav", 
        "--include=*.caf", "--include=*.aac", "--include=*.flac",
        "--exclude=*",
        f"{VOICE_MEMOS_DIR}/",
        f"{AUDIO_DIR}/"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to copy files: {result.stderr}")
        return False
    
    return True

def get_audio_files():
    """Get all audio files sorted by creation date"""
    audio_files = []
    
    for pattern in ["*.m4a", "*.mp3", "*.wav", "*.caf", "*.aac", "*.flac"]:
        audio_files.extend(AUDIO_DIR.glob(pattern))
    
    # Sort by creation time
    audio_files.sort(key=lambda f: f.stat().st_mtime)
    return audio_files

def transcribe_file(audio_file: Path) -> str:
    """Transcribe a single audio file and return the text"""
    # Convert to wav first
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
        temp_wav_path = temp_wav.name
    
    # FFmpeg conversion
    ffmpeg_cmd = [
        "ffmpeg", "-i", str(audio_file), 
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", 
        temp_wav_path, "-y"
    ]
    
    ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if ffmpeg_result.returncode != 0:
        os.unlink(temp_wav_path)
        return f"❌ CONVERSION FAILED: {ffmpeg_result.stderr[:200]}"
    
    # Whisper transcription
    whisper_cmd = [
        "whisper-cli", 
        "-m", MODEL_PATH,
        temp_wav_path,
        "-nt", "-fa", "-t", "4", "-nth", "0.30"
    ]
    
    whisper_result = subprocess.run(whisper_cmd, capture_output=True, text=True)
    
    # Clean up temp file
    os.unlink(temp_wav_path)
    
    if whisper_result.returncode != 0:
        return f"❌ TRANSCRIPTION FAILED: {whisper_result.stderr[:200]}"
    
    transcript = whisper_result.stdout.strip()
    return transcript if transcript else "_No speech detected._"

def main():
    """Main transcription workflow"""
    if not Path(MODEL_PATH).exists():
        print(f"❌ Model not found: {MODEL_PATH}")
        print("Run ./setup.sh first to download the model")
        sys.exit(1)
    
    if not VOICE_MEMOS_DIR.exists():
        print(f"❌ Voice Memos directory not found: {VOICE_MEMOS_DIR}")
        sys.exit(1)
    
    # Copy files
    if not copy_voice_memos():
        sys.exit(1)
    
    # Get audio files
    audio_files = get_audio_files()
    total_files = len(audio_files)
    
    if total_files == 0:
        print("❌ No audio files found")
        sys.exit(1)
    
    # Create output file with dashed date format
    OUTPUTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%m-%d-%Y-%H%M%S")
    output_file = OUTPUTS_DIR / f"{timestamp}-transcript.md"
    
    print(f"🎤 Starting transcription of {total_files} files...")
    print(f"📝 Output: {output_file}")
    print()
    
    # Initialize markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Voice Memos Transcripts\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: whisper.cpp {MODEL_NAME.replace('.bin', '')}\n")
        f.write(f"Total files: {total_files}\n\n")
    
    # Process files grouped by date
    current_date = None
    successfully_transcribed = []
    
    for i, audio_file in enumerate(audio_files, 1):
        filename = audio_file.name
        file_date = datetime.fromtimestamp(audio_file.stat().st_mtime).strftime("%Y-%m-%d")
        
        # Add date header if needed
        if file_date != current_date:
            if current_date is not None:
                print()  # Add spacing between dates
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write("\n")
            
            print(f"📅 Processing files from {file_date}...")
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"# {file_date}\n\n")
            current_date = file_date
        
        print(f"[{i}/{total_files}] Processing: {filename}")
        
        # Transcribe
        transcript = transcribe_file(audio_file)
        
        # Show transcript in real-time
        if not transcript.startswith("❌") and transcript != "_No speech detected._":
            print(f"✅ Transcript:")
            print(transcript)
            print("---")
            print()
            successfully_transcribed.append(audio_file)
        else:
            print(f"⚠️  {transcript}")
            print()
        
        # Add to markdown
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"## {filename}\n\n")
            f.write(f"{transcript}\n\n")
    
    # Clean up successfully transcribed files
    for audio_file in successfully_transcribed:
        audio_file.unlink()
    
    # Clean up directory if empty
    remaining_files = len(list(AUDIO_DIR.glob("*")))
    if remaining_files == 0:
        AUDIO_DIR.rmdir()
        print(f"🗑️  All files transcribed successfully - audio_input cleaned up")
    else:
        print(f"⚠️  {remaining_files} failed files kept in {AUDIO_DIR} for inspection")
    
    print()
    print("✅ Transcription complete!")
    print(f"📄 Output saved to: {output_file}")
    print(f"📊 Total files processed: {total_files}")

if __name__ == "__main__":
    main()