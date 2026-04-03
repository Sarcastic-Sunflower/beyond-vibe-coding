import os
import re
from board import ChessBoard
from engine import ChessEngine

def main():
    board = ChessBoard()
    base_dir = os.path.dirname(__file__)
    input_path = os.path.join(base_dir, "moves2.txt")
    output_path = os.path.join(base_dir, "output2.txt")
    
    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            content = f.read()
            # Regex to find SAN moves while ignoring move numbers
            moves = re.findall(r'(?<!\d\.)\b[a-zA-Z][\w=+#x-]+', content)
    
    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            # Better SAN extraction to handle 'd7' and 'e7' correctly
            raw = f.read()
            moves = re.findall(r'[a-zA-Z][\w=+#x-]+', raw)
        
        turn = "W"
        for i in range(min(7, len(moves))):
            ChessEngine.apply_san_move(board, moves[i], turn)
            turn = "B" if turn == "W" else "W"

    all_m, leg_m, ill_m = ChessEngine.get_king_moves(board, "B")
    
    # Check if the current position of the Black King is under attack
    k_pos = next(pos for pos, p in board.pieces.items() if p == "BK")
    is_checked = ChessEngine.is_square_attacked(board, k_pos, "B")

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}",
        f"1 : K{board.FILES[k_pos[0]]}{board.RANKS[k_pos[1]]}" # Required Reference Line
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()