import os
from board import ChessBoard
from engine import MoveGenerator

def main():
    board = ChessBoard()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves2.txt")
    
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            moves = f.read().split()
            
        turn = "W"
        for move in moves:
            board.parse_san(move, turn)
            turn = "B" if turn == "W" else "W"

    all_m, leg_m, ill_m = MoveGenerator.get_black_moves(board)

    with open(os.path.join(script_dir, "output2.txt"), "w") as f:
        f.write(board.get_position_string() + "\n")
        f.write(f"{len(all_m)} : " + ";".join(all_m) + "\n")
        f.write(f"{len(leg_m)} : " + ";".join(leg_m) + "\n")
        f.write(f"{len(ill_m)} : " + ";".join(ill_m) + "\n")

if __name__ == "__main__":
    main()