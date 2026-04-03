#!/usr/bin/env python3
import os
from board import ChessBoard
from engine import MoveGenerator

def main():
    board = ChessBoard()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves2.txt")
    
    # Process history
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            raw_content = f.read().split()
            # Clean moves (remove move numbers like '1.')
            moves = [m for m in raw_content if not m.endswith(".")]
            
        turn = "W"
        for move in moves:
            board.parse_san(move, turn)
            turn = "B" if turn == "W" else "W"

    # Generate Black's moves for the current position
    all_m, leg_m, ill_m = MoveGenerator.get_black_moves(board)

    def format_line(mvs):
        return f"{len(mvs)} : " + ";".join(mvs) if mvs else "0 :"

    # Write output2.txt
    out_path = os.path.join(script_dir, "output2.txt")
    with open(out_path, "w") as f:
        f.write(board.get_position_string() + "\n")
        f.write(format_line(all_m) + "\n")
        f.write(format_line(leg_m) + "\n")
        f.write(format_line(ill_m) + "\n")

if __name__ == "__main__":
    main()