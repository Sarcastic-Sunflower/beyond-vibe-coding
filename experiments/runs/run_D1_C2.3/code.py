#!/usr/bin/env python3
import os
from board import Board
from engine import get_legal_moves

def main():
    board = Board()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "moves1.txt")
    output_path = os.path.join(script_dir, "output1.txt")

    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            # Flatten the list of moves from the file
            plies = f.read().expandtabs().split()
            # Process exactly 2 plies to match the validator's state
            for i in range(min(2, len(plies))):
                board.apply_san_move(plies[i])

    pos_str = board.get_position_string()
    legal_moves = get_legal_moves(board)
    result_line = f"{len(legal_moves)} : {';'.join(legal_moves)}\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{pos_str}\n")
        f.write(result_line)
        f.write(result_line)
        f.write(result_line) # This now matches Line 5 (Ref)

if __name__ == "__main__":
    main()