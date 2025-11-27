import os
from supabase import create_client, Client
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_audio_to_supabase(file_path: str, file_name: str) -> str:
    """
    Upload an audio file to Supabase Storage.
    
    Args:
        file_path: Local path to the audio file
        file_name: Name to use for the file in storage
        
    Returns:
        Public URL of the uploaded file
    """
    try:
        # Read the binary data from the file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Upload to the audio-commentary bucket
        bucket_name = "audio-commentary"
        response = supabase.storage.from_(bucket_name).upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": "audio/mpeg"}
        )
        
        # Get the public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        
        print(f"✅ Audio uploaded successfully: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"❌ Error uploading audio to Supabase: {e}")
        raise


def save_recording(
    user_id: str,
    pgn: str,
    audio_url: str,
    white_player: Optional[str] = None,
    black_player: Optional[str] = None
) -> dict:
    """
    Save recording metadata to the recordings table.
    
    Args:
        user_id: Clerk User ID
        pgn: The PGN string of the game
        audio_url: Public URL of the audio file
        white_player: Name of the white player (optional)
        black_player: Name of the black player (optional)
        
    Returns:
        The inserted record
    """
    try:
        data = {
            "user_id": user_id,
            "pgn": pgn,
            "audio_url": audio_url,
            "player_white": white_player,
            "player_black": black_player
        }
        
        response = supabase.table("recordings").insert(data).execute()
        
        print(f"✅ Recording saved to database: {response.data}")
        return response.data[0] if response.data else {}
        
    except Exception as e:
        print(f"❌ Error saving recording to database: {e}")
        raise


def get_user_recordings(user_id: str) -> list:
    """
    Fetch all recordings for a specific user from the database.
    
    Args:
        user_id: Clerk User ID
        
    Returns:
        List of recording dictionaries
    """
    try:
        response = supabase.table("recordings").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        print(f"✅ Fetched {len(response.data)} recordings for user {user_id}")
        return response.data
        
    except Exception as e:
        print(f"❌ Error fetching recordings from database: {e}")
        return []
