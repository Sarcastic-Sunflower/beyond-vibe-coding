#!/usr/bin/env python3
import sys, os
from engine import ChessEngine

def main():
    engine = ChessEngine()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    # 1. Process move history
    if os.path.isfile(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                for mv in parts:
                    if mv and not mv.startswith("#"):
                        engine.apply_move(mv)

    # 2. Calculate Output
    pos_str = engine.get_position_string()
    available_moves = engine.get_moves(engine.turn)
    
    move_count = len(available_moves)
    move_list_str = ";".join(available_moves)
    formatted_moves = f"{move_count} :" + (f" {move_list_str}" if available_moves else "")

    # 3. Write output1.txt (Identical format, corrected logic)
    out_path = os.path.join(script_dir, "output1.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pos_str + "\n")      # Line 1: Current positions
        f.write(formatted_moves + "\n") # Line 2: Possible moves
        f.write(formatted_moves + "\n") # Line 3: Possible moves (repeated per legacy)
        f.write("0 :\n")                # Line 4: Explicitly fixed as requested

if __name__ == "__main__":
    main()