import os
import platform
from dotenv import load_dotenv
from pathlib import Path

# --- Get the project's root directory ---
# This finds the directory where 'src' is (the backend root)
# On Local: .../chess_ai_commentary/backend
# On Cloud: /app
BACKEND_ROOT = Path(__file__).parent.parent

# --- Load the .env file ---
load_dotenv(BACKEND_ROOT / '.env')

print("🔄 Loading configuration...")

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY is not set.")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- SMART STOCKFISH PATH SELECTION ---
# Detect if we are on Windows or Linux (Cloud)
system_os = platform.system()

if system_os == "Windows":
    # Option A: If you moved stockfish.exe into backend/ (Recommended)
    STOCKFISH_BINARY = "stockfish.exe"
    
    # Option B: If stockfish.exe is still in the old engines folder
    # STOCKFISH_BINARY = "../engines/stockfish/stockfish.exe"
else:
    # Linux (Cloud) - File is always in the root of the app container
    STOCKFISH_BINARY = "stockfish_linux"

# Construct the full path
STOCKFISH_PATH = str(BACKEND_ROOT / STOCKFISH_BINARY)

# Verify it exists
if not os.path.exists(STOCKFISH_PATH):
    print(f"⚠️  WARNING: Stockfish not found at {STOCKFISH_PATH}")
    print(f"    Detected OS: {system_os}")
    print(f"    Expected File: {STOCKFISH_BINARY}")
else:
    # Make sure Linux binary is executable
    if system_os != "Windows":
        os.chmod(STOCKFISH_PATH, 0o755)

# --- Model Names ---
TTS_MODEL_NAME = "./tts_cache/tts_models--multilingual--multi-dataset--xtts_v2"

# --- System Settings ---
DEVICE = os.getenv("TTS_DEVICE", "cpu")

print("✅ Configuration loaded.")
print(f"   - OS Detected: {system_os}")
print(f"   - Stockfish Path: {STOCKFISH_PATH}")