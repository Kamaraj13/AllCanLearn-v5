# piper_tts_client.py

import os
import subprocess
import time
import asyncio

class PiperTTS:
    """Piper TTS client - Free, high-quality open source TTS"""
    
    def __init__(self):
        self.voice_map = {
            "en-US": "en_US-lessac-medium",      # American male - clear, professional
            "en-GB": "en_GB-apc-medium",      # British male - sophisticated
            "es-ES": "es_ES-apc-medium",      # Spanish male - natural
            "default": "en_US-lessac-medium"
        }
        
        # Check if Piper is available
        self.piper_available = self._check_piper()
    
    def _check_piper(self):
        """Check if Piper TTS is available"""
        try:
            result = subprocess.run(["piper", "--help"], 
                              capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def speak_text(self, text, accent="en-US", folder="tts_output"):
        """
        Generate high-quality speech using Piper TTS
        
        Args:
            text: Text to synthesize
            accent: Voice accent (en-US, en-GB, es-ES)
            folder: Output folder for audio files
            
        Returns:
            Filename of generated audio file
        """
        os.makedirs(folder, exist_ok=True)
        
        timestamp = int(time.time() * 1000)
        wav_filename = f"{timestamp}.wav"
        wav_filepath = os.path.join(folder, wav_filename)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        # Get voice model
        voice_model = self.voice_map.get(accent, self.voice_map["default"])
        
        try:
            if self.piper_available:
                # Use Piper TTS for high-quality audio
                cmd = [
                    "piper",
                    "--model", f"/home/vikki/piper_models/{voice_model}.onnx",
                    "--output_file", wav_filepath
                ]
                
                # Pipe text to Piper
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=text.encode(), timeout=30)
                
                if process.returncode == 0 and os.path.exists(wav_filepath):
                    # Convert to MP3 for web compatibility
                    await self._convert_to_mp3(wav_filepath, mp3_filepath)
                    os.remove(wav_filepath)  # Clean up WAV
                    return mp3_filename
                else:
                    print(f"Piper TTS failed: {stderr.decode()}")
                    return await self._fallback_tts(text, accent, folder, timestamp)
            else:
                # Install Piper first time
                await self._install_piper()
                return await self.speak_text(text, accent, folder)  # Retry
                
        except Exception as e:
            print(f"Piper TTS error: {e}")
            return await self._fallback_tts(text, accent, folder, timestamp)
    
    async def _install_piper(self):
        """Install Piper TTS on Ubuntu"""
        try:
            print("🔧 Installing Piper TTS for high-quality voice...")
            
            # Install Piper
            install_cmds = [
                "sudo apt update",
                "sudo apt install -y python3-pip",
                "pip3 install piper-tts",
                "mkdir -p /home/vikki/piper_models",
                "cd /home/vikki/piper_models"
            ]
            
            for cmd in install_cmds:
                subprocess.run(cmd, shell=True, check=True)
            
            # Download voice models
            models = [
                "en_US-lessac-medium.onnx",
                "en_GB-lessac-medium.onnx", 
                "es_ES-lessac-medium.onnx"
            ]
            
            for model in models:
                download_cmd = f"wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{model}"
                subprocess.run(download_cmd, shell=True, check=True)
            
            print("✅ Piper TTS installed successfully!")
            self.piper_available = True
            
        except Exception as e:
            print(f"❌ Failed to install Piper: {e}")
    
    async def _convert_to_mp3(self, wav_path, mp3_path):
        """Convert WAV to MP3 using ffmpeg"""
        try:
            subprocess.run([
                "ffmpeg", "-i", wav_path, "-codec:a", "mp3", 
                "-b:a", "128k", "-y", mp3_path
            ], check=True, capture_output=True, timeout=30)
        except Exception as e:
            print(f"MP3 conversion failed: {e}")
    
    async def _fallback_tts(self, text, accent, folder, timestamp):
        """Fallback to original system TTS"""
        try:
            from tts_client import speak_text as system_speak
            return await system_speak(text, accent, folder)
        except:
            return f"{timestamp}.wav"

# Global instance
piper_tts = PiperTTS()

async def speak_text(text, accent="en-US", folder="tts_output"):
    """Main function - use Piper TTS for high-quality voice"""
    return await piper_tts.speak_text(text, accent, folder)
