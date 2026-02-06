# 🎯 AllCanLearn - Complete Architecture Guide

## 📁 Project Structure Overview

```
AllCanLearn/
├── app/                        # Backend application
│   ├── main.py                # FastAPI entry point (309 lines)
│   ├── moderator.py           # Roundtable manager (559 lines)
│   ├── groq_client.py         # AI API client (32 lines)
│   ├── tts_client.py          # Text-to-speech (71 lines)
│   ├── quiz_generator.py      # Quiz builder (62 lines)
│   ├── episodes.py            # Episode storage (116 lines)
│   ├── chat.py                # Chat manager (79 lines)
│   ├── chat_endpoints.py      # Chat API (59 lines)
│   ├── models.py              # Data structures (54 lines)
│   ├── cleanup.py             # File cleanup utility (35 lines)
│   ├── characters.py          # Default characters
│   ├── travel_characters.py   # Travel personas (90 lines)
│   ├── tech_startup_characters.py    # Tech personas (86 lines)
│   ├── personal_finance_characters.py # Finance personas (86 lines)
│   ├── mental_health_characters.py   # Mental health personas (86 lines)
│   └── static/
│       ├── index.html         # Main UI (990 lines)
│       ├── quiz.html          # Quiz interface (748 lines)
│       └── assets/sounds/
│           └── sounds.js      # Sound effects (191 lines)
├── venv/                      # Python virtual environment
├── tts_output/ → symlink     # Audio files (on Data drive)
├── episodes_data/ → symlink  # Saved episodes (on Data drive)
├── .env                      # API keys (NOT in git)
└── *.log → symlinks          # Application logs (on Data drive)
```

---

## 🏗️ Core Backend Architecture

### **app/main.py** - THE BRAIN (309 lines)
**Purpose:** FastAPI application entry point

**Key Responsibilities:**
- HTTP request/response handling
- Route definitions and endpoint management
- Static file serving
- WebSocket connection management
- CORS configuration

**Main Endpoints:**
```python
GET  /                          # Health check
POST /generate                  # Generate podcast episodes
POST /api/quiz/generate         # Generate quiz questions
GET  /api/topics/popular        # List available topics
GET  /tts_output/{filename}     # Serve audio files
WebSocket /ws/chat              # Real-time chat connection
POST /api/chat/send             # Send chat message
GET  /api/chat/history/{room}   # Get chat history
GET  /api/episodes              # List saved episodes
GET  /api/episodes/{id}         # Get specific episode
```

**Technology Stack:**
- FastAPI (async web framework)
- Uvicorn (ASGI server)
- WebSocket for real-time features
- Static file middleware

---

## 🎙️ Podcast Generation System

### **app/moderator.py** - ROUNDTABLE MANAGER (559 lines)
**Purpose:** Orchestrates AI roundtable discussions

**Key Functions:**
- `generate_tts_batch()` - Parallel TTS generation for all speakers
- `run_roundtable()` - Main discussion orchestrator
- `run_travel_roundtable()` - Travel-themed discussions
- `run_tech_startup_roundtable()` - Tech startup discussions
- `run_personal_finance_roundtable()` - Finance discussions
- `run_mental_health_roundtable()` - Mental health discussions

**Flow:**
1. Select character set based on topic
2. Loop MAX_TURNS times (default: 5 turns)
3. Each turn:
   - Call Groq API for AI-generated response
   - Maintain conversation context
   - Track speaker rotation
4. Generate TTS audio in parallel for all responses
5. Attach TTS URLs to each turn
6. Return complete discussion JSON

**Recent Fix:** TTS URL format now includes `/tts_output/` prefix for proper audio playback

### **Character System**
**app/characters.py** - Default (Government Jobs)
- Exam Strategist
- Serving Officer
- Fresh Qualifier
- Citizen

**app/travel_characters.py** (90 lines)
- Elena (Barcelona, Spanish accent)
- Fatima (Cairo, Middle Eastern accent)
- Priya (Mumbai, Indian accent)
- Carlos (Buenos Aires, Latin accent)

**app/tech_startup_characters.py** (86 lines)
- Founder
- VC Investor
- Lead Engineer
- Marketing Director

**app/personal_finance_characters.py** (86 lines)
- Financial Advisor
- Seasoned Investor
- Budget Coach
- College Student

