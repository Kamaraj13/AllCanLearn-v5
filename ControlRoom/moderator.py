import os
import re
import json
import asyncio
from dotenv import load_dotenv

from Newsroom.groq_client import call_groq
from ControlRoom.characters import CHARACTERS

load_dotenv()

MAX_TURNS = 8
MAX_ESSENTIAL_TURNS = 20  # Extended Essential Topics for deeper content


async def generate_tts_batch(entries, tts_enabled):
    """Parallelize TTS generation for multiple speakers at once."""
    if not tts_enabled:
        return entries
    
    # Generate all TTS files in parallel
    tts_tasks = []
    for entry in entries:
        voice = get_voice_for_character(entry.get("speaker", ""))
        # Run TTS in thread pool since it's synchronous
        task = asyncio.to_thread(speak_text, entry["message"], voice)
        tts_tasks.append(task)
    
    tts_results = await asyncio.gather(*tts_tasks, return_exceptions=True)
    
    # Attach results to entries
    for entry, tts_result in zip(entries, tts_results):
        if not isinstance(tts_result, Exception) and tts_result:
            entry["tts"] = tts_result  # Just filename, no path prefix
        else:
            entry["tts"] = None
    
    return entries


async def run_roundtable(tts_enabled=True, topic_type="government_jobs", custom_topic=None):
    """
    Run a roundtable discussion.
    
    Args:
        tts_enabled: Enable text-to-speech
        topic_type: "government_jobs", "travel", "tech_startup", "personal_finance", "mental_health", "custom", or "essential"
        custom_topic: Custom topic string when topic_type is "custom"
    """
    if topic_type == "travel":
        return await run_travel_roundtable(tts_enabled)
    elif topic_type == "tech_startup":
        return await run_tech_startup_roundtable(tts_enabled)
    elif topic_type == "personal_finance":
        return await run_personal_finance_roundtable(tts_enabled)
    elif topic_type == "mental_health":
        return await run_mental_health_roundtable(tts_enabled)
    elif topic_type == "custom" and custom_topic:
        return await run_custom_roundtable(tts_enabled, custom_topic)
    elif topic_type == "essential" and custom_topic:
        return await run_essential_roundtable(tts_enabled, custom_topic)
    else:
        # Default to government jobs
        return await run_government_jobs_roundtable(tts_enabled)


def get_voice_for_character(speaker_name):
    """Map character names to voice IDs."""
    voice_map = {
        "Alex Thompson": "en-US-Standard-A",
        "Sarah Chen": "en-US-Standard-B", 
        "Marcus Rodriguez": "en-US-Standard-C",
        "Emily Davis": "en-US-Standard-D",
        "Expert Analyst": "en-US-Standard-A",
        "Research Specialist": "en-US-Standard-B",
        "Industry Professional": "en-US-Standard-C", 
        "Enthusiast": "en-US-Standard-D",
        "Dr. Sarah Chen": "en-US-Standard-B",
        "Prof. Marcus Williams": "en-GB-Standard-A",
        "Dr. Elena Rodriguez": "es-ES-Standard-A",
        "James Thompson": "en-US-Standard-C"
    }
    return voice_map.get(speaker_name, "en-US-Standard-A")


def speak_text(text, voice):
    """Generate TTS audio and return filename."""
    try:
        import edge_tts
        import uuid
        
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        output_path = os.path.join("static", filename)
        
        communicate = edge_tts.Communicate(text, voice)
        communicate.save(output_path)
        
        return filename
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def parse_responses(text):
    text = text.strip()

    # Case 1: Already valid JSON
    try:
        return json.loads(text)
    except:
        pass

    # Case 2: Extract JSON from inside wrappers / partial output
    start = text.find("[")
    end = text.rfind("]")
    if start != -1:
        candidate = text[start:end + 1] if end != -1 else text[start:] + "]"
        # Remove trailing commas before ] or }
        candidate = re.sub(r",\s*(\]|\})", r"\1", candidate)
        try:
            return json.loads(candidate)
        except:
            pass

    raise RuntimeError(f"Groq returned invalid JSON:\n{text}")


