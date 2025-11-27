import os

# Define the project structure
project_structure = {
    'notebooks': [],
    'engines/stockfish': [],
    'input/pgn_files': [],
    'input/fen_files': [],
    'input/videos/game_recordings': [],
    'output/audio': [],
    'output/text': [],
    'output/combined/final_videos': [],
    'src': ['__init__.py'],
    'models/tts_models': [],
    'models/voice_samples': [],
    'models/model_configs': [],
    'config': [],
    'tests/sample_data': [],
    'docs': []
}

# Create the project directory
project_name = "chess_ai_commentary"
base_path = os.path.join(os.getcwd(), project_name)

print(f"Creating project structure at: {base_path}")

# Create directories
for dir_path, files in project_structure.items():
    full_path = os.path.join(base_path, dir_path)
    os.makedirs(full_path, exist_ok=True)
    print(f"✅ Created: {dir_path}")
    
    # Create files if specified
    for file_name in files:
        file_path = os.path.join(full_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                if file_name == '__init__.py':
                    f.write('# Chess AI Commentary Package\n')
            print(f"   📄 Created: {file_name}")

# Create main files
main_files = {
    'requirements.txt': '''chess
python-chess
stockfish
google-generativeai
TTS
pydub
pygame
torch
numpy
pandas
python-dotenv
''',
    'README.md': '''# Chess AI Commentary System

An AI-powered chess game commentary system that converts PGN/FEN files into natural voice commentary.

## Features
- Stockfish chess analysis
- Google Gemini AI commentary generation  
- Coqui TTS high-quality voice synthesis
- Downloadable audio commentary

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Set up Stockfish path in config
3. Add Gemini API key
4. Run main_commentary.ipynb

## Usage
See notebooks/main_commentary.ipynb for examples.
''',
    '.env.example': '''# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Paths  
STOCKFISH_PATH=engines/stockfish/stockfish

# Settings
TTS_DEVICE=cpu
COMMENTARY_STYLE=professional
''',
    '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Jupyter
.ipynb_checkpoints/

# Models and cache
models/tts_models/
*.pth
*.pt

# Output files
output/audio/*.wav
output/audio/*.mp3
output/text/*.txt

# Config with secrets
.env
config/settings.json

# OS
.DS_Store
Thumbs.db
'''
}

# Create main files
for filename, content in main_files.items():
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created: {filename}")

print(f"\n🎉 Project structure created successfully!")
print(f"📁 Project location: {base_path}")
print(f"\n📝 Next steps:")
print(f"1. cd {project_name}")
print(f"2. Copy your stockfish executable to engines/stockfish/")
print(f"3. Open notebooks/main_commentary.ipynb in Jupyter")
print(f"4. Install requirements: pip install -r requirements.txt")