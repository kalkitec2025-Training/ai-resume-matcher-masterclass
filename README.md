# Python Full Stack with AI — Live Masterclass Starter Repo

Welcome! Please complete the **Pre-Session Setup Guide** before Sunday's live session:

1. **Create & activate virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your Gemini API Key:**
   - Copy `.env.example` to `.env`
   - Paste your free Google AI Studio key into `GEMINI_API_KEY=...`
4. **Verify readiness:**
   ```bash
   python verify_setup.py
   ```
