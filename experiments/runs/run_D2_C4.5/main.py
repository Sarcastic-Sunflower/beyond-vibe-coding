import os
from board import ChessBoard
from engine import ChessEngine
from constants import FILES, RANKS

def main():
    board = ChessBoard()
    base_path = os.path.dirname(__file__)
    
    try:
        with open(os.path.join(base_path, "moves2.txt"), "r") as f:
            # Efficiently pull SAN moves only
            content = f.read().split()
            moves = [m for m in content if not m[0].isdigit()]
        
        for i in range(min(7, len(moves))):
            ChessEngine.apply_san_move(board, moves[i], "W" if i % 2 == 0 else "B")
    except FileNotFoundError:
        return

    all_m, leg_m, ill_m = ChessEngine.get_king_moves(board, "B")
    k_idx = board.state.index("BK")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : K{FILES[k_idx % 8]}{RANKS[k_idx // 8]}"
    ]

    with open(os.path.join(base_path, "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()