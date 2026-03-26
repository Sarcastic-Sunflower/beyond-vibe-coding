import os
import sys
from chess_engine import ChessEngine

def main():
    """
    Entry point for the refactored chess engine.
    Maintains the legacy output format while utilizing the improved ChessEngine class.
    """
    engine = ChessEngine()
    engine.setup_initial_position()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    # Process the next 3 moves (lines) from the file history
    if os.path.exists(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[:3]:
                # Split by whitespace to handle multiple moves per line (White, then Black)
                move_parts = line.strip().split()
                for i, move in enumerate(move_parts):
                    # Determine color based on position in the line
                    current_color = "W" if i % 2 == 0 else "B"
                    engine.apply_move(move, current_color)
                    # Toggle turn state after each half-move
                    engine.turn = "B" if engine.turn == "W" else "W"

    # Generate pseudo-legal moves for the current turn
    available_moves = engine.get_pseudo_legal_moves(engine.turn)
    move_list_str = ";".join(available_moves)
    move_line = f"{len(available_moves)} :" + (f" {move_list_str}" if available_moves else "")
    
    current_pos = engine.get_position_string()

    # Output to file in the exact legacy format required
    output_path = os.path.join(script_dir, "output1.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(current_pos + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n")
        f.write("0 :\n")

if __name__ == "__main__":
    main()
