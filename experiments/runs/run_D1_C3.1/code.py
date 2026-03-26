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
            # Flatten moves and take the first 3
            plies = [move for line in f for move in line.split()]
            for i in range(min(3, len(plies))):
                board.apply_san_move(plies[i])

    pos_str = board.get_position_string()
    
    # Line 2 & 3: All legal moves for current player
    all_moves = get_legal_moves(board)
    move_list_str = ";".join(all_moves)
    full_result = f"{len(all_moves)} : {move_list_str}\n"
    
    # Line 4: Only Rook moves
    rook_moves = get_legal_moves(board, piece_filter="R")
    rook_result = f"{len(rook_moves)} : {';'.join(rook_moves)}\n"

    output_content = f"{pos_str}\n{full_result}{full_result}{rook_result}"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

if __name__ == "__main__":
    main()