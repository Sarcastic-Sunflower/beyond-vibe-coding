import os, re
from board import ChessBoard
from engine import ChessEngine

def main():
    board = ChessBoard()
    base_dir = os.path.dirname(__file__)
    
    # Process inputs
    try:
        with open(os.path.join(base_dir, "moves2.txt"), "r") as f:
            # Single-pass move extraction 
            moves = re.findall(r'[a-zA-Z][\w=+#x-]+', f.read())
        
        turn = "W"
        for i in range(min(7, len(moves))):
            ChessEngine.apply_san_move(board, moves[i], turn)
            turn = "B" if turn == "W" else "W"
            
    except FileNotFoundError:
        return

    # Generate results for Black 
    all_m, leg_m, ill_m = ChessEngine.get_king_moves(board, "B")
    k_pos = next(pos for pos, p in board.pieces.items() if p == "BK")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : K{board.FILES[k_pos[0]]}{board.RANKS[k_pos[1]]}"
    ]

    with open(os.path.join(base_dir, "output2.txt"), "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()