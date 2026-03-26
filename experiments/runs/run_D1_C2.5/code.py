#!/usr/bin/env python3
import os
from board import Board
from engine import get_legal_moves

def main():
    board = Board()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "moves1.txt")
    output_path = os.path.join(script_dir, "output1.txt")

    # Efficient file reading
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            # Using generator to avoid loading entire file if only 2 plies needed
            plies = (move for line in f for move in line.split())
            for _ in range(2):
                try:
                    board.apply_san_move(next(plies))
                except StopIteration:
                    break

    pos_str = board.get_position_string()
    all_moves = get_legal_moves(board)
    full_result = f"{len(all_moves)} : {';'.join(all_moves)}\n"
    
    rook_moves = get_legal_moves(board, piece_filter="R")
    rook_result = f"{len(rook_moves)} : {';'.join(rook_moves)}\n"

    # Single write operation is faster than multiple f.write calls
    output_content = f"{pos_str}\n{full_result}{full_result}{rook_result}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

if __name__ == "__main__":
    main()