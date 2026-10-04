# create_db.py
import sqlite3
import os

DB = "career_expert_system.db"

def create_db():
    if os.path.exists(DB):
        print(f"Removing existing {DB} for a fresh start.")
        os.remove(DB)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        stage TEXT NOT NULL  -- 'highschool' or 'university' or 'graduate'
    )
    """)

    # Careers table
    cur.execute("""
    CREATE TABLE careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career TEXT NOT NULL,
        description TEXT
    )
    """)

    # Career rules table: one row per career per stage (highschool/university)
    cur.execute("""
    CREATE TABLE career_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career_id INTEGER NOT NULL,
        stage TEXT NOT NULL,             -- 'highschool' or 'university'
        education_level TEXT,            -- comma separated acceptable degrees for uni (e.g. 'BSc,Masters')
        subjects TEXT,                   -- comma-separated required/important subjects
        skills TEXT,                     -- comma-separated required/important skills
        interests TEXT,                  -- comma-separated related interests
        min_cgpa REAL,                   -- optional threshold for uni rows
        FOREIGN KEY (career_id) REFERENCES careers(id)
    )
    """)

    # Store user choices for analytics
    cur.execute("""
    CREATE TABLE user_choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        stage TEXT,
        subjects TEXT,
        subject_grades TEXT,  -- format subject:grade,subject:grade
        skills TEXT,
        interests TEXT,
        education_level TEXT,
        cgpa REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created:", DB)

if __name__ == "__main__":
    create_db()
