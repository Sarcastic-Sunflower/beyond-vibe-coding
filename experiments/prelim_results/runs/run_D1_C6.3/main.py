# main.py
import sys, os
from engine import Board, WHITE, BLACK

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves1.txt")
    
    board = Board()
    board.setup_initial()
    turn = WHITE
    moves_left = 3 # Process exactly 3 tokens

    if os.path.exists(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            for line in f:
                if moves_left <= 0: break
                line = line.strip()
                if not line or line.startswith("#"): continue
                
                # Split using legacy bracket rule
                san_part = line.split(']')[-1]
                for token in san_part.split():
                    if moves_left > 0:
                        board.apply_san(token, turn)
                        turn = BLACK if turn == WHITE else WHITE
                        moves_left -= 1

    legal_moves = board.get_legal_moves(turn)
    mv_str = ";".join(legal_moves)
    move_line = f"{len(legal_moves)} :" + (f" {mv_str}" if legal_moves else "")
    
    # Strictly preserve the 4-line duplicate layout
    output = f"{board.pos_string()}\n{move_line}\n{move_line}\n0 :\n"
    
    with open(os.path.join(script_dir, "output1.txt"), "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    main()