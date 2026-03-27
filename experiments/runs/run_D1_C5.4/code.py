import os
from board import Board
import engine

def main():
    board = Board()
    # Path handling for same-directory files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_file = os.path.join(base_dir, "moves1.txt")
    output_file = os.path.join(base_dir, "output1.txt")

    if os.path.exists(moves_file):
        with open(moves_file, "r") as f:
            # Tokenize moves, skipping empty strings or newlines
            moves = [m for m in f.read().split() if m]
            for move in moves[:3]:
                board.apply_move(move)

    legal = engine.get_legal_moves(board)
    move_str = ";".join(legal)
    
    # Line 4: King moves ending on Rank 5
    line4 = [m for m in legal if m.startswith('K') and m.endswith('5')]
    
    # Line 5: Tactical Subset
    subset = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    line5 = [m for m in legal if m in subset]

    with open(output_file, "w") as f:
        f.write(f"{board.get_pos_string()}\n")
        f.write(f"{len(legal)} : {move_str}\n")
        f.write(f"{len(legal)} : {move_str}\n")
        f.write(f"{len(line4)} : {';'.join(line4)}\n")
        f.write(f"{len(line5)} : {';'.join(line5)}\n")

if __name__ == "__main__":
    main()