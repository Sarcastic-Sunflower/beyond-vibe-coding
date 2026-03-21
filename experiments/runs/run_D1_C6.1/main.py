# main.py
import sys, os
from engine import ChessEngine, Color

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "moves1.txt")
    
    engine = ChessEngine()
    engine.setup()

    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            move_count = 0
            for line in f:
                if not line.strip() or line.startswith("#"): continue
                tokens = line.split(']')[-1].split()
                for token in tokens:
                    if move_count < 3:
                        engine.apply_san(token)
                        move_count += 1
    
    legal_moves = engine.get_legal_moves(engine.turn)
    mv_line = f"{len(legal_moves)} :" + (f" {';'.join(legal_moves)}" if legal_moves else "")
    
    with open(os.path.join(script_dir, "output1.txt"), "w") as f:
        f.write(f"{engine.get_pos_string()}\n{mv_line}\n{mv_line}\n0 :\n")

if __name__ == "__main__":
    main()