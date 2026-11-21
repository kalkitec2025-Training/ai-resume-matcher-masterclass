import os
import sqlite3
import sys
from dotenv import load_dotenv

load_dotenv()

print(f"1. Python Version: {sys.version.split()[0]} -> OK")
print(f"2. Built-in SQLite Version: {sqlite3.sqlite_version} -> OK")

try:
    import fastapi, pydantic, pypdf
    from google import genai
    print("3. Core Libraries (FastAPI, Pydantic, PyPDF, Google GenAI) -> OK")
except ImportError as e:
    print(f"3. Library Missing: {e}. Run: pip install -r requirements.txt")
    sys.exit(1)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key or "your_api_key" in api_key:
    print("4. API Key -> MISSING! Copy .env.example to .env and paste your GEMINI_API_KEY.")
    sys.exit(1)

print("4. API Key Loaded -> OK")
print("\nALL CHECKS PASSED! You are 100% ready for the Live MasterClass.")
