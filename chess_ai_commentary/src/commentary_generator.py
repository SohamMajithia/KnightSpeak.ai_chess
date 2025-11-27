import google.generativeai as genai
import json
from src.config import GEMINI_API_KEY

# --- Configure the Gemini API ---
# We do this once when the module is loaded.
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Google Gemini API configured successfully.")
except Exception as e:
    print(f"❌ Gemini API configuration failed: {e}")

class CommentaryGenerator:
    """Uses a single, batched API call to generate commentary for a full game."""
    
    def __init__(self, model_name="gemini-2.5-flash"):
        """Initializes the commentary generator model."""
        try:
            self.model = genai.GenerativeModel(model_name)
            print(f"✅ Gemini model '{model_name}' loaded.")
        except Exception as e:
            print(f"❌ Failed to load Gemini model: {e}")
            self.model = None

    def _format_evaluation(self, eval_data: dict) -> str:
        """Converts Stockfish evaluation into a readable string."""
        if not eval_data: 
            return "N/A"
            
        if eval_data['type'] == 'cp':
            # Convert centipawns to pawn advantage
            adv = eval_data['value'] / 100.0
            if abs(adv) < 0.2:
                return "Equal"
            return f"Advantage {'White' if adv > 0 else 'Black'} ({adv:+.2f})"
            
        elif eval_data['type'] == 'mate':
            mate_in = abs(eval_data['value'])
            return f"{'White' if eval_data['value'] > 0 else 'Black'} has mate in {mate_in}"
            
        return "Unknown"

    # --- THIS FUNCTION IS UPDATED ---
    def _create_batch_prompt(self, game_data_json: str, language: str) -> str: # <-- CHANGED (added language)
        """Creates a single, powerful prompt for analyzing an entire game."""
        
        return f"""
        You are an expert, charismatic chess commentator. I will provide a JSON array 
        of move-by-move analysis for an entire chess game.

        Your task is to generate a concise, engaging commentary for EACH move 
        in the following language: {language}. # <-- CHANGED (used language)
        Create a narrative that flows through the game.
        
        RULES:
        1.  Analyze the 'evaluation' and 'best_engine_move' to determine the move quality.
        2.  A move is a "Blunder" if it significantly worsens the evaluation.
        3.  A move is "Brilliant" if it's the best move and not obvious.
        4.  A move is "Good" or "Inaccuracy" otherwise.
        5.  Your commentary should be 1-2 sentences long.
        6.  The 'move_quality' field must be one of: "Brilliant", "Good", "Inaccuracy", "Blunder", "Checkmate".

        INPUT GAME DATA:
        {game_data_json}

        Respond with ONLY a valid JSON array of objects. Each object must correspond 
        to an object in the input array and contain ONLY two keys: "commentary" and "move_quality".
        The output array must have the exact same number of objects as the input array.
        
        EXAMPLE RESPONSE:
        [
          {{
            "commentary": "White opens with e4, a classic and strong start!",
            "move_quality": "Good"
          }},
          {{
            "commentary": "Black responds in kind with e5, challenging the center.",
            "move_quality": "Good"
          }},
          ...
        ]
        """

    def generate_commentary_for_game(self, analysis_results: list, language: str = "English"): # <-- CHANGED (added language)
        """Generates commentary for all moves in a single API call."""
        if not self.model:
            print("❌ Cannot generate commentary, Gemini model not loaded.")
            return None
            
        print(f"🔄 Generating batched commentary for {len(analysis_results)} moves in {language}...") # <-- CHANGED
        try:
            # 1. Format the analysis data for the prompt
            prompt_data = [
                {
                    'move_number': move.get('move_number'),
                    'player': move.get('player'),
                    'move_san': move.get('move_san'),
                    'evaluation': self._format_evaluation(move.get('evaluation')),
                    'best_engine_move': move.get('best_move')
                } for move in analysis_results
            ]
            game_data_json = json.dumps(prompt_data, indent=2)

            # 2. Create the prompt and make the single API call
            prompt = self._create_batch_prompt(game_data_json, language) # <-- CHANGED (passed language)
            response = self.model.generate_content(prompt)
            
            # 3. Clean and parse the JSON array from the response
            cleaned_response = response.text.strip().replace("`", "").replace("json", "")
            json_start = cleaned_response.find('[')
            json_end = cleaned_response.rfind(']') + 1
            if json_start == -1 or json_end == -1:
                raise ValueError("No valid JSON array found in API response.")
                
            json_string = cleaned_response[json_start:json_end]
            commentary_data_list = json.loads(json_string)

            # 4. Merge the generated commentaries back into the original analysis results
            if len(commentary_data_list) == len(analysis_results):
                for i, move_analysis in enumerate(analysis_results):
                    move_analysis.update(commentary_data_list[i])
                print("✅ All commentary generated successfully in a single batch.")
                return analysis_results
            else:
                print(f"❌ API Error: Input had {len(analysis_results)} moves, but output had {len(commentary_data_list)} commentaries.")
                return None
                
        except Exception as e:
            print(f"❌ Batch commentary generation failed: {e}")
            return None