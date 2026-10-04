import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="JobAI API")

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "sql_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

api_key = os.getenv("GEMINI_API_KEY")
ai_client = genai.Client(api_key=api_key)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Backend, SQLite Database, and AI Service connected successfully!"
    }

@app.post("/api/generate")
def generate_ai_response(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
    try:
        ai_response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=req.prompt,
        )
        response_text = ai_response.text

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prompts_history (prompt, response) VALUES (?, ?)",
            (req.prompt, response_text)
        )
        conn.commit()
        conn.close()

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))