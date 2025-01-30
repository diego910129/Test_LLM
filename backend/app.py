from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llm import llm_completion
import sqlite3
import os
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000", # Important: Add this line to include 127.0.0.1
    "http://127.0.0.1:5173" # Also add it for Vite if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Setup
DATABASE = 'completions.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            key INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completion TEXT NOT NULL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
async def startup_event():
    initialize_db()
    if not os.path.exists("hunspell_US.txt"):
        raise FileNotFoundError("hunspell_US.txt is missing from backend folder!")

@app.get("/completions")
def completion(text: str):
    print("text ===>   ", text) 
    if not text:
        raise HTTPException(status_code=400, detail="Input text is required.")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # fetch existing completions
    cursor.execute(
        "SELECT completion FROM completions WHERE text = ? ORDER BY last_updated DESC", (text,)
    )
    accepted_completions = [row['completion'] for row in cursor.fetchall()]
    print("accepted_completions ===> ", accepted_completions)
    conn.close()

    if text.endswith(" "):  # Sentence completion
        try:
            llm_results = llm_completion(text, 5)
            print("llm_results ===> ", llm_results)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error in LLM completion")
        if len(llm_results) < 5:
            raise HTTPException(status_code=500, detail="LLM could not produce 5 completions")
        filtered_results = [result for result in llm_results if result.strip()]
        completions = list(dict.fromkeys(accepted_completions + filtered_results))[:5]
    else:  # Word Completion
         
        with open('hunspell_US.txt', 'r') as f:
            dictionary = [line.strip().lower() for line in f.readlines()]

        filtered_results = [word for word in dictionary if word.startswith(text.lower())]
        completions = list(dict.fromkeys(accepted_completions + filtered_results))[:5]

    return {"suggestions": completions}


class CompletionRequest(BaseModel):
    text: str
    completion: str


@app.post("/completions")
def record_completion(request: CompletionRequest):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.now()
        cursor.execute(
            "INSERT INTO completions (text, completion, last_updated) VALUES (?, ?, ?)",
            (request.text, request.completion, now),
        )
        conn.commit()
        return {"message": "Completion recorded"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if conn:
            conn.close()


