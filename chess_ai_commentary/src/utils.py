import os
import torch
import google.generativeai as genai
from stockfish import Stockfish
from TTS.api import TTS
from pathlib import Path
import requests

# We need to import the config to get the API key for initialization
from src.config import GEMINI_API_KEY, STOCKFISH_PATH, DEVICE, TTS_MODEL_NAME

# This is your SAMPLE_GAMES dictionary, now stored in utils
SAMPLE_GAMES = {
    "quick_test": '''[Event "Quick Test"]
[Site "Testing"]
[Date "2024.09.19"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 1-0''',

    "scholars_mate": '''[Event "Scholar's Mate Example"]
[Site "Tutorial"]
[Date "2024.09.19"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0''',

    "immortal_game": '''[Event "Immortal Game"]
[Site "London"]
[Date "1851.06.21"]
[White "Adolf Anderssen"]
[Black "Lionel Kieseritzky"]
[Result "1-0"]

1. e4 e5 2. f4 exf4 3. Bc4 Qh4+ 4. Kf1 b5 5. Bxb5 Nf6 6. Nf3 Qh6 7. d3 Nh5 8. Nh4 Qg5 9. Nf5 c6 10. g4 Nf6 11. Rg1 cxb5 12. h4 Qg6 13. h5 Qg5 14. Qf3 Ng8 15. Bxf4 Qf6 16. Nc3 Bc5 17. Nd5 Qxb2 18. Bd6 Bxg1 19. e5 Qxa1+ 20. Ke2 Na6 21. Nxg7+ Kd8 22. Qf6+ Nxf6 23. Be7# 1-0'''
}

print("✅ Utility functions and sample games loaded.")

def setup_environment():
    """Checks for GPU availability and prints system info."""
    print("\n1. Checking system environment...")
    # Use the DEVICE from our config file
    print(f"✅ Device set to: {DEVICE.upper()} (from config)")
    print(f"🐍 PyTorch version: {torch.__version__}")
    return DEVICE

def initialize_tts_model(model_name=TTS_MODEL_NAME, device=DEVICE):
    """Loads the Coqui TTS model with a compatibility patch for PyTorch."""
    
    print("\n2. Initializing Coqui TTS model...")
    try:
        # --- START: Robust PyTorch Patch ---
        original_load = torch.load
        
        def patched_load(*args, **kwargs):
            kwargs['weights_only'] = False
            return original_load(*args, **kwargs)
        
        torch.load = patched_load
        # --- END: Robust PyTorch Patch ---

        # Load the TTS model
        tts = TTS(model_name).to(device)

        # --- IMPORTANT: Restore the original torch.load function ---
        torch.load = original_load
        
        print("✅ Coqui TTS model loaded successfully!")
        return tts
        
    except Exception as e:
        print(f"⚠️ TTS model loading failed: {e}")
        print("   If this is a 'module' error, try deleting the model folder and re-downloading.")
        return None

def initialize_services():
    """Initializes and configures Stockfish and Gemini from config."""
    print("\n3. Initializing Stockfish & Gemini...")
    
    # Stockfish is initialized in the ChessAnalyzer class,
    # but we can check the path here.
    if STOCKFISH_PATH and os.path.exists(STOCKFISH_PATH):
        print("✅ Stockfish path is valid.")
    else:
        print(f"❌ Stockfish path is INVALID: {STOCKFISH_PATH}")

    # Gemini was already configured when commentary_generator.py was imported
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
        print("✅ Google Gemini API is configured.")
    else:
        print("❌ Gemini API key is not set. Please check your .env file.")

def print_summary(tts_model):
    """Prints a final summary of the setup status."""
    print("\n" + "="*25)
    print("🚀 SETUP SUMMARY 🚀")
    print("="*25)
    print(f"🎵 TTS Model: {'✅ Loaded' if tts_model else '❌ Failed'}")
    print(f"♟️  Stockfish: {'✅ Path OK' if STOCKFISH_PATH and os.path.exists(STOCKFISH_PATH) else '❌ Path Invalid'}")
    print(f"💎 Gemini API: {'✅ Set' if GEMINI_API_KEY and 'your_gemini_api_key' not in GEMINI_API_KEY else '❌ Not Set'}")
    print("="*25)

