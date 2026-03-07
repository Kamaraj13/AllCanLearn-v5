# tts_client.py - Piper TTS Client for AllCanLearn Radio Station

import os
import subprocess
import tempfile
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def speak_text(text: str, voice: Optional[str] = None, output_file: Optional[str] = None) -> str:
    """
    Convert text to speech using Piper TTS
    
    Args:
        text: Text to convert to speech
        voice: Voice model to use (optional)
        output_file: Output file path (optional, will generate if not provided)
    
    Returns:
        Path to generated audio file
    """
    try:
        # Generate output filename if not provided
        if not output_file:
            import time
            timestamp = int(time.time() * 1000)
            output_file = f"tts_output/{timestamp}.mp3"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Default voice model
        if not voice:
            voice = "en_US-lessac-medium"
        
        # Check if voice model exists
        model_path = f"/home/$USER/piper_models/{voice}.onnx"
        if not os.path.exists(model_path):
            # Try alternative paths
            alt_paths = [
                f"./piper_models/{voice}.onnx",
                f"~/.local/share/piper_tts/{voice}.onnx"
            ]
            for alt_path in alt_paths:
                if os.path.exists(alt_path):
                    model_path = alt_path
                    break
            else:
                logger.warning(f"Voice model {voice} not found, using fallback")
                return fallback_tts(text, output_file)
        
        # Use Piper TTS
        cmd = [
            "piper-tts",
            "--model", model_path,
            "--output_file", output_file
        ]
        
        # Write text to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            temp_text_file = f.name
        
        try:
            # Run Piper TTS
            with open(temp_text_file, 'r') as f:
                result = subprocess.run(
                    cmd,
                    stdin=f,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0 and os.path.exists(output_file):
                logger.info(f"TTS generated: {output_file}")
                return output_file
            else:
                logger.warning(f"Piper TTS failed: {result.stderr}")
                return fallback_tts(text, output_file)
        finally:
            os.unlink(temp_text_file)
            
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return fallback_tts(text, output_file)

def fallback_tts(text: str, output_file: str) -> str:
    """Fallback TTS using system TTS"""
    try:
        if os.name == 'posix':  # macOS/Linux
            # Use system say/espeak
            temp_wav = output_file.replace('.mp3', '.wav')
            
            if os.system('which say > /dev/null 2>&1') == 0:  # macOS
                os.system(f'say -o "{temp_wav}" "{text}"')
            elif os.system('which espeak-ng > /dev/null 2>&1') == 0:  # Linux
                os.system(f'espeak-ng -w "{temp_wav}" "{text}"')
            else:
                raise Exception("No TTS available")
            
            # Convert to MP3 if ffmpeg available
            if os.system('which ffmpeg > /dev/null 2>&1') == 0:
                os.system(f'ffmpeg -i "{temp_wav}" -y "{output_file}" 2>/dev/null')
                os.unlink(temp_wav)
            else:
                # Keep WAV if no ffmpeg
                output_file = temp_wav
                
            return output_file
        else:
            raise Exception("Unsupported OS")
            
    except Exception as e:
        logger.error(f"Fallback TTS failed: {e}")
        # Create empty file as last resort
        with open(output_file, 'w') as f:
            f.write("")
        return output_file

def check_piper_installation():
    """Check if Piper TTS is installed"""
    return os.system('which piper-tts > /dev/null 2>&1') == 0

def install_piper():
    """Install Piper TTS (Linux only)"""
    if os.name == 'posix':
        os.system('pip install piper-tts')
        return check_piper_installation()
    return False
