# main.py

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from app.moderator import run_roundtable
from app.episodes import get_audio_files, add_episode, get_all_episodes
from app.cleanup import cleanup_old_audio_files
from app.quiz_generator import generate_quiz_questions, generate_topic_description
from app.chat import manager

load_dotenv()

# Use ORJSON for faster JSON serialization
app = FastAPI(
    title="AllCanLearn",
    description="Universal learning platform with AI podcasts and quizzes",
    default_response_class=ORJSONResponse
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression for faster response delivery
app.add_middleware(GZipMiddleware, minimum_size=1000)

logger = logging.getLogger(__name__)

# Create directories if they don't exist
os.makedirs("tts_output", exist_ok=True)
os.makedirs("episodes_data", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/tts_output", StaticFiles(directory="tts_output"), name="tts_output")

# Setup background scheduler for cleanup
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_audio_files, "cron", hour=2, minute=0)  # Daily at 2 AM
scheduler.start()

logger.info("✅ Cleanup scheduler started - runs daily at 2 AM")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate(tts: bool = True, topic: str = "government_jobs"):
    """
    Generate a roundtable episode.
    
    Args:
        tts: Enable text-to-speech (default: True)
        topic: Topic type - "government_jobs" or "travel" (default: "government_jobs")
    """
    try:
        logger.info(f"Generating episode: topic={topic}, tts={tts}")
        episode = await run_roundtable(tts_enabled=tts, topic_type=topic)
        
        # Store episode metadata
        episode_id = add_episode(episode["topic"], episode["turns"])
        logger.info(f"Episode created: {episode_id} - {episode['topic']}")
        
        return episode
    except Exception as e:
        logger.error(f"Error generating episode: {str(e)}", exc_info=True)
        raise


@app.get("/api/episodes")
def get_episodes():
    """Get all episodes - client-side caches for 5 minutes"""
    episodes = get_all_episodes()
    return {"episodes": episodes}


@app.get("/api/audio-files")
def get_audio_files_list():
    """Get list of all audio files"""
    return get_audio_files()


@app.get("/ui")
def serve_ui():
    """Serve the web UI"""
    return FileResponse("app/static/index.html", media_type="text/html")


@app.get("/quiz")
def serve_quiz():
    """Serve the quiz UI"""
    return FileResponse("app/static/quiz.html", media_type="text/html")


# ==================== QUIZ ENDPOINTS ====================

class GenerateQuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5


class SubmitQuizRequest(BaseModel):
    topic: str
    score: int
    total_questions: int
    time_taken: int


@app.post("/api/quiz/generate")
async def generate_quiz(request: GenerateQuizRequest):
    """Generate quiz questions for any topic"""
    try:
        logger.info(f"Generating quiz: {request.topic}, difficulty={request.difficulty}")
        
        questions = await generate_quiz_questions(
            topic=request.topic,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )
        
        description = await generate_topic_description(request.topic)
        
        return {
            "success": True,
            "topic": request.topic,
            "description": description,
            "difficulty": request.difficulty,
            "questions": questions,
            "total_questions": len(questions)
        }
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz/submit")
async def submit_quiz(request: SubmitQuizRequest):
    """Submit quiz score"""
    try:
        percentage = (request.score / request.total_questions) * 100
        points_earned = request.score * 20
        
        # TODO: Save to database when user system is added
        
        return {
            "success": True,
            "score": request.score,
            "total": request.total_questions,
            "percentage": round(percentage, 1),
            "points_earned": points_earned,
            "message": "Great job!" if percentage >= 70 else "Keep practicing!"
        }
    except Exception as e:
        logger.error(f"Error submitting quiz: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/topics/popular")
def get_popular_topics():
    """Get popular learning topics"""
    return {
        "categories": [
            {
                "name": "Technology",
                "icon": "💻",
                "topics": [
                    "Artificial Intelligence", "Cloud Computing", "Cybersecurity",
                    "Web Development", "Mobile Apps", "Blockchain", "Data Science"
                ]
            },
            {
                "name": "Science",
                "icon": "🔬",
                "topics": [
                    "Physics", "Chemistry", "Biology", "Astronomy",
                    "Climate Science", "Neuroscience", "Genetics"
                ]
            },
            {
                "name": "Business & Finance",
                "icon": "💼",
                "topics": [
                    "Entrepreneurship", "Stock Market", "Cryptocurrency",
                    "Marketing", "Economics", "Personal Finance", "Real Estate"
                ]
            },
            {
                "name": "Arts & Culture",
                "icon": "🎨",
                "topics": [
                    "Music Theory", "Painting", "Photography", "Film Making",
                    "Creative Writing", "Architecture", "Fashion Design"
                ]
            },
            {
                "name": "Sports & Fitness",
                "icon": "⚽",
                "topics": [
                    "Football", "Basketball", "Cricket", "Tennis",
                    "Fitness Training", "Yoga", "Nutrition"
                ]
            },
            {
                "name": "Life Skills",
                "icon": "🌱",
                "topics": [
                    "Cooking", "Gardening", "Public Speaking", "Time Management",
                    "Meditation", "Leadership", "Communication"
                ]
            },
            {
                "name": "Gaming",
                "icon": "🎮",
                "topics": [
                    "Minecraft Building", "Chess Strategies", "Esports",
                    "Game Design", "Speedrunning", "Streaming", "Game Development"
                ]
            },
            {
                "name": "Nature & Animals",
                "icon": "🐾",
                "topics": [
                    "Marine Biology", "Birds", "Farming", "Beekeeping",
                    "Wildlife Conservation", "Pet Care", "Aquariums"
                ]
            }
        ]
    }


@app.get("/api/leaderboard")
def get_leaderboard():
    """Get global leaderboard"""
    # Mock data for now
    return {
        "leaderboard": [
            {"rank": 1, "username": "LearningMaster", "points": 15420, "level": 32, "quizzes": 215},
            {"rank": 2, "username": "QuizGenius", "points": 12800, "level": 28, "quizzes": 180},
            {"rank": 3, "username": "TopicExplorer", "points": 11200, "level": 25, "quizzes": 165},
            {"rank": 4, "username": "KnowledgeSeeker", "points": 9800, "level": 22, "quizzes": 142},
            {"rank": 5, "username": "BrainPower", "points": 8500, "level": 19, "quizzes": 128}
        ]
    }




# ============= CHAT WEBSOCKET =============

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, username: str = "Anonymous"):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, username)
    
    await manager.send_personal_message({
        "type": "online_users",
        "users": manager.get_online_users(),
        "count": len(manager.active_connections)
    }, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "message",
                "username": username,
                "message": data,
                "timestamp": datetime.now().isoformat()
            }
            manager.add_to_history(message)
            await manager.broadcast(message)
            
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast({
                "type": "system",
                "message": f"{username} left the chat",
                "timestamp": datetime.now().isoformat(),
                "online_count": len(manager.active_connections)
            })


@app.get("/api/chat/online")
def get_online_users():
    """Get currently online users"""
    return {
        "users": manager.get_online_users(),
        "count": len(manager.active_connections)
    }
