# quiz_generator.py - Generate quiz questions for any topic using Groq

from app.groq_client import call_groq
import json
import re


async def generate_quiz_questions(topic: str, difficulty: str = "medium", num_questions: int = 5):
    """Generate quiz questions for any topic using Groq"""
    
    prompt = f"""You are a quiz game expert. Generate {num_questions} multiple choice questions about: {topic}
    
Difficulty level: {difficulty}

Format your response as a JSON array with this exact structure:
[
  {{
    "question": "What is...",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": 0,
    "explanation": "Brief explanation of the correct answer"
  }}
]

Make questions engaging, educational, and appropriate for the difficulty level.
Return ONLY the JSON array, no other text."""

    messages = [
        {"role": "system", "content": "You are a quiz generator. Return only valid JSON."},
        {"role": "user", "content": prompt}
    ]
    
    response = await call_groq(messages)
    
    # Parse JSON response
    try:
        questions = json.loads(response)
    except json.JSONDecodeError:
        # If response is not valid JSON, try to extract it
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group())
        else:
            raise ValueError("Could not parse quiz questions from response")
    
    return questions


async def generate_topic_description(topic: str):
    """Generate a brief description for a topic"""
    
    prompt = f"""Write a brief 2-sentence description of the topic: {topic}
    
Make it engaging and educational. Just return the description text, nothing else."""

    messages = [
        {"role": "system", "content": "You are an educational content writer."},
        {"role": "user", "content": prompt}
    ]
    
    response = await call_groq(messages)
    return response.strip()
