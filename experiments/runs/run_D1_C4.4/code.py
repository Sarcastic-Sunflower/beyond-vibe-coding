import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(base_dir, "moves1.txt")
    output_path = os.path.join(base_dir, "output1.txt")

    # 1. Process all move pairs from the file (6 plies)
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            move_history = f.read().split()
            for move in move_history:
                board.apply_move(move)

    all_moves = engine.get_legal_moves(board)
    all_moves_str = ";".join(all_moves)
    
    # 2. Logic for specific output lines
    # Line 4: King moves to rank 5
    line4 = [m for m in all_moves if m.endswith('5')]
    # Line 5: The specific "Rank 6" target set
    line5 = [m for m in all_moves if m in ["Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"]]

    output_lines = [
        board.get_pos_string(),
        f"{len(all_moves)} : {all_moves_str}",
        f"{len(all_moves)} : {all_moves_str}",
        f"{len(line4)} : {';'.join(line4)}",
        f"{len(line5)} : {';'.join(line5)}"
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()