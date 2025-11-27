import os
import io
import chess
import chess.pgn
from stockfish import Stockfish

class ChessAnalyzer:
    """
    A class to analyze chess games from various sources using the Stockfish engine.
    It can analyze PGN strings, FEN strings, and PGN files.
    """
    
    def __init__(self, stockfish_path):
        """Initializes the chess analyzer with the Stockfish engine."""
        self.stockfish_path = stockfish_path
        try:
            # Ensure the provided path exists before initializing
            if not self.stockfish_path or not os.path.exists(self.stockfish_path):
                raise FileNotFoundError(f"Stockfish executable not found at: {self.stockfish_path}")
            
            self.stockfish = Stockfish(path=self.stockfish_path)
            print("✅ Stockfish engine initialized successfully!")
        except Exception as e:
            print(f"❌ Stockfish initialization failed: {e}")
            self.stockfish = None

    def analyze_position(self, fen, depth=15):
        """Analyzes a single chess position from a FEN string."""
        if not self.stockfish:
            print("⚠️ Stockfish not available for analysis.")
            return None
        try:
            self.stockfish.set_depth(depth)
            self.stockfish.set_fen_position(fen)
            evaluation = self.stockfish.get_evaluation()
            best_move = self.stockfish.get_best_move()
            top_moves = self.stockfish.get_top_moves(3)
            
            return {
                'fen': fen, 
                'evaluation': evaluation,
                'best_move': best_move, 
                'top_moves': top_moves,
            }
        except Exception as e:
            print(f"⚠️ Position analysis error: {e}")
            return None

    def analyze_game(self, pgn_string):
        """Analyzes a complete game from a PGN string, move by move."""
        if not self.stockfish: 
            print("⚠️ Stockfish not available for game analysis.")
            return []
            
        try:
            game = chess.pgn.read_game(io.StringIO(pgn_string))
            if not game:
                print("❌ Invalid PGN format.")
                return []
                
            board = game.board()
            analysis_results = []
            mainline_moves = list(game.mainline_moves())
            total_moves = len(mainline_moves)
            print(f"🔄 Analyzing game with {total_moves} moves...")

            for i, move in enumerate(mainline_moves):
                # Get the move in Standard Algebraic Notation (e.g., "Nf3") *before* pushing
                move_san = board.san(move) 
                
                # Make the move
                board.push(move)
                
                # Analyze the position *after* the move
                position_data = self.analyze_position(board.fen())
                
                if position_data:
                    position_data.update({
                        'move_number': i + 1,
                        'move_san': move_san, 
                        'player': 'White' if board.turn == chess.BLACK else 'Black' # Player who *just* moved
                    })
                    analysis_results.append(position_data)
                    
                if (i + 1) % 10 == 0 or (i + 1) == total_moves:
                    print(f"   📊 Analyzed move {i + 1}/{total_moves} ({move_san})...")
                    
            print("✅ Game analysis complete.")
            return analysis_results
            
        except Exception as e:
            print(f"❌ Game analysis failed: {e}")
            return []

    def load_pgn_from_file(self, file_path):
        """Loads PGN content from a specified file path."""
        try:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                pgn_content = f.read()
            print(f"✅ PGN file loaded: {os.path.basename(file_path)} ({len(pgn_content)} chars)")
            return pgn_content
        except Exception as e:
            print(f"❌ Error loading PGN file: {e}")
            return None
            
    def analyze_pgn_file(self, file_path):
        """A convenience method to load and analyze a PGN file."""
        pgn_content = self.load_pgn_from_file(file_path)
        if pgn_content:
            return self.analyze_game(pgn_content)
        return []