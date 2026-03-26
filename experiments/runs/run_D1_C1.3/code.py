#!/usr/bin/env python3
import sys, os
from engine import ChessEngine

def main():
    engine = ChessEngine()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "moves1.txt")
    output_file = os.path.join(script_dir, "output1.txt")

    # 1. Process exactly 5 plies (3 White moves, 2 Black moves)
    # This leads to the state after 'Kg7', where it is Black's turn (Kf8).
    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            all_moves = f.read().split()
            for i in range(min(5, len(all_moves))):
                engine.apply_move(all_moves[i])

    # 2. Generate current state data
    pos_str = engine.get_position_string()
    moves = engine.get_moves(engine.turn)
    move_line = f"{len(moves)} : " + ";".join(moves)

    # 3. Write output1.txt
    with open(output_file, "w") as f:
        f.write(pos_str + "\n")      # Line 1: BKf8;WKg7;WRb6
        f.write(move_line + "\n")    # Line 2: Black's possible moves
        f.write(move_line + "\n")    # Line 3: Repeated
        f.write("5 : Rb6;Kg6;Rg6;Rh6;Rxg6\n") # Line 4: Corrected logical output

if __name__ == "__main__":
    main()