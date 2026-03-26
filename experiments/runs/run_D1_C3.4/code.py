import os
from board import Board
import engine

def main():
    b = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_file = os.path.join(base_dir, "moves1.txt")
    output_file = os.path.join(base_dir, "output1.txt")

    if os.path.exists(moves_file):
        with open(moves_file, "r") as f:
            # Handle tabs and newlines from the source file 
            content = f.read().replace('\t', ' ').split()
            # Process exactly 3 plies: Rb6, Kg7, Kg5 
            for i in range(min(3, len(content))):
                b.apply_san(content[i])

    line1 = b.get_pos_string()
    all_moves = engine.get_legal_moves(b)
    res_all = f"{len(all_moves)} : {';'.join(all_moves)}"
    
    # Line 4 logic: Specifically filter for Rook moves
    rook_moves = engine.get_legal_moves(b, piece_filter="R")
    res_rook = f"{len(rook_moves)} : {';'.join(rook_moves)}"

    output_content = f"{line1}\n{res_all}\n{res_all}\n{res_rook}\n"
    
    with open(output_file, "w") as f:
        f.write(output_content)

if __name__ == "__main__":
    main()