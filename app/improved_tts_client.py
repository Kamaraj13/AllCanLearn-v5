# improved_tts_client.py

import os
import subprocess
import time
import platform

def is_macos():
    return platform.system() == "Darwin"

def resolve_voice(accent):
    """Get voice identifier based on OS and accent"""
    if is_macos():
        # macOS voices - better quality
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
        return VOICE_MAP_MACOS.get(accent, VOICE_MAP_MACOS["default"])
    else:
        # Linux voices - use better espeak-ng settings
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
        return VOICE_MAP_LINUX.get(accent, VOICE_MAP_LINUX["default"])

async def speak_text(text, accent, folder="tts_output"):
    """Generate speech audio file using improved system TTS"""
    os.makedirs(folder, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    
    if is_macos():
        # macOS: use native 'say' command with better quality
        aiff_filename = f"{timestamp}.aiff"
        aiff_filepath = os.path.join(folder, aiff_filename)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        voice = resolve_voice(accent)
        subprocess.run([
            "say", "-v", voice, "-r", "180", text, "-o", aiff_filepath
        ], check=True)
        
        # Convert to MP3 with higher quality
        try:
            subprocess.run([
                "ffmpeg", "-i", aiff_filepath, "-codec:a", "mp3", "-b:a", "128k", 
                "-ar", "44100", "-y", mp3_filepath
            ], check=True, capture_output=True)
            os.remove(aiff_filepath)
            return mp3_filename
        except (subprocess.CalledProcessError, FileNotFoundError):
            return aiff_filename
    else:
        # Linux: use espeak-ng with improved settings
        wav_filename = f"{timestamp}.wav"
        wav_filepath = os.path.join(folder, wav_filename)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        voice = resolve_voice(accent)
        
        # Generate WAV with better quality settings
        subprocess.run([
            "espeak-ng", "-v", voice, "-s", "140", "-p", "50", "-a", "180", 
            "-g", "10", "-w", wav_filepath, text
        ], check=True, capture_output=True)
        
        # Convert to MP3 with higher quality
        try:
            subprocess.run([
                "ffmpeg", "-i", wav_filepath, "-codec:a", "mp3", "-b:a", "128k", 
                "-ar", "44100", "-y", mp3_filepath
            ], check=True, capture_output=True)
            os.remove(wav_filepath)
            return mp3_filename
        except (subprocess.CalledProcessError, FileNotFoundError):
            return wav_filename
