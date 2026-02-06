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
    "Spanish": "Monica",        # Spanish accent
    "Arabian": "Majed",         # Arabic accent (female alternative: Maged)
    "Mexican": "Juan",          # Mexican Spanish accent
    "default": "Alex",
}

VOICE_MAP_LINUX = {
    "Indian English": "en-in",  # Indian English
    "American": "en-us",         # US English
    "British": "en-gb",          # British English
    "Australian": "en-au",       # Australian English
    "Spanish": "es",             # Spanish
    "Arabian": "ar",             # Arabic
    "Mexican": "es-mx",          # Mexican Spanish
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
    """Generate speech audio file using platform-appropriate TTS and convert to MP3"""
    os.makedirs(folder, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    
    if is_macos():
        # macOS: use native 'say' command, then convert to MP3
        aiff_filename = f"{timestamp}.aiff"
        aiff_filepath = os.path.join(folder, aiff_filename)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        voice = resolve_voice(accent)
        subprocess.run(["say", "-v", voice, text, "-o", aiff_filepath], check=True)
        
        # Convert AIFF to MP3 using ffmpeg (if available) or keep AIFF
        try:
            subprocess.run([
                "ffmpeg", "-i", aiff_filepath, "-codec:a", "mp3", "-b:a", "64k", 
                "-y", mp3_filepath
            ], check=True, capture_output=True)
            # Remove original AIFF file to save space
            os.remove(aiff_filepath)
            return mp3_filename
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to AIFF if ffmpeg not available
            return aiff_filename
    else:
        # Linux: use espeak-ng with WAV output, then convert to MP3
        wav_filename = f"{timestamp}.wav"
        wav_filepath = os.path.join(folder, wav_filename)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        voice = resolve_voice(accent)
        
        # Generate WAV first with significantly improved clarity
        subprocess.run([
            "espeak-ng", "-v", voice, "-s", "140", "-p", "50", "-a", "180", 
            "-g", "2", "-k", "20", "-w", wav_filepath, text
        ], check=True, capture_output=True)
        
        # Convert to MP3 with premium quality
        try:
            subprocess.run([
                "ffmpeg", "-i", wav_filepath, "-codec:a", "mp3", "-b:a", "128k", 
                "-ar", "44100", "-q:a", "0", "-compression_level", "0", "-y", mp3_filepath
            ], check=True, capture_output=True)
            # Remove original WAV file to save space
            os.remove(wav_filepath)
            return mp3_filename
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to WAV if ffmpeg not available
            return wav_filename
