# ♟️ Knightspeaks: AI Chess Commentary

**Knightspeaks** is a full-stack web application that turns your chess games into exciting, professional audio commentary. It combines **Stockfish** for analysis, **Google Gemini** for charismatic narration, and **Coqui TTS** for lifelike voice synthesis.
## 📌 Project Overview
KnightSpeak.ai_chess is a full-stack AI-powered chess commentary web app that:
Analyzes game moves using Stockfish
Generates natural commentary using an LLM (Google Gemini)
Converts that commentary into lifelike audio (Coqui)
Presents results through a clean UI built with Next.js
This project was developed as part of a team, with all members contributing to its architecture, implementation, and deployment. The final working version is hosted on this GitHub for showcase purposes.
🚀🚀MY ROLE AND CONTRIBUTION:
I was the primary architect of the project and the owner of the core commentary pipeline. My responsibilities included:
Project ideation: Conceptualized the idea of an automated chess commentary system that converts raw gameplay into natural-sounding audio explanations.
System design: Designed the end-to-end pipeline from input to output, defining how PGN data flows through analysis, language generation, and audio synthesis stages.
PGN processing: Implemented logic to read, parse, and iterate through chess games from PGN files, extracting move-level information required for analysis.
Game evaluation: Integrated Stockfish to evaluate positions and generate quantitative assessments for each move.
Commentary generation: Designed prompts and data formatting to feed move context and engine evaluations into an LLM, generating human-like chess commentary.
Audio synthesis: Converted generated commentary into audio outputs, forming the final consumable narration layer.
Pipeline integration: Ensured seamless coordination between analysis, language generation, and audio modules to produce synchronized outputs.
This role required combining algorithmic thinking, AI integration, and system-level design, making the commentary pipeline the central component of the project.

## ✨ Features
* **Smart Analysis:** Deep move-by-move analysis using the Stockfish engine.
* **AI Commentary:** Generates exciting, sports-style commentary using Google Gemini.
* **Lifelike Voice:** Converts text to speech using the high-quality Coqui XTTS-v2 model.
* **Game History:** Automatically fetches your recent games from Chess.com.
* **Secure Auth:** User authentication and management via Clerk.
* **Modern UI:** A clean, responsive dashboard built with Next.js and Tailwind CSS.

---

## 🛠️ Project Structure

This project is divided into two main parts:

* **`backend/` (FastAPI):** The Python brain. Handles chess analysis, AI generation, and TTS.
* **`frontend/` (Next.js):** The user interface. Handles login, game fetching, and audio playback.

---

## 🚀 Setup Guide (Windows)

### Prerequisites
1.  **Python 3.10+** installed.
2.  **Node.js 18+** installed.
3.  **Stockfish Engine:** Download the **Windows** version and place the `stockfish.exe` file directly inside the `backend/` folder.
4.  **API Keys:**
    * Google Gemini API Key
    * Clerk Publishable Key & Secret Key

### Part 1: Backend Setup (Python)

1.  **Open Command Prompt (cmd) or PowerShell.**

2.  **Navigate to the backend folder:**
    ```powershell
    cd backend
    ```

3.  **Create and activate a virtual environment:**
    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```
    *(Note: If you have an NVIDIA GPU, ensure you install the CUDA version of PyTorch for faster processing).*

5.  **Configure Environment:**
    Create a file named `.env` inside the `backend/` folder and add your keys:
    ```ini
    GEMINI_API_KEY=your_gemini_key_here
    STOCKFISH_PATH=./stockfish.exe
    ```

6.  **Run the Server:**
    ```powershell
    uvicorn main:app --reload
    ```
    The backend will start at `http://127.0.0.1:8000`.

---

### Part 2: Frontend Setup (Next.js)

1.  **Open a NEW Command Prompt or PowerShell window.**

2.  **Navigate to the frontend folder:**
    ```powershell
    cd frontend
    ```

3.  **Install dependencies:**
    ```powershell
    npm install
    ```

4.  **Configure Environment:**
    Create a file named `.env.local` inside the `frontend/` folder and add your Clerk keys:
    ```ini
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
    CLERK_SECRET_KEY=sk_test_...
    
    NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
    NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
    NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
    NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
    ```

5.  **Run the Frontend:**
    ```powershell
    npm run dev
    ```
    The app will start at `http://localhost:3000`.

---

## 🎮 How to Use

1.  **Start both servers** (Backend on port 8000, Frontend on port 3000).
2.  Open **`http://localhost:3000`** in your browser.
3.  **Sign In** using your account.
4.  Go to the **Dashboard**.
5.  Click **"Fetch Recent Games"** to see your Chess.com history.
6.  Click **"Generate AI Commentary"** on any game.
    * *Note: Generation takes time (30s - 2 mins) depending on hardware.*
7.  Listen to your personalized commentary!

---

## 📁 Key Directories

* **`templates/`**: Contains the 28 image templates used for computer vision tasks.
* **`output/`**: Generated audio files are saved here.
* **`models/`**: Stores the downloaded Coqui TTS models.
