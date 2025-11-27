# Use Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for audio processing & stockfish)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
# Install PyTorch first (CPU version to save space, HF handles hardware)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure Stockfish is executable
# (Assuming you uploaded 'stockfish_linux' to the root of backend/)
RUN chmod +x stockfish_linux

# Create output directory for audio
RUN mkdir -p ../output/audio

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]