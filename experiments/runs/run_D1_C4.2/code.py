import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(base_dir, "moves1.txt")
    output_path = os.path.join(base_dir, "output1.txt")

    # Read and process exactly 3 moves
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            # split() handles all whitespace/newlines automatically
            move_history = f.read().split()
            for i in range(min(3, len(move_history))):
                board.apply_move(move_history[i])

    # Generate current board state string
    current_state = board.get_pos_string()
    
    # Generate ALL legal moves for the current turn
    all_moves = engine.get_legal_moves(board)
    all_moves_str = ";".join(all_moves)
    
    # Filter for Rook-only moves for the 4th line
    rook_moves = [m for m in all_moves if m.startswith('R')]
    rook_moves_str = ";".join(rook_moves)

    # Prepare output exactly as requested
    output_lines = [
        current_state,
        f"{len(all_moves)} : {all_moves_str}",
        f"{len(all_moves)} : {all_moves_str}",
        f"{len(rook_moves)} : {rook_moves_str}"
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()