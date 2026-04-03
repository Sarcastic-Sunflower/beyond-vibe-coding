import os, re
from board import ChessBoard
from engine import ChessEngine
from constants import FILES, RANKS

def main():
    board = ChessBoard()
    base_dir = os.path.dirname(__file__)
    
    try:
        with open(os.path.join(base_dir, "moves2.txt"), "r") as f:
            raw_text = f.read()
            # Improved regex to capture moves including captures and promotions
            moves = re.findall(r'\b[a-zA-Z][\w=+#x-]+\b', raw_text)
        
        # Process exactly 7 moves (4 White, 3 Black)
        for i in range(min(7, len(moves))):
            turn = "W" if i % 2 == 0 else "B"
            ChessEngine.apply_san_move(board, moves[i], turn)
            
    except FileNotFoundError:
        return

    # It is now Black's turn. Calculate moves for the Black King (BK)
    all_m, leg_m, ill_m = ChessEngine.get_king_moves(board, "B")
    k_pos = next(pos for pos, p in board.pieces.items() if p == "BK")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : K{FILES[k_pos[0]]}{RANKS[k_pos[1]]}"
    ]

    with open(os.path.join(base_dir, "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()