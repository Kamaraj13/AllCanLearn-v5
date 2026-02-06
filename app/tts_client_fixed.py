# tts_client.py

import subprocess
import os
import time
import platform

# Voice mapping for espeak-ng (Linux) and say (macOS)
VOICE_MAP_MACOS = {
    "Indian English": "Veena",
    "American": "Alex",
    "British": "Daniel",
    "Australian": "Karen",
    "Spanish": "Monica",
    "Arabian": "Majed",
    "Mexican": "Juan",
    "default": "Alex",
}

VOICE_MAP_LINUX = {
    "Indian English": "en-in",
    "American": "en-us",
    "British": "en-gb",
    "Australian": "en-au",
    "Spanish": "es",
    "Arabian": "ar",
    "Mexican": "es-mx",
    "default": "en-us",
}

def is_macos():
    return platform.system() == "Darwin"

def resolve_voice(accent):
    """Get voice identifier based on OS and accent"""
    if is_macos():
        return VOICE_MAP_MACOS.get(accent, VOICE_MAP_MACOS["default"])
    else:
        return VOICE_MAP_LINUX.get(accent, VOICE_MAP_LINUX["default"])

async def speak_text(text, accent, folder="tts_output"):
    """Generate speech audio file in MP3 format using platform-appropriate TTS"""
    os.makedirs(folder, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    temp_file = None
    mp3_filename = f"{timestamp}.mp3"
    mp3_filepath = os.path.join(folder, mp3_filename)
    
    try:
        if is_macos():
            # macOS: use native 'say' command, then convert to MP3
            temp_file = f"{timestamp}_temp.aiff"
            temp_filepath = os.path.join(folder, temp_file)
            voice = resolve_voice(accent)
            subprocess.run(["say", "-v", voice, text, "-o", temp_filepath], check=True)
            
            # Convert AIFF to MP3 with good quality (192kbps)
            subprocess.run([
                "ffmpeg", "-i", temp_filepath, 
                "-codec:a", "libmp3lame", 
                "-b:a", "192k",
                "-y",  # Overwrite if exists
                mp3_filepath
            ], check=True, capture_output=True)
            
            # Clean up temp file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                
        else:
            # Linux: use espeak-ng to WAV, then convert to MP3
            temp_file = f"{timestamp}_temp.wav"
            temp_filepath = os.path.join(folder, temp_file)
            voice = resolve_voice(accent)
            
            # espeak-ng with quality improvements
            subprocess.run(
                ["espeak-ng", "-v", voice, "-s", "100", "-p", "50", 
                 "-a", "200", "-g", "15", "-w", temp_filepath, text],
                check=True,
                capture_output=True
            )
            
            # Convert WAV to MP3 with good quality (192kbps)
            subprocess.run([
                "ffmpeg", "-i", temp_filepath, 
                "-codec:a", "libmp3lame", 
                "-b:a", "192k",
                "-y",  # Overwrite if exists
                mp3_filepath
            ], check=True, capture_output=True)
            
            # Clean up temp file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
    
    except Exception as e:
        # Clean up on error
        if temp_file and os.path.exists(os.path.join(folder, temp_file)):
            os.remove(os.path.join(folder, temp_file))
        raise e
    
    # Return just filename (no path prefix)
    return mp3_filename
