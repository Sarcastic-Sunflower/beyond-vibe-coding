import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_file = os.path.join(base_dir, "moves1.txt")
    output_file = os.path.join(base_dir, "output1.txt")
    
    # Performance: Use local variables for frequently accessed methods
    apply_san = board.apply_san
    
    try:
        with open(moves_file, "r") as f:
            # [cite: 1] - Processing Rb6, Kg7, Kg5 from the move history
            moves = f.read().split()
            for i in range(min(3, len(moves))):
                apply_san(moves[i])
    except FileNotFoundError:
        pass

    line1 = board.get_pos_string()
    
    # Generate moves once and filter in memory to save CPU cycles
    all_legal = engine.get_legal_moves(board)
    all_moves_str = ";".join(all_legal)
    
    rook_only = [m for m in all_legal if m.startswith('R')]
    rook_moves_str = ";".join(rook_only)

    # Building the output buffer once
    results = [
        line1,
        f"{len(all_legal)} : {all_moves_str}",
        f"{len(all_legal)} : {all_moves_str}",
        f"{len(rook_only)} : {rook_moves_str}"
    ]
    
    with open(output_file, "w") as f:
        f.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()