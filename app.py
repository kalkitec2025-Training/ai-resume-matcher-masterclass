# Python Full Stack with AI — Live Masterclass Backend
# We will build our FastAPI + SQLite + Gemini AI endpoints here!

from fastapi import FastAPI

app = FastAPI(title="AI Resume & Job-Match Analyzer")


@app.get("/health")
def health_check():
    return {"status": "ready", "message": "FastAPI server is running!"}
