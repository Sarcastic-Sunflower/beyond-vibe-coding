# main.py
import sys, os
from engine import Board, WHITE, BLACK

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves1.txt")
    
    board = Board()
    board.setup_initial()
    turn = WHITE
    moves_processed = 0

    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            for line in f:
                if moves_processed >= 3: break
                line = line.strip()
                if not line or line.startswith("#"): continue
                
                # Handle bracketed source info and tokenize
                tokens = line.split(']')[-1].split()
                for token in tokens:
                    if moves_processed < 3:
                        board.apply_san(token, turn)
                        turn = BLACK if turn == WHITE else WHITE
                        moves_processed += 1

    legal_moves = board.get_legal_moves(turn)
    mv_str = ";".join(legal_moves)
    move_line = f"{len(legal_moves)} :" + (f" {mv_str}" if legal_moves else "")
    
    output_content = f"{board.pos_string()}\n{move_line}\n{move_line}\n0 :\n"
    
    with open(os.path.join(script_dir, "output1.txt"), "w") as f:
        f.write(output_content)

if __name__ == "__main__":
    main()