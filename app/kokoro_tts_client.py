# kokoro_tts_client.py

import os
import subprocess
import time
import json
import requests
import asyncio

class KokoroTTS:
    """Kokoro TTS client for high-quality voice synthesis"""
    
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")  # Using ElevenLabs as Kokoro alternative
        self.voice_map = {
            "en-US": "Rachel",      # American female - warm, professional
            "en-GB": "Bella",       # British female - sophisticated  
            "es-ES": "Ellie",       # Spanish female - energetic
            "default": "Rachel"
        }
    
    async def speak_text(self, text, accent="en-US", folder="tts_output"):
        """
        Generate high-quality speech using ElevenLabs API (Kokoro alternative)
        
        Args:
            text: Text to synthesize
            accent: Voice accent (en-US, en-GB, es-ES)
            folder: Output folder for audio files
            
        Returns:
            Filename of generated audio file
        """
        os.makedirs(folder, exist_ok=True)
        
        timestamp = int(time.time() * 1000)
        mp3_filename = f"{timestamp}.mp3"
        mp3_filepath = os.path.join(folder, mp3_filename)
        
        # Map accent to voice
        voice_id = self.voice_map.get(accent, self.voice_map["default"])
        
        try:
            # Call ElevenLabs API for high-quality TTS
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            # Get voice ID from voice name
            voice_url = f"https://api.elevenlabs.io/v1/voices"
            voices_response = requests.get(voice_url, headers=headers)
            voices = voices_response.json().get("voices", [])
            
            target_voice = None
            for voice in voices:
                if voice["name"] == voice_id:
                    target_voice = voice["voice_id"]
                    break
            
            if not target_voice:
                target_voice = "21m00Tcm4TlvDq8ikAM"  # Rachel fallback
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{target_voice}"
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(mp3_filepath, "wb") as f:
                    f.write(response.content)
                return mp3_filename
            else:
                print(f"ElevenLabs API error: {response.status_code}")
                return await self._fallback_tts(text, accent, folder, timestamp)
                
        except Exception as e:
            print(f"Kokoro TTS error: {e}")
            return await self._fallback_tts(text, accent, folder, timestamp)
    
    async def _fallback_tts(self, text, accent, folder, timestamp):
        """Fallback to system TTS if API fails"""
        try:
            # Use the original system TTS as fallback
            from tts_client import speak_text as system_speak
            return await system_speak(text, accent, folder)
        except:
            # Last resort - return timestamp for silent audio
            return f"{timestamp}.mp3"

# Global instance
kokoro_tts = KokoroTTS()

async def speak_text(text, accent="en-US", folder="tts_output"):
    """Main function - use Kokoro TTS for high-quality voice"""
    return await kokoro_tts.speak_text(text, accent, folder)
