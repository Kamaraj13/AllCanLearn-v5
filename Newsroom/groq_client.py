# groq_client.py

import os
import asyncio
import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"  # Back to working model


async def call_groq(messages, temperature=0.7, max_tokens=2048):
    """
    Call Groq API with optimized settings for high-quality podcast generation.
    
    Args:
        messages: List of message dictionaries
        temperature: Creativity level (0.7 for balanced quality)
        max_tokens: Maximum response length (2048 for detailed responses)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        async with httpx.AsyncClient(timeout=90) as client:  # Increased timeout
            res = await client.post(GROQ_URL, json=payload, headers=headers)
            res.raise_for_status()
            data = res.json()

        return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            # Rate limit handling
            await asyncio.sleep(2)
            return await call_groq(messages, temperature, max_tokens)
        else:
            raise
    except Exception as e:
        print(f"Groq API error: {e}")
        # Fallback with simpler settings
        payload["model"] = "llama-3.1-8b-instant"
        payload["max_tokens"] = 1024
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(GROQ_URL, json=payload, headers=headers)
            res.raise_for_status()
            data = res.json()
        return data["choices"][0]["message"]["content"]

