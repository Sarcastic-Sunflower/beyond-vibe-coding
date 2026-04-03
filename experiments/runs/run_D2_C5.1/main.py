import os
from board import ChessBoard
from engine import ChessEngine

def main():
    board = ChessBoard()
    dir_path = os.path.dirname(__file__)
    
    # Process moves2.txt
    try:
        with open(os.path.join(dir_path, "moves2.txt"), "r") as f:
            tokens = f.read().split()
            # Filter out move numbers (e.g., "1.")
            san_moves = [m for m in tokens if not m[0].isdigit()]
            
        # Process exactly 7 half-moves (4 White, 3 Black)
        for i in range(min(7, len(san_moves))):
            color = "W" if i % 2 == 0 else "B"
            ChessEngine.apply_move(board, san_moves[i], color)
    except FileNotFoundError:
        return

    # Calculate Black King moves (Black to move)
    all_m, leg_m, ill_m, k_pos = ChessEngine.get_king_analysis(board, "B")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : {k_pos}"
    ]

    with open(os.path.join(dir_path, "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()