def normalize_responses(data, characters):
    """Ensure each entry has 'speaker' and 'message' keys and map to known characters."""
    if not isinstance(data, list):
        return []

    normalized = []
    used_speakers = set()

    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            continue

        speaker = entry.get("speaker") or entry.get("name") or entry.get("character")
        message = entry.get("message") or entry.get("text") or entry.get("content")

        if not speaker and idx < len(characters):
            speaker = characters[idx]["name"]

        if not speaker or not message:
            continue

        normalized.append({"speaker": speaker, "message": message})
        used_speakers.add(speaker)

    # Fill missing speakers with a short placeholder to keep flow stable
    for c in characters:
        if c["name"] not in used_speakers:
            normalized.append({"speaker": c["name"], "message": "Let's continue."})

    # Keep exactly one entry per character in same order
    final = []
    for c in characters:
        for entry in normalized:
            if entry["speaker"] == c["name"]:
                final.append(entry)
                break

    return final


def attach_accents(data, characters):
    for entry in data:
        entry.setdefault("accent", "default")
        for c in characters:
            if c["name"] == entry["speaker"]:
                entry["accent"] = c["accent"]
    return data


async def run_essential_roundtable(tts_enabled=True, essential_topic=""):
    """
    Run a 40-minute essential topic roundtable with 4 expert speakers.
    
    Args:
        tts_enabled: Enable text-to-speech
        essential_topic: The essential topic provided by the user
    """
    topic = essential_topic
    # Essential topic specialists
    characters = [
        {"name": "Dr. Sarah Chen", "role": "Lead Researcher", "accent": "en-US"},
        {"name": "Prof. Marcus Williams", "role": "Industry Expert", "accent": "en-GB"},
        {"name": "Dr. Elena Rodriguez", "role": "Policy Analyst", "accent": "es-ES"},
        {"name": "James Thompson", "role": "Public Advocate", "accent": "en-US"}
    ]
    
    turns = []
    MAX_ESSENTIAL_TURNS = 16  # More turns for 40-minute discussion

    intro = (
        f"Welcome to this Essential Topics Deep Dive on {topic}. "
        "I'm your moderator, and today we have four distinguished experts: "
        "Dr. Sarah Chen, our lead researcher; Professor Marcus Williams, industry expert; "
        "Dr. Elena Rodriguez, policy analyst; and James Thompson, public advocate. "
        "We'll be exploring this critical topic from multiple perspectives over the next 40 minutes."
    )

    # Generate the extended discussion
    for i in range(MAX_ESSENTIAL_TURNS):
        if i == 0:
            prompt = f"""Create a comprehensive 40-minute roundtable discussion about "{topic}" with 4 expert speakers: Dr. Sarah Chen (Lead Researcher), Prof. Marcus Williams (Industry Expert), Dr. Elena Rodriguez (Policy Analyst), and James Thompson (Public Advocate).

This is an essential topic that everyone should understand. Each speaker should provide deep, expert insights with detailed explanations, real-world examples, and practical implications.

Return your response as a JSON array with this format:
[
    {{"speaker": "Dr. Sarah Chen", "message": "Detailed research-based insights with data and evidence (3-4 sentences)"}},
    {{"speaker": "Prof. Marcus Williams", "message": "Industry perspective with practical examples and market insights (3-4 sentences)"}},
    {{"speaker": "Dr. Elena Rodriguez", "message": "Policy analysis with regulatory and societal implications (3-4 sentences)"}},
    {{"speaker": "James Thompson", "message": "Public advocacy perspective with impact on everyday people (3-4 sentences)"}}
]

Make responses comprehensive and educational."""

        elif i < 6:
            prompt = f"""Continue the essential topic discussion on "{topic}" with the same 4 experts.

Each speaker should:
- Build upon previous points with deeper analysis
- Provide specific examples and case studies
- Address different aspects of topic
- Keep responses detailed (3-4 sentences)

Return as JSON array:
[
    {{"speaker": "Dr. Sarah Chen", "message": "research insights"}},
    {{"speaker": "Prof. Marcus Williams", "message": "industry perspective"}},
    {{"speaker": "Dr. Elena Rodriguez", "message": "policy analysis"}},
    {{"speaker": "James Thompson", "message": "public impact"}}
]"""

        elif i < 12:
            prompt = f"""Continue the essential topic discussion on "{topic}" with deeper exploration.

Each speaker should:
- Address challenges and solutions
- Discuss future implications
- Provide actionable insights
- Consider global perspectives
- Keep responses detailed (3-4 sentences)

Return as JSON array:
[
    {{"speaker": "Dr. Sarah Chen", "message": "research insights"}},
    {{"speaker": "Prof. Marcus Williams", "message": "industry perspective"}},
    {{"speaker": "Dr. Elena Rodriguez", "message": "policy analysis"}},
    {{"speaker": "James Thompson", "message": "public impact"}}
]"""

        else:
            prompt = f"""Conclude the essential topic discussion on "{topic}" with final insights.

Each speaker should:
- Summarize key takeaways
- Provide future outlook
- Offer practical advice for listeners
- End with thought-provoking insights
- Keep responses detailed (3-4 sentences)

Return as JSON array:
[
    {{"speaker": "Dr. Sarah Chen", "message": "research insights"}},
    {{"speaker": "Prof. Marcus Williams", "message": "industry perspective"}},
    {{"speaker": "Dr. Elena Rodriguez", "message": "policy analysis"}},
    {{"speaker": "James Thompson", "message": "public impact"}}
]"""

        response = await call_groq([
            {"role": "system", "content": "You are facilitating an essential educational roundtable discussion with 4 world experts. ALWAYS return your response as a valid JSON array with exact format specified. Do not include any explanations or text outside the JSON array."},
            {"role": "user", "content": prompt},
        ])

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

    return {
        "topic": topic,
        "turns": turns,
        "is_essential": True,
        "duration_minutes": 40
    }


