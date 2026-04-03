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
        
        # Process moves: 4 for White, 3 for Black
        turn = "W"
        for i in range(min(7, len(moves))):
            ChessEngine.apply_san_move(board, moves[i], turn)
            turn = "B" if turn == "W" else "W"

    # Generate Black's moves (Black's turn after 7 moves)
    all_m, leg_m, ill_m = ChessEngine.get_king_moves(board, "B")

    # Final Output Formatting
    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}"
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()