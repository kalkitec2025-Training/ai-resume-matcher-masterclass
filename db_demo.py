# Section 3: Introduction to Database Connectivity (Completed)

import sqlite3

# 1. Connect to SQLite database file (creates analyzer.db automatically if not present)
conn = sqlite3.connect("analyzer.db")
cursor = conn.cursor()

# 2. Create table using SQL
cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    match_score INTEGER NOT NULL,
    summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 3. Insert a sample record safely using parameterized query (?)
cursor.execute(
    "INSERT INTO analysis_history (filename, match_score, summary) VALUES (?, ?, ?)",
    ("sample_resume.pdf", 82, "Strong Python & FastAPI foundation; add Docker and cloud experience.")
)
conn.commit()

# 4. Query all saved records
cursor.execute("SELECT id, filename, match_score, summary, created_at FROM analysis_history")
rows = cursor.fetchall()

print("=== Saved Records in SQLite Database ===")
for row in rows:
    print(row)

conn.close()