async def run_custom_roundtable(tts_enabled=True, custom_topic=""):
    """
    Run a roundtable discussion on a custom topic.
    
    Args:
        tts_enabled: Enable text-to-speech
        custom_topic: The custom topic provided by the user
    """
    topic = custom_topic
    characters = CHARACTERS  # Use default characters for custom topics
    turns = []

    intro = (
        f"Welcome to the AI Roundtable. Today we discuss {topic}. "
        "Our panel includes an Expert Analyst, a Research Specialist, an Industry Professional, and an Enthusiast."
    )

    # Generate the discussion
    for i in range(MAX_TURNS):
        if i == 0:
            prompt = f"""Create a roundtable discussion about "{topic}" with 4 speakers: Expert Analyst, Research Specialist, Industry Professional, and Enthusiast.

Each person should provide their unique perspective on {topic}. Make it engaging and informative.

Return your response as a JSON array with this format:
[
    {{"speaker": "Expert Analyst", "message": "Detailed analysis and insights about {topic}"}},
    {{"speaker": "Research Specialist", "message": "Research-based perspective on {topic}"}},
    {{"speaker": "Industry Professional", "message": "Industry insights and practical applications of {topic}"}},
    {{"speaker": "Enthusiast", "message": "Enthusiastic take on {topic} with real-world examples"}}
]

Keep responses concise but insightful (2-3 sentences each)."""

        else:
            prompt = f"""Continue the roundtable discussion about "{topic}" with the same 4 speakers.

Build upon the previous points. Each speaker should:
- React to what others said
- Add new insights or ask questions
- Keep responses concise (2-3 sentences each)

Return your response as a JSON array with this format:
[
    {{"speaker": "Expert Analyst", "message": "Detailed analysis and insights about {topic}"}},
    {{"speaker": "Research Specialist", "message": "Research-based perspective on {topic}"}},
    {{"speaker": "Industry Professional", "message": "Industry insights and practical applications of {topic}"}},
    {{"speaker": "Enthusiast", "message": "Enthusiastic take on {topic} with real-world examples"}}
]"""

        response = await call_groq([
            {"role": "system", "content": "You are facilitating an engaging roundtable discussion with 4 experts discussing various perspectives on a topic. Always return your response as a valid JSON array."},
            {"role": "user", "content": prompt},
        ])

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

    return {
        "topic": topic,
        "turns": turns,
    }


# Legacy functions for backward compatibility
async def run_government_jobs_roundtable(tts_enabled=True):
    """Legacy function - use run_roundtable with topic_type='government_jobs' instead."""
    return await run_roundtable(tts_enabled, "government_jobs")

def build_government_jobs_prompt():
    """Build the initial prompt for government jobs discussion."""
    return """Create a roundtable discussion about government jobs with 4 speakers: Alex Thompson (HR Manager), Sarah Chen (Career Coach), Marcus Rodriguez (Hiring Manager), and Emily Davis (Policy Expert).

Each person should provide their unique perspective on government careers. Make it engaging and informative.

Return your response as a JSON array with this format:
[
    {"speaker": "Alex Thompson", "message": "HR perspective on government careers"},
    {"speaker": "Sarah Chen", "message": "Career coaching insights"},
    {"speaker": "Marcus Rodriguez", "message": "Hiring manager perspective"},
    {"speaker": "Emily Davis", "message": "Policy expert analysis"}
]

Keep responses concise but insightful (2-3 sentences each)."""

def build_government_jobs_system_prompt():
    """Build the system prompt for government jobs discussion."""
    return "You are facilitating an engaging roundtable discussion with 4 experts discussing government careers. Always return your response as a valid JSON array."
