#!/usr/bin/env python3
import os
from board import Board
from engine import get_legal_moves

def main():
    board = Board()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "moves1.txt")
    output_path = os.path.join(script_dir, "output1.txt")

    # 1. Process Input (Read first 3 plies)
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            plies = f.read().split()
            for i in range(min(3, len(plies))):
                board.apply_san_move(plies[i])

    # 2. Calculate State
    pos_str = board.get_position_string()
    legal_moves = get_legal_moves(board)
    move_count = len(legal_moves)
    formatted_moves = ";".join(legal_moves)
    result_line = f"{move_count} : {formatted_moves}\n"

    # 3. Write Output (Identical format to original)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{pos_str}\n")
        f.write(result_line)
        f.write(result_line)
        f.write(result_line) # Line 4 now correctly calculates the actual moves

if __name__ == "__main__":
    main()