**app/mental_health_characters.py** (86 lines)
- Psychologist
- Patient
- Therapist
- Advocate

---

## 🤖 AI & Voice Services

### **app/groq_client.py** - AI API CLIENT (32 lines)
**Purpose:** Interface with Groq LLM API

**Model:** llama-3.1-8b-instant
**Key Function:** `call_groq(prompt, max_tokens=150)`

**Configuration:**
- Uses GROQ_API_KEY from .env file
- Temperature: 0.7 (balanced creativity)
- Max tokens: 150 (concise responses)

**Error Handling:**
- Catches API failures
- Returns error messages for debugging
- Logs all requests/responses

### **app/tts_client.py** - TEXT-TO-SPEECH (71 lines)
**Purpose:** Generate audio from text

**Platform Support:**
- **Linux:** espeak-ng (generates .wav files)
  - Quality: 16kHz sample rate
  - Amplitude: 200 (enhanced volume)
  - Speed: 175 words/minute
- **macOS:** say command (generates .aiff files)

**Voice Mapping:**
```python
VOICE_MAPPING = {
    "Indian": "hi",      # Hindi voice
    "British": "en-gb",  # British English
    "American": "en-us", # American English
    "Spanish": "es",     # Spanish
    # ... more accents
}
```

**Output:** Returns filename only (path added by moderator.py)

---

## 📝 Quiz System

### **app/quiz_generator.py** - QUIZ BUILDER (62 lines)
**Purpose:** Generate educational quizzes using AI

**Function:** `generate_quiz(topic, difficulty="medium", num_questions=5)`

**Capabilities:**
- Custom topics (any subject)
- 3 difficulty levels: easy, medium, hard
- 1-10 questions per quiz
- Multiple choice format (4 options)
- Detailed explanations for each answer

**AI Prompt Engineering:**
- Structured JSON output format
- Contextual difficulty adjustment
- Educational explanations
- Variety in question types

### **app/static/quiz.html** - QUIZ UI (748 lines)
**Features:**
- Topic selection dropdown (50+ predefined topics)
- Custom topic input
- Difficulty selector
- Progress indicator
- Score tracking
- Answer explanations
- Retry functionality
- Leaderboard display

---

## 💬 Chat System

### **app/chat.py** - CHAT MANAGER (79 lines)
**Purpose:** Manage real-time chat sessions

**Data Structure:**
```python
chat_history = {
    "room_name": [
        {"user": "username", "message": "text", "timestamp": "..."},
        # ... up to 100 messages
    ]
}
```

**Features:**
- In-memory storage (100 messages per room)
- Multiple chat rooms support
- Message broadcasting
- Timestamp tracking
- Automatic history trimming

### **app/chat_endpoints.py** - CHAT API (59 lines)
**REST Endpoints:**
- POST `/api/chat/send` - Send message
- GET `/api/chat/history/{room}` - Retrieve history

**WebSocket Integration:**
- Real-time message delivery
- Connected client tracking
- Broadcast to all participants

---

## 📊 Data & Storage Management

### **app/episodes.py** - EPISODE STORAGE (116 lines)
**Purpose:** Persist generated podcast episodes

**Database:** SQLite (`data/db/episodes.db`)

**Schema:**
```sql
CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    turns JSON NOT NULL
);
```

**Functions:**
- `save_episode()` - Store new episode
- `get_episode(id)` - Retrieve by ID
- `list_episodes()` - Get all episodes
- `delete_old_episodes()` - Cleanup utility

### **app/models.py** - DATA STRUCTURES (54 lines)
**Purpose:** Pydantic models for type validation

**Models:**
```python
class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5

class ChatMessage(BaseModel):
    user: str
    message: str
    room: str = "default"

class Episode(BaseModel):
    id: Optional[int]
    topic: str
    turns: List[Dict]
    created_at: datetime
```

---

## 🌐 Frontend Architecture

### **app/static/index.html** - MAIN UI (990 lines)
**Type:** Single Page Application (SPA)

**Sections:**
1. **Home** - Welcome page with quick access
2. **Podcast** - Episode generation and playback
3. **Quiz** - Link to quiz interface
4. **Chat** - Real-time discussion room
5. **Library** - Saved episode browsing

**Features:**
- Sidebar navigation
- Sound effects toggle
- Responsive design (mobile/tablet/desktop)
- Dark theme
- Loading animations
- Error handling UI

**JavaScript Components:**
- Topic selection handler
- Podcast generation API calls
- Audio player management
- WebSocket chat client
- Episode library display

### **app/static/quiz.html** - QUIZ PAGE (748 lines)
**Features:**
- Standalone quiz interface
- 8 topic categories
- 50+ predefined topics
- Custom topic input
- Difficulty selection
- Question display
- Answer validation
- Score calculation
- Results summary
- Leaderboard

### **app/static/assets/sounds/sounds.js** - SOUND EFFECTS (191 lines)
**Purpose:** Interactive audio feedback

**Technology:** Web Audio API (synthesized sounds)

**Sounds:**
1. Water drop
2. Gentle chime
3. Wind chimes
4. Soft wave
5. Bell harmonics
6. Soft tick
7. Raindrop
8. Gentle breeze

**Features:**
- No external audio files (100% synthesized)
- Biquad filters for natural resonance
- Toggle control with localStorage persistence
- Auto-attach to all interactive elements
- Volume control

---

## 🔄 Data Flow Diagrams

### Podcast Generation Flow
```
User Action: Click "Generate Podcast"
    ↓
Frontend (index.html)
    ↓ POST /generate?topic=travel&tts=true
Backend (main.py)
    ↓
moderator.py
    ├─→ Select character set (travel_characters.py)
    ├─→ Loop 5 turns:
    │   ├─→ groq_client.py (AI response)
    │   └─→ Collect all responses
    └─→ Parallel TTS generation:
        ├─→ tts_client.py (speaker 1)
        ├─→ tts_client.py (speaker 2)
        ├─→ tts_client.py (speaker 3)
        └─→ tts_client.py (speaker 4)
    ↓
Return JSON: {topic, turns: [{speaker, message, tts}]}
    ↓
Frontend displays:
    ├─→ Conversation text
    └─→ Audio players for each turn
```

### Quiz Generation Flow
```
User Action: Enter topic + difficulty
    ↓
Frontend (quiz.html)
    ↓ POST /api/quiz/generate
Backend (main.py)
    ↓
quiz_generator.py
    ↓
groq_client.py (with quiz prompt)
    ↓
Return JSON: {questions: [{question, options, correct, explanation}]}
    ↓
Frontend displays interactive quiz
    ↓
User submits answers
    ↓
Calculate score + show explanations
```

### Chat Flow
```
User Action: Type message
    ↓
Frontend WebSocket client
    ↓ WebSocket /ws/chat
Backend (main.py)
    ├─→ chat.py (store in memory)
    └─→ Broadcast to all connected clients
    ↓
All users receive message in real-time
```

---

## 💾 Storage Architecture

### Symbolic Link Strategy
**Purpose:** Separate code from data, optimize storage usage

```
System Drive (/home/vikki/AllCanLearn/)
├── app/                    # Code (101MB)
├── venv/                   # Dependencies (~200MB)
├── .env                    # Configuration
├── tts_output/ → SYMLINK   # Points to Data drive
├── episodes_data/ → SYMLINK # Points to Data drive
└── *.log → SYMLINKS        # Points to Data drive

Data Drive (/media/vikki/Data/AllCanLearn_Storage/)
├── tts_output/             # Audio files (grows 50-100MB/month)
├── episodes_data/          # Saved episodes (~10MB)
└── logs/                   # Application logs (~5MB/month)
```

**Benefits:**
- Code stays on fast system drive
- Large files on spacious data drive
- Easy backup strategy
- No code changes needed

---

## 🌐 Network & Deployment

### Local Network
- **IP:** 192.168.1.138
- **Port:** 8000
- **Access:** http://192.168.1.138:8000

### Global Access (Cloudflare Tunnel)
- **URL:** https://dominant-jim-sheets-portraits.trycloudflare.com/ui
- **Type:** Free tier
- **Features:**
  - No port forwarding needed
  - HTTPS by default
  - Multi-region access
  - DDoS protection

### Systemd Services
**allcanlearn.service:**
```ini
[Service]
ExecStart=/home/vikki/AllCanLearn/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10s
```

**allcanlearn-tunnel.service:**
```ini
[Service]
ExecStart=/usr/local/bin/cloudflared tunnel --url http://localhost:8000
Requires=allcanlearn.service
Restart=always
```

