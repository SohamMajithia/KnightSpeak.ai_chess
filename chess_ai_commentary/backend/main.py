import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import chessdotcom
import requests

# Import database functions
from database import upload_audio_to_supabase, save_recording ,get_user_recordings



# --- Path Hack & Imports (Same as before) ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config import STOCKFISH_PATH, DEVICE, TTS_MODEL_NAME
from src.utils import initialize_tts_model
from src.chess_analyzer import ChessAnalyzer
from src.commentary_generator import CommentaryGenerator
from src.voice_generator import VoiceGenerator
from src.pipeline import ChessCommentaryPipeline

APP_USER_AGENT = "Chess AI Commentary Project v0.1 (Contact: your_email@example.com)"
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server starting up...")
    chessdotcom.Client.request_config["headers"]["User-Agent"] = APP_USER_AGENT
    
    print("Loading AI models...")
    tts = initialize_tts_model(model_name=TTS_MODEL_NAME, device=DEVICE)
    analyzer = ChessAnalyzer(STOCKFISH_PATH)
    commentary_gen = CommentaryGenerator()
    voice_gen = VoiceGenerator(tts)
    
    ml_models["pipeline"] = ChessCommentaryPipeline(analyzer, commentary_gen, voice_gen)
    print("✅ AI Pipeline loaded and ready!")
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

# --- CORS (Same as before) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Serve Audio Files ---
# This makes files in 'output/audio' accessible at 'http://localhost:8000/audio/...'
# Ensure the directory exists first
os.makedirs("../output/audio", exist_ok=True)
app.mount("/audio", StaticFiles(directory="../output/audio"), name="audio")

class PgnModel(BaseModel):
    pgn: str
    language: str = "English"
    user_id: Optional[str] = None  # Clerk User ID
    player_white: Optional[str] = None
    player_black: Optional[str] = None

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Chess AI Backend Running"}

@app.get("/api/v1/recordings/{user_id}")
async def get_recordings(user_id: str):
    """
    Retrieve all recordings for a specific user.
    """
    try:
        recordings = get_user_recordings(user_id)
        return {"recordings": recordings}
    except Exception as e:
        print(f"❌ Error in get_recordings endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/games/archives/{username}")
async def get_game_archives(username: str):
    # ... (Keep your existing get_game_archives code here) ...
    # (Copy the code from our previous step)
    try:
        url = f"https://api.chess.com/pub/player/{username}/games/archives"
        headers = {"User-Agent": APP_USER_AGENT}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v1/games/by-month/{username}/{YYYY}/{MM}")
async def get_games_for_month(username: str, YYYY: str, MM: str):
    # ... (Keep your existing get_games_for_month code here) ...
    try:
        return chessdotcom.get_player_games_by_month(username, YYYY, MM).json
    except Exception as e:
        return {"error": str(e)}

# --- UPDATED: Synchronous Generation Endpoint with Supabase Integration ---
@app.post("/api/v1/generate-commentary")
async def generate_commentary(pgn_data: PgnModel):
    """
    Runs the pipeline AND WAITS for the result.
    Uploads to Supabase Storage and saves metadata to database.
    Returns the Supabase URL so the frontend can play it.
    """
    print(f"Received PGN. Starting synchronous generation...")
    
    pipeline = ml_models.get("pipeline")
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not loaded")
    
    # Run the pipeline (This will block for 30-60s, which is fine for this test)
    file_path = pipeline.run_pipeline_for_backend(pgn_data.pgn, pgn_data.language)
    
    if not file_path:
        raise HTTPException(status_code=500, detail="Generation failed")
    
    # Get the filename
    filename = os.path.basename(file_path)
    
    # Upload to Supabase Storage
    try:
        audio_url = upload_audio_to_supabase(file_path, filename)
        
        # Save metadata to database if user_id is provided
        if pgn_data.user_id:
            save_recording(
                user_id=pgn_data.user_id,
                pgn=pgn_data.pgn,
                audio_url=audio_url,
                white_player=pgn_data.player_white,
                black_player=pgn_data.player_black
            )
        
        # Return the Supabase URL
        return {
            "status": "complete",
            "audio_url": audio_url,
            "local_url": f"http://127.0.0.1:8000/audio/{filename}"  # Keep local URL as backup
        }
    except Exception as e:
        print(f"Error with Supabase upload: {e}")
        # Fallback to local URL if Supabase fails
        return {
            "status": "complete",
            "audio_url": f"http://127.0.0.1:8000/audio/{filename}",
            "error": "Supabase upload failed, using local storage"
        }


@app.get("/api/v1/recordings/{user_id}")
def get_user_recordings_route(user_id: str):
    """Fetch all recordings for a specific user from the database."""
    print(f"Fetching recordings for user: {user_id}")
    try:
        # Call the helper function from database.py
        recordings_data = get_user_recordings(user_id) 

        if "error" in recordings_data:
            raise HTTPException(status_code=500, detail=recordings_data["error"])

        return recordings_data

    except Exception as e:
        print(f"❌ Error fetching recordings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recordings.")