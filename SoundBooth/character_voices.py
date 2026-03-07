# character_voices.py - Voice mappings for AllCanLearn Radio Station characters

CHARACTER_VOICES = {
    "captain": {
        "voice_model": "en_US-lessac-medium",
        "description": "American male voice - clear and professional",
        "language": "en_US",
        "accent": "American"
    },
    "sage": {
        "voice_model": "en_GB-apc-medium", 
        "description": "British male voice - sophisticated and wise",
        "language": "en_GB",
        "accent": "British"
    },
    "rebel": {
        "voice_model": "es_ES-apc-medium",
        "description": "Spanish male voice - natural and passionate",
        "language": "es_ES", 
        "accent": "Spanish"
    },
    "architect": {
        "voice_model": "en_US-lessac-medium",
        "description": "American male voice - versatile and practical",
        "language": "en_US",
        "accent": "American"
    }
}

def get_voice_for_character(character_name: str) -> str:
    """Get voice model for a character"""
    # Map character names to voice keys
    character_mapping = {
        "Exam Strategist": "captain",
        "Serving Officer": "architect", 
        "Fresh Qualifier": "captain",
        "Citizen": "sage",
        "Elena": "rebel",
        "Fatima": "sage",
        "Priya": "captain",
        "Vikram": "architect",
        "Sofia": "rebel",
        "Alex": "captain",
        "Jasmine": "sage"
    }
    
    voice_key = character_mapping.get(character_name, "captain")
    return CHARACTER_VOICES[voice_key]["voice_model"]

def get_voice_info(voice_model: str) -> dict:
    """Get information about a voice model"""
    for voice_data in CHARACTER_VOICES.values():
        if voice_data["voice_model"] == voice_model:
            return voice_data
    return CHARACTER_VOICES["captain"]

def list_available_voices() -> list:
    """List all available voice models"""
    return [voice["voice_model"] for voice in CHARACTER_VOICES.values()]

def download_voice_models():
    """Download voice models (Linux only)"""
    import os
    
    models_dir = "/home/$USER/piper_models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir, exist_ok=True)
    
    # Download commands for voice models
    download_commands = {
        "en_US-lessac-medium": "wget https://huggingface.co/rhasspy/piper-voice-v1-en-us-lessac-medium/resolve/main/en_US-lessac-medium.onnx -O " + models_dir + "/en_US-lessac-medium.onnx",
        "en_GB-apc-medium": "wget https://huggingface.co/rhasspy/piper-voice-v1-en-gb-apc-medium/resolve/main/en_GB-apc-medium.onnx -O " + models_dir + "/en_GB-apc-medium.onnx",
        "es_ES-apc-medium": "wget https://huggingface.co/rhasspy/piper-voice-v1-es-es-apc-medium/resolve/main/es_ES-apc-medium.onnx -O " + models_dir + "/es_ES-apc-medium.onnx"
    }
    
    for voice_model, command in download_commands.items():
        if not os.path.exists(f"{models_dir}/{voice_model}.onnx"):
            print(f"Downloading {voice_model}...")
            os.system(command)
        else:
            print(f"{voice_model} already exists")
