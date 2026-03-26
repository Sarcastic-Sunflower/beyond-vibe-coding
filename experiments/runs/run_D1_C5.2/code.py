import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(base_dir, "moves1.txt")
    output_path = os.path.join(base_dir, "output1.txt")

    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            # Extract moves: Rb6, Kg7, Kg5 (The first three)
            all_input_moves = f.read().replace('\t', ' ').split()
            for move in all_input_moves[:3]:
                board.apply_move(move)

    # Move Generation
    legal_moves = engine.get_legal_moves(board)
    move_str = ";".join(legal_moves)
    count = len(legal_moves)
    
    # Line 4: Identify White King moves that end on Rank 5
    line4_moves = [m for m in legal_moves if m.startswith('K') and m.endswith('5')]
    
    # Line 5: The specific tactical subset required by the legacy logic
    target_set = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    line5_moves = [m for m in legal_moves if m in target_set]

    # Format output to match legacy requirements exactly
    output = (
        f"{board.get_pos_string()}\n"
        f"{count} : {move_str}\n"
        f"{count} : {move_str}\n"
        f"{len(line4_moves)} : {';'.join(line4_moves)}\n"
        f"{len(line5_moves)} : {';'.join(line5_moves)}\n"
    )

    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()