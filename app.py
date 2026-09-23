from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "placement360.db"


# -----------------------------
# DATABASE
# -----------------------------

def init_db():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applicants (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            education TEXT,

            experience REAL,

            skills TEXT,

            score INTEGER,

            created_at TEXT

        )
    """)

    conn.commit()

    conn.close()


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# ANALYZE APPLICATION
# -----------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    name = data.get("name", "")
    email = data.get("email", "")
    education = data.get("education", "")
    skills = data.get("skills", "")
    experience = data.get("experience", 0)

    score = 0

    if name:
        score += 10

    if email:
        score += 10

    if education:
        score += 20

    if skills:
        score += 30

    try:

        experience = float(experience)

        score += min(experience * 10, 30)

    except (ValueError, TypeError):

        experience = 0

    score = min(round(score), 100)


    # SAVE APPLICATION

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applicants
        (name, email, education, experience, skills, score, created_at)

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        email,
        education,
        experience,
        skills,
        score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()

    conn.close()


    return jsonify({

        "name": name,

        "email": email,

        "education": education,

        "skills": skills,

        "experience": experience,

        "score": score

    })


# -----------------------------
# DASHBOARD
# -----------------------------

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
        SELECT * FROM applicants
        ORDER BY id DESC
    """)

    applicants = cursor.fetchall()


    cursor.execute("""
        SELECT COUNT(*) FROM applicants
    """)

    total = cursor.fetchone()[0]


    cursor.execute("""
        SELECT AVG(score) FROM applicants
    """)

    average = cursor.fetchone()[0]


    conn.close()


    if average is None:

        average = 0


    return render_template(

        "dashboard.html",

        applicants=applicants,

        total=total,

        average=round(average, 1)

    )


# -----------------------------
# RUN SERVER
# -----------------------------

if __name__ == "__main__":

    init_db()

    app.run(debug=True)