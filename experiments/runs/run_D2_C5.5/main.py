import os
from board import ChessBoard
from engine import ChessEngine

def main():
    board = ChessBoard()
    path = os.path.join(os.path.dirname(__file__), "moves2.txt")
    
    if os.path.exists(path):
        with open(path, "r") as f:
            san_moves = [m for m in f.read().split() if not m[0].isdigit()]
            
        for i in range(min(7, len(san_moves))):
            ChessEngine.apply_move(board, san_moves[i], "W" if i % 2 == 0 else "B")

    all_m, leg_m, ill_m, k_pos = ChessEngine.get_king_analysis(board, "B")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : {k_pos}"
    ]

    with open(os.path.join(os.path.dirname(__file__), "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()