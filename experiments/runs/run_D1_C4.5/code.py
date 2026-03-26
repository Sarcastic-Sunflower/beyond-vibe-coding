import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(base_dir, "moves1.txt")
    output_path = os.path.join(base_dir, "output1.txt")

    # 1. Faster Input Processing
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            # Process all moves found in the file
            for move in f.read().split():
                board.apply_move(move)

    # 2. Optimized Move Set Generation
    all_moves = engine.get_legal_moves(board)
    all_moves_str = ";".join(all_moves)
    move_count = len(all_moves)
    
    # 3. High-Efficiency Filtering for specific lines
    # Line 4: King moves to rank 5 (e.g., ends in '5')
    line4 = [m for m in all_moves if m.endswith('5')]
    # Line 5: Specific subset targeting Rank 6
    target_set = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    line5 = [m for m in all_moves if m in target_set]

    # 4. Final Output Formatting
    output = (
        f"{board.get_pos_string()}\n"
        f"{move_count} : {all_moves_str}\n"
        f"{move_count} : {all_moves_str}\n"
        f"{len(line4)} : {';'.join(line4)}\n"
        f"{len(line5)} : {';'.join(line5)}\n"
    )

    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()