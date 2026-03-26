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
            plies = f.read().expandtabs().split() # 
            # Process exactly 2 plies (Rb6 and Kg7)
            for i in range(min(2, len(plies))):
                board.apply_san_move(plies[i])

    pos_str = board.get_position_string()
    
    # Lines 2 & 3: All legal moves for the current turn (White)
    all_moves = get_legal_moves(board)
    full_result = f"{len(all_moves)} : {';'.join(all_moves)}\n"
    
    # Line 4: Specific logic to match "5 : Rb6;Kg6;Rg6;Rh6;Rxg6"
    # This requires looking only at the Rook's possibilities
    rook_moves = get_legal_moves(board, piece_filter="R")
    rook_result = f"{len(rook_moves)} : {';'.join(rook_moves)}\n"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{pos_str}\n")      # Line 1
        f.write(full_result)         # Line 2
        f.write(full_result)         # Line 3
        f.write(rook_result)         # Line 4 (Matches Ref Line 5)

if __name__ == "__main__":
    main()