def get_pgn_source():
    """
    Interactively prompts the user to select a PGN source.
    Returns the PGN data (str) and its type ('file', 'sample', 'direct', or None).
    """
    print("\n" + "-"*30)
    print("🎯 Please choose a PGN source for analysis:")
    print("   1. Use a built-in sample game")
    print("   2. Load a PGN file (from 'input/pgn_files/')")
    print("   3. Paste PGN text directly")
    choice = input(">> Enter your choice (1/2/3): ").strip()

    # Option 1: Use sample game
    if choice == '1':
        games = list(SAMPLE_GAMES.keys())
        print("\n📋 Available sample games:")
        for i, name in enumerate(games, 1): 
            print(f"   {i}. {name}")
        try:
            game_choice = int(input(f"\n>> Select a game (1-{len(games)}): ")) - 1
            if 0 <= game_choice < len(games):
                selected_game_name = games[game_choice]
                print(f"✅ Selected sample: {selected_game_name}")
                return SAMPLE_GAMES[selected_game_name], selected_game_name
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return None, None

    # Option 2: Load from file
    elif choice == '2':
        # Path is relative to the project root
        pgn_dir = "input/pgn_files" 
        if not os.path.exists(pgn_dir) or not os.listdir(pgn_dir):
            print(f"❌ No files found. Please place your .pgn files in the '{pgn_dir}' directory.")
            return None, None
        
        files = [f for f in os.listdir(pgn_dir) if f.lower().endswith('.pgn')]
        if not files:
            print(f"❌ No .pgn files found in '{pgn_dir}'.")
            return None, None
            
        print("\n📋 Available files:")
        for i, name in enumerate(files, 1): 
            print(f"   {i}. {name}")
        
        try:
            file_choice = int(input(f"\n>> Select a file (1-{len(files)}): ")) - 1
            if 0 <= file_choice < len(files):
                file_path = os.path.join(pgn_dir, files[file_choice])
                print(f"✅ Selected file: {files[file_choice]}")
                # We return the *content* of the file, not the path
                with open(file_path, 'r') as f:
                    pgn_content = f.read()
                return pgn_content, files[file_choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return None, None

    # Option 3: Paste PGN text
    elif choice == '3':
        print("\n📝 Paste your PGN text below. Press Enter on an empty line to finish.")
        lines = []
        while True:
            line = input()
            if line == "": 
                break
            lines.append(line)
        pgn_text = "\n".join(lines)
        if pgn_text.strip():
            print("✅ PGN text received.")
            return pgn_text, "direct paste"
        else:
            print("❌ No PGN text entered.")
            return None, None

    print("❌ Invalid choice.")
    return None, None

DEFAULT_VOICE_PATH = "models/voice_samples/default_voice.wav"

def setup_default_voice():
    """Checks for the default voice file and downloads it if it's missing."""

    # Check if the file already exists
    if not os.path.exists(DEFAULT_VOICE_PATH):
        print(f"Default voice not found at {DEFAULT_VOICE_PATH}. Downloading...")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(DEFAULT_VOICE_PATH), exist_ok=True)

        # A high-quality sample from the official Coqui TTS GitHub repo
        url = "https://github.com/coqui-ai/TTS/raw/dev/tests/data/ljspeech/wavs/LJ001-0001.wav"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for bad status codes
            with open(DEFAULT_VOICE_PATH, 'wb') as f:
                f.write(response.content)
            print(f"✅ Default voice downloaded and saved to {DEFAULT_VOICE_PATH}")
        except Exception as e:
            print(f"❌ Failed to download default voice: {e}")
            return False
    else:
        print(f"✅ Default voice found at {DEFAULT_VOICE_PATH}.")

    return True