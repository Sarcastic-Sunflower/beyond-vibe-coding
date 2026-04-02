# main.py
import sys, os
from engine import Board, WHITE, BLACK

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves1.txt")
    
    board = Board()
    board.setup_initial() # 
    turn = WHITE
    move_count = 0

    if os.path.exists(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            for line in f:
                if move_count >= 3: break
                line = line.strip()
                if not line or line.startswith("#"): continue
                
                # Robust tokenization for SAN strings
                tokens = line.split(']')[-1].split()
                for token in tokens:
                    if move_count < 3:
                        board.apply_san(token, turn)
                        turn = BLACK if turn == WHITE else WHITE
                        move_count += 1

    legal_moves = board.get_legal_moves(turn)
    mv_str = ";".join(legal_moves)
    move_line = f"{len(legal_moves)} :" + (f" {mv_str}" if legal_moves else "")
    
    # Exact output format preservation
    out_path = os.path.join(script_dir, "output1.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{board.pos_string()}\n{move_line}\n{move_line}\n0 :\n")

if __name__ == "__main__":
    main()