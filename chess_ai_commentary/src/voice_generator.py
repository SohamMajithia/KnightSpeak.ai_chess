import os
import tempfile
import pygame
import time
from TTS.api import TTS

class VoiceGenerator:
    """
    Handles TTS conversion and audio playback using pygame.
    Supports both built-in speakers (for notebook) 
    and voice cloning (for Gradio app).
    """
    
    def __init__(self, tts_model: TTS):
        """Initializes the voice generator with the loaded TTS model."""
        self.tts_model = tts_model
        # This is the default built-in speaker for the notebook
        self.notebook_speaker_name = "Claribel Dervla" 
        
        try:
            pygame.mixer.init(frequency=24000)
            print("✅ Pygame audio mixer initialized.")
        except Exception as e:
            print(f"⚠️ Audio system initialization failed: {e}")
            
        if self.tts_model:
            print("✅ VoiceGenerator ready with model.")
        else:
            print("❌ VoiceGenerator initialized WITHOUT a TTS model.")

    # --- Method for Gradio App (Voice Cloning) ---
    def generate_audio_with_clone(self, text: str, speaker_wav_path: str, language: str, output_path: str):
        """Generates audio using a speaker_wav file for voice cloning."""
        if not self.tts_model:
            print("❌ TTS model not configured.")
            return None
        if not os.path.exists(speaker_wav_path):
            print(f"❌ Speaker WAV file not found: {speaker_wav_path}")
            return None

        try:
            print(f"🎤 Generating audio with cloned voice from: {os.path.basename(speaker_wav_path)}...")
            start_time = time.time()
            
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=speaker_wav_path, # <-- Uses voice cloning
                language=language
            )
            
            gen_time = time.time() - start_time
            print(f"✅ Audio generated in {gen_time:.2f} seconds.")
            print(f"   💾 File saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            return None

    # --- Method for Notebook (Built-in Speaker) ---
    def generate_and_play(self, text: str, output_path: str = None, language: str = 'en'):
        """
        Generates audio using a built-in speaker and plays it immediately.
        This is the method for the notebook.
        """
        if not self.tts_model:
            print("❌ TTS model not configured.")
            return None

        temp_file_used = False
        if not output_path:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            output_path = temp_file.name
            temp_file.close()
            temp_file_used = True

        try:
            print(f"🎤 Generating audio with built-in speaker '{self.notebook_speaker_name}'...")
            start_time = time.time()
            
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker=self.notebook_speaker_name, # <-- Uses built-in speaker
                language=language
            )
            
            gen_time = time.time() - start_time
            print(f"✅ Audio generated in {gen_time:.2f} seconds.")
            print(f"   💾 File saved to: {output_path}")
            
            # Play the generated audio
            self.play_audio(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            return None
        finally:
            # Clean up the temporary file if we created one
            if temp_file_used and os.path.exists(output_path):
                try:
                    os.remove(output_path)
                    print(f"   🗑️ Temporary file {os.path.basename(output_path)} removed.")
                except Exception as e:
                    print(f"   ⚠️ Could not remove temporary file: {e}")

    # --- Helper for playback ---
    def play_audio(self, audio_path: str):
        """Plays an audio file using pygame."""
        if not os.path.exists(audio_path):
            print(f"❌ Cannot play audio. File not found at: {audio_path}")
            return
        try:
            print(f"🔊 Playing audio...")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            print("✅ Playback finished.")
        except Exception as e:
            print(f"❌ Audio playback error: {e}")