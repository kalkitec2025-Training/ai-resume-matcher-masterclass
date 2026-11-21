import io
import os
import sqlite3
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from pypdf import PdfReader

load_dotenv()

DB_PATH = "analyzer.db"

app = FastAPI(title="AI Resume & Job-Match Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        match_score INTEGER NOT NULL,
        summary TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


init_db()


class MatchReport(BaseModel):
    match_score: int = Field(..., ge=0, le=100, description="Overall fit score from 0 to 100")
    summary: str = Field(..., description="2-3 sentence executive summary of candidate fit")
    matching_skills: list[str] = Field(..., description="Skills present in both resume and JD")
    missing_skills: list[str] = Field(..., description="Important JD skills missing from resume")
    interview_questions: list[str] = Field(..., description="5 tailored technical interview questions")


def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()
        if not text:
            raise ValueError("No readable text found in PDF.")
        return text
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")


def save_analysis(filename: str, report: MatchReport) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analysis_history (filename, match_score, summary) VALUES (?, ?, ?)",
        (filename, report.match_score, report.summary),
    )
    conn.commit()
    conn.close()


@app.get("/health")
def health_check():
    return {"status": "ok", "database": "sqlite_connected"}


@app.post("/analyze-text", response_model=MatchReport)
def analyze_text(
    resume_text: str = Form(...),
    job_description: str = Form(...),
):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing in .env")

    prompt = f"""You are a senior technical recruiter.
Analyze the candidate's resume text against the target job description objectively.

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{job_description}
"""
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MatchReport,
                temperature=0.2,
            ),
        )
        report = MatchReport.model_validate_json(response.text)
        save_analysis("text_input.txt", report)
        return report
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {exc}")


@app.post("/analyze-resume", response_model=MatchReport)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a valid PDF file.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing in .env")

    file_bytes = await resume.read()
    resume_text = extract_pdf_text(file_bytes)

    prompt = f"""You are a senior technical recruiter.
Analyze the candidate's resume against the target job description.
Be objective, practical, and specific.

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{job_description}
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MatchReport,
                temperature=0.2,
            ),
        )
        report = MatchReport.model_validate_json(response.text)
        save_analysis(resume.filename, report)
        return report
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {exc}")


@app.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, match_score, summary, created_at FROM analysis_history ORDER BY id DESC LIMIT 10"
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"records": rows}
