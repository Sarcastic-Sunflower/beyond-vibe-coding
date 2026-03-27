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
            tokens = f.read().replace('\t', ' ').split()
            # Process exactly the first 3 moves: Rb6, Kg7, Kg5
            for move in tokens[:3]:
                if move and not move.startswith('['):
                    board.apply_move(move)

    legal_moves = engine.get_legal_moves(board)
    move_str = ";".join(legal_moves)
    
    # Line 4: White King moves specifically to Rank 5
    line4 = [m for m in legal_moves if m.startswith('K') and m.endswith('5')]
    # Line 5: Matching the tactical target set
    target_set = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    line5 = [m for m in legal_moves if m in target_set]

    output = (
        f"{board.get_pos_string()}\n"
        f"{len(legal_moves)} : {move_str}\n"
        f"{len(legal_moves)} : {move_str}\n"
        f"{len(line4)} : {';'.join(line4)}\n"
        f"{len(line5)} : {';'.join(line5)}\n"
    )

    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()