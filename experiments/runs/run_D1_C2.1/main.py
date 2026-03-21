# main.py
import sys
import os
from board import Board
from move_gen import get_legal_moves

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    # Initialize Board
    board = Board()
    board.setup_initial()
    turn = "W"

    if os.path.isfile(moves_path):
        moves_processed = 0
        with open(moves_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Strip out tags
                if ']' in line:
                    line = line.split(']', 1)[-1]
                
                tokens = line.split()
                if not tokens:
                    continue
                
                # Apply moves and alternate turn
                for token in tokens:
                    board.apply_san_move(token, turn)
                    turn = "B" if turn == "W" else "W"
                
                moves_processed += 1
                if moves_processed == 3:
                    break

    # Calculate strictly legal moves for the current board state
    legal_moves = get_legal_moves(board, turn)
    mv_str = ";".join(legal_moves)
    pos = board.pos_string()
    
    # Match the exact legacy string formatting
    move_line = f"{len(legal_moves)} :" + (f" {mv_str}" if legal_moves else "")

    out_path = os.path.join(script_dir, "output1.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{pos}\n{move_line}\n{move_line}\n0 :\n")

if __name__ == "__main__":
    main()