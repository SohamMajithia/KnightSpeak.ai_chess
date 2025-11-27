import os
from datetime import datetime
from src.chess_analyzer import ChessAnalyzer
from src.commentary_generator import CommentaryGenerator
from src.voice_generator import VoiceGenerator

class ChessCommentaryPipeline:
    """Orchestrates the entire process from PGN to audio commentary."""

    def __init__(self, analyzer: ChessAnalyzer, commentary_gen: CommentaryGenerator, voice_gen: VoiceGenerator):
        """
        Initializes the pipeline with all the necessary components.
        """
        self.analyzer = analyzer
        self.commentary_generator = commentary_gen
        self.voice_generator = voice_gen
        
        if not all([analyzer, commentary_gen, voice_gen]):
            raise ValueError("All components (analyzer, commentary_gen, voice_gen) must be provided.")
            
        print("\n🚀 Complete chess commentary pipeline is ready!")

    def _run_common_steps(self, pgn_string: str, language_choice: str = "English"):
        """Internal method for analysis and commentary generation."""
        
        # --- Step 1: Analyze the game moves with Stockfish ---
        print("\n[Step 1/2] 📊 Analyzing game moves...")
        analysis_results = self.analyzer.analyze_game(pgn_string)
        if not analysis_results:
            print("❌ Analysis step failed.")
            return None, None

        # --- Step 2: Generate commentary for each move using the Gemini model ---
        print("\n[Step 2/2] ✍️ Generating AI commentary...")
        
        # Map full language name to language code for TTS
        language_map = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
        language_code = language_map.get(language_choice, "en") # Default to 'en'

        analysis_with_commentary = self.commentary_generator.generate_commentary_for_game(
            analysis_results, 
            language=language_choice # Pass full name to Gemini
        )
        if not analysis_with_commentary:
            print("❌ Commentary step failed.")
            return None, None
            
        # Combine all commentary strings into a single text block
        full_commentary = " ".join(
            move.get('commentary', '') for move in analysis_with_commentary if move.get('commentary')
        )
        
        if not full_commentary.strip():
            print("⚠️ No commentary text was generated to synthesize.")
            return None, None
            
        return full_commentary, language_code

    # --- THIS IS THE MISSING METHOD ---
    def run_pipeline_for_backend(self, pgn_string: str, language_choice: str = "English"):
        """
        Runs the full pipeline, saves the file, and returns the path.
        Does NOT play audio. Used by the FastAPI backend.
        """
        print(f"--- Backend Pipeline Started for PGN: {pgn_string[:30]}... ---")
        
        # 1. Run common analysis and commentary steps
        full_commentary, language_code = self._run_common_steps(pgn_string, language_choice)
        
        if not full_commentary:
            print("❌ Backend Pipeline: Failed at common steps.")
            return None

        # 2. Synthesize voice
        print("   Synthesizing voice...")
        
        # Create a unique output path
        # We assume we are running from the 'backend' folder, so we go up one level to 'output'
        output_dir = "../output/audio"
        os.makedirs(output_dir, exist_ok=True)
        
        output_filename = f"{output_dir}/commentary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        default_voice_path = os.path.join(os.getcwd(), "default_voice.wav")
        
        if not os.path.exists(default_voice_path):
             print(f"⚠️ Default voice not found at {default_voice_path}, trying to download or use fallback...")
             # You might want to call your setup_default_voice() here if you imported it
        
        audio_file_path = self.voice_generator.generate_audio_with_clone(
            text=full_commentary,
            speaker_wav_path=default_voice_path, 
            language=language_code,
            output_path=output_filename
        )
        
        if not audio_file_path:
            print("❌ Backend Pipeline: Voice generation failed.")
            return None
            
        print(f"✅ Backend Pipeline Finished. File saved to: {audio_file_path}")
        return audio_file_path

    def process_pgn_for_app(self, pgn_string: str, language_choice: str, speaker_wav_path: str):
        """Runs the full pipeline using a cloned voice for the Gradio app."""
        print("\n" + "="*50)
        print("🎯 Starting App Pipeline (with Voice Cloning)...")
        print("="*50)
        
        full_commentary, language_code = self._run_common_steps(pgn_string, language_choice)
        
        if not full_commentary:
            return None, None 

        # --- Step 3: Synthesize voice using voice cloning ---
        print("\n[Step 3/3] 🔊 Synthesizing voice audio (cloning)...")
        
        output_filename = f"output/audio/commentary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        audio_file_path = self.voice_generator.generate_audio_with_clone(
            text=full_commentary,
            speaker_wav_path=speaker_wav_path,
            language=language_code,
            output_path=output_filename
        )

        if not audio_file_path:
            print("❌ Voice generation step failed.")
            return None, None
            
        print("\n🎉 APP PIPELINE FINISHED! 🎉")
        return audio_file_path, full_commentary

    def process_pgn_for_notebook(self, pgn_string: str, play_audio: bool = True, save_path: str = None, language: str = 'en'):
        """Runs the full pipeline using built-in speakers (for your notebook)."""
        print("\n" + "="*50)
        print("🎯 Starting Notebook Pipeline (with Built-in Speaker)...")
        print("="*50)

        language_map_rev = {"en": "English", "es": "Spanish", "fr": "French", "de": "German"}
        language_choice = language_map_rev.get(language, "English")
        
        full_commentary, language_code = self._run_common_steps(pgn_string, language_choice)
        
        if not full_commentary:
            return 

        print("\n[Step 3/3] 🔊 Synthesizing voice audio (built-in)...")
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            print(f"   📂 Output directory ensured: {os.path.dirname(save_path)}")

        # Note: Ensure VoiceGenerator has generate_and_play method
        if hasattr(self.voice_generator, 'generate_and_play'):
             audio_file_path = self.voice_generator.generate_and_play(
                full_commentary, 
                output_path=save_path,
                language=language_code
            )
        else:
             print("❌ VoiceGenerator missing 'generate_and_play' method")
             return

        if not audio_file_path:
            print("❌ Voice generation step failed.")
            return

        print("\n🎉 NOTEBOOK PIPELINE FINISHED! 🎉")
        return audio_file_path