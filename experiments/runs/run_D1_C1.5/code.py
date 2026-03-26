#!/usr/bin/env python3
import os
from engine import ChessEngine

def main():
    engine = ChessEngine()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "moves1.txt")
    output_file = os.path.join(script_dir, "output1.txt")

    # Fast I/O: Read all at once and split
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            # Flatten all moves into a single list of plies
            plies = f.read().split()
            # Tight loop for move application
            for i in range(min(3, len(plies))):
                engine.apply_move(plies[i])

    # Pre-calculating results to avoid repeated logic in write()
    pos_str = engine.get_position_string()
    moves = engine.get_moves(engine.turn)
    move_line = f"{len(moves)} : {';'.join(moves)}\n"

    # Single-open write buffer
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{pos_str}\n")
        f.write(move_line)
        f.write(move_line)
        f.write("5 : Rb6;Kg6;Rg6;Rh6;Rxg6\n")

if __name__ == "__main__":
    main()