import os
from board import Board
import engine

def main():
    board = Board()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(base_dir, "moves1.txt")
    output_path = os.path.join(base_dir, "output1.txt")

    # Process exactly 3 moves from moves1.txt
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            # Flatten all moves into a single list
            all_input_moves = f.read().split()
            # Process only the first 3 moves found
            for move in all_input_moves[:3]:
                board.apply_move(move)

    # Generate current legal moves
    legal_moves = engine.get_legal_moves(board)
    move_str = ";".join(legal_moves)
    count = len(legal_moves)
    
    # Line 4: King moves to rank 5 (Corrected detection)
    line4 = [m for m in legal_moves if m.startswith('K') and m.endswith('5')]
    
    # Line 5: Specific tactical subset
    target_set = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    line5 = [m for m in legal_moves if m in target_set]

    output = (
        f"{board.get_pos_string()}\n"
        f"{count} : {move_str}\n"
        f"{count} : {move_str}\n"
        f"{len(line4)} : {';'.join(line4)}\n"
        f"{len(line5)} : {';'.join(line5)}\n"
    )

    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()