**Features:**
- Auto-start on boot
- Auto-restart on crash
- 10-second delay between restarts
- Proper dependency management
- Centralized logging

### SSH Access
- **Host:** vikki@192.168.1.138
- **Auth:** Passwordless SSH key
- **Key:** ~/.ssh/id_ed25519
- **Setup:** ssh-copy-id completed

---

## 🔐 Security & Configuration

### Environment Variables (.env)
```
GROQ_API_KEY=your_groq_api_key_here
NGROK_AUTHTOKEN=your_ngrok_token_here
```

**Security:**
- Excluded from git (.gitignore)
- Never committed to GitHub
- Manually copied to deployment servers
- Required for app functionality

### CORS Configuration
```python
origins = ["*"]  # Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🛠️ Maintenance & Utilities

### **app/cleanup.py** - FILE CLEANUP (35 lines)
**Purpose:** Delete old TTS files to manage storage

**Features:**
- Configurable age threshold (default: 7 days)
- Safe deletion (checks file age)
- Logging of deleted files
- Can run via cron job

**Usage:**
```bash
python -m app.cleanup --days 7
```

### Monitoring & Logging
**Log Location:** `/media/vikki/Data/AllCanLearn_Storage/logs/allcanlearn.log`

**What's Logged:**
- API requests/responses
- TTS generation events
- Error messages and stack traces
- Podcast generation timing
- Quiz generation requests
- Chat messages (optional)

**Log Rotation:** Manual (recommend logrotate setup)

---

## 📈 Performance Metrics

### Response Times
- **Health check:** <10ms
- **Topic list:** <50ms
- **Quiz generation:** 3-8 seconds (AI dependent)
- **Podcast generation (no TTS):** 15-25 seconds
- **Podcast generation (with TTS):** 30-45 seconds
- **Chat message:** <100ms (real-time)

### Storage Growth
- **TTS files:** 0.5-2MB per speaker turn
- **Average podcast:** 10-20 TTS files = 10-30MB
- **Monthly estimate:** 50-100MB (10-15 podcasts)
- **Database:** ~1KB per episode metadata

### Concurrency
- **Max WebSocket connections:** ~100 (configurable)
- **Concurrent podcast generation:** 1 (serialized, AI API limitation)
- **Chat rooms:** Unlimited (in-memory)
- **TTS generation:** Parallel within single podcast

---

## 🚀 Future Enhancements

### Short Term
1. Database persistence for chat history
2. User authentication and profiles
3. TTS file caching (reuse common phrases)
4. Episode search functionality
5. Export episodes to audio file

### Medium Term
1. Real-time podcast streaming
2. Multiple language support
3. Voice cloning for consistent characters
4. Quiz difficulty auto-adjustment
5. Collaborative chat features

### Long Term
1. Mobile app (React Native)
2. Admin dashboard for content management
3. Analytics and usage tracking
4. Integration with learning management systems
5. AI-powered topic recommendations

---

## 📚 Key Dependencies

### Python Backend
```
fastapi>=0.104.0
uvicorn>=0.24.0
groq>=0.4.0
websockets>=12.0
pydantic>=2.0.0
python-dotenv>=1.0.0
aiofiles>=23.0.0
```

### System Requirements
- Python 3.10+
- espeak-ng (Linux TTS)
- SQLite 3
- 1GB RAM minimum
- 10GB storage recommended

### Frontend (No Build Required)
- Vanilla JavaScript (ES6+)
- Web Audio API
- WebSocket API
- Fetch API

---

## 🎯 Architecture Principles

1. **Separation of Concerns**
   - Backend: Business logic and data
   - Frontend: Presentation and interaction
   - Storage: Isolated on separate drive

2. **Async by Default**
   - FastAPI async handlers
   - Parallel TTS generation
   - Non-blocking WebSocket

3. **Fail-Safe**
   - Auto-restart services
   - Error logging
   - Graceful degradation

4. **Scalability**
   - Stateless API design
   - File-based storage (easy to migrate)
   - In-memory caching where appropriate

5. **Developer Experience**
   - Clear file organization
   - Consistent naming conventions
   - Comprehensive documentation
   - Easy local development

---

**Last Updated:** January 31, 2026
**Version:** 1.0
**Status:** Production-ready with 24/7 uptime
