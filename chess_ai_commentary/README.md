# ♟️ Knightspeaks: AI Chess Commentary

**Knightspeaks** is a full-stack web application that turns your chess games into exciting, professional audio commentary. It combines **Stockfish** for analysis, **Google Gemini** for charismatic narration, and **Coqui TTS** for lifelike voice synthesis.

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