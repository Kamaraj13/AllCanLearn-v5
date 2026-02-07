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
                f"piper_models/{voice}.onnx"
            ]
            for path in alt_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            else:
                logger.warning(f"Voice model not found: {voice}")
                # Fallback to basic TTS using system say (macOS) or espeak (Linux)
                return fallback_tts(text, output_file)
        
        # Generate WAV file with Piper
        wav_file = output_file.replace('.mp3', '.wav')
        try:
            cmd = [
                'piper',
                '--model', model_path,
                '--output_file', wav_file
            ]
            
            # Add text input
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                logger.error(f"Piper TTS error: {stderr}")
                return fallback_tts(text, output_file)
            
            # Convert WAV to MP3 using ffmpeg
            subprocess.run([
                'ffmpeg', '-y', '-i', wav_file,
                '-codec:a', 'libmp3lame', '-qscale:a', '2',
                output_file
            ], check=True, capture_output=True)
            
            # Clean up WAV file
            os.remove(wav_file)
            
            logger.info(f"TTS generated: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Piper TTS failed: {e}")
            return fallback_tts(text, output_file)
            
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return fallback_tts(text, output_file)

def fallback_tts(text: str, output_file: str) -> str:
    """Fallback TTS using system tools"""
    try:
        if os.system('which say > /dev/null 2>&1') == 0:
            # macOS
            subprocess.run(['say', '-o', output_file.replace('.mp3', '.aiff'), text], check=True)
            subprocess.run([
                'ffmpeg', '-y', '-i', output_file.replace('.mp3', '.aiff'),
                '-codec:a', 'libmp3lame', '-qscale:a', '2',
                output_file
            ], check=True, capture_output=True)
        else:
            # Linux espeak-ng
            subprocess.run([
                'espeak-ng', '-w', output_file.replace('.mp3', '.wav'), text
            ], check=True)
            subprocess.run([
                'ffmpeg', '-y', '-i', output_file.replace('.mp3', '.wav'),
                '-codec:a', 'libmp3lame', '-qscale:a', '2',
                output_file
            ], check=True, capture_output=True)
        
        return output_file
    except Exception as e:
        logger.error(f"Fallback TTS failed: {e}")
        return output_file  # Return path even if generation failed

def check_piper_installation():
    """Check if Piper TTS is installed"""
    try:
        result = subprocess.run(['piper', '--help'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False
