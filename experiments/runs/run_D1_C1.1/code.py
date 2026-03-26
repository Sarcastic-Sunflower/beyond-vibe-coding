import os
import sys
from engine import ChessEngine

def main():
    engine = ChessEngine()
    engine.setup_initial()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves1.txt")
    
    plies = []
    if os.path.exists(moves_path):
        with open(moves_path, 'r') as f:
            for line in f:
                # Handle tab or space separation
                plies.extend(line.strip().replace('\t', ' ').split())
    
    # Process exactly 3 plies
    move_outputs = []
    for i in range(3):
        if i < len(plies):
            color = "W" if i % 2 == 0 else "B"
            engine.parse_and_move(plies[i], color)
            
            # Get moves for the player whose turn it is AFTER this ply
            next_player = "B" if color == "W" else "W"
            legal_moves = engine.get_legal_moves(next_player)
            move_outputs.append(f"{len(legal_moves)} :" + (f" {';'.join(legal_moves)}" if legal_moves else ""))
        else:
            move_outputs.append("0 :")
            
    pos_str = engine.get_position_string()
    
    out_path = os.path.join(script_dir, "output1.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pos_str + "\n")
        for line in move_outputs:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
