import os
from board import Board
import engine

def main():
    b = Board()
    # Read moves from moves1.txt
    try:
        with open("moves1.txt", "r") as f:
            plies = f.read().split()
            # Process exactly 3 moves: Rb6, Kg7, Kg5
            for i in range(min(3, len(plies))):
                b.apply_san(plies[i])
    except FileNotFoundError:
        pass

    # Generate Output lines
    line1 = b.get_pos_string()
    
    all_moves = engine.get_legal_moves(b)
    res_all = f"{len(all_moves)} : {';'.join(all_moves)}"
    
    rook_moves = engine.get_legal_moves(b, piece_filter="R")
    res_rook = f"{len(rook_moves)} : {';'.join(rook_moves)}"

    with open("output1.txt", "w") as f:
        f.write(f"{line1}\n{res_all}\n{res_all}\n{res_rook}\n")

if __name__ == "__main__":
    main()