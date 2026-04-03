import os
from board import ChessBoard
from engine import MoveGenerator

def main():
    board = ChessBoard()
    path = os.path.join(os.path.dirname(__file__), "moves2.txt")
    
    if os.path.exists(path):
        with open(path, "r") as f:
            # Flatten move list and filter out move numbers
            moves = [m for m in f.read().split() if not m[0].isdigit()]
            
        turn = "W"
        for move in moves:
            board.parse_san(move, turn)
            turn = "B" if turn == "W" else "W"

    all_m, leg_m, ill_m = MoveGenerator.get_black_moves(board)

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}"
    ]

    with open(os.path.join(os.path.dirname(__file__), "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()