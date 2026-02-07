# models.py - Database models for AllCanLearn

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password_hash: str
    total_points: int = 0
    level: int = 1
    created_at: Optional[datetime] = None


class Topic(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    description: str
    podcast_generated: bool = False
    quiz_generated: bool = False
    plays_count: int = 0
    created_at: Optional[datetime] = None


class QuizScore(BaseModel):
    id: Optional[int] = None
    user_id: int
    topic_id: int
    score: int
    total_questions: int
    percentage: float
    time_taken: int
    completed_at: Optional[datetime] = None


class PodcastPlay(BaseModel):
    id: Optional[int] = None
    user_id: int
    topic_id: int
    episode_file: str
    completed: bool = False
    played_at: Optional[datetime] = None


class Leaderboard(BaseModel):
    rank: int
    username: str
    total_points: int
    level: int
    quizzes_completed: int
