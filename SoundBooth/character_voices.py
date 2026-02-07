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
    """
    Get the Piper TTS voice model for a character
    
    Args:
        character_name: Name of the character
        
    Returns:
        Voice model string for Piper TTS
    """
    character_name = character_name.lower()
    
    if character_name in CHARACTER_VOICES:
        return CHARACTER_VOICES[character_name]["voice_model"]
    
    # Default fallback
    return "en_US-lessac-medium"

def get_character_info(character_name: str) -> dict:
    """
    Get full voice information for a character
    
    Args:
        character_name: Name of the character
        
    Returns:
        Dictionary with voice information
    """
    character_name = character_name.lower()
    
    if character_name in CHARACTER_VOICES:
        return CHARACTER_VOICES[character_name]
    
    # Default fallback
    return {
        "voice_model": "en_US-lessac-medium",
        "description": "Default American male voice",
        "language": "en_US",
        "accent": "American"
    }

def list_available_voices() -> list:
    """
    List all available character voices
    
    Returns:
        List of character names with their voice models
    """
    return [
        {
            "character": char,
            "voice_model": info["voice_model"],
            "description": info["description"]
        }
        for char, info in CHARACTER_VOICES.items()
    ]

def get_required_models() -> list:
    """
    Get list of required Piper TTS models
    
    Returns:
        List of model files that need to be downloaded
    """
    return list(set(info["voice_model"] for info in CHARACTER_VOICES.values()))

# Model download URLs (Piper TTS voice models)
MODEL_URLS = {
    "en_US-lessac-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en_US-lessac-medium.onnx",
    "en_GB-apc-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en_GB-apc-medium.onnx", 
    "es_ES-apc-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es_ES-apc-medium.onnx"
}
