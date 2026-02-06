#!/bin/bash
cd /home/vikki/AllCanLearn-v4
source venv/bin/activate
source .env
export GROQ_API_KEY=$(grep GROQ_API_KEY .env | cut -d'=' -f2)
echo "Starting server with GROQ_API_KEY: ${GROQ_API_KEY:0:20}..."
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
echo "Server started on port 8000"
