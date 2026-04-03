import os
from board import ChessBoard
from move_logic import MoveProcessor, MoveGenerator

def main():
    board = ChessBoard()
    input_path = os.path.join(os.path.dirname(__file__), "moves2.txt")
    output_path = os.path.join(os.path.dirname(__file__), "output2.txt")
    
    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            # Extract moves, ignoring move numbers/tags
            raw_content = f.read()
            moves = re.findall(r'[a-zA-Z][\w=+#x-]+', raw_content)
        
        # Process the 7 moves (White: 4, Black: 3)
        turn = "W"
        for i in range(min(7, len(moves))):
            MoveProcessor.apply_san(board, moves[i], turn)
            turn = "B" if turn == "W" else "W"

    # Generate moves for Black (it is now Black's turn)
    all_m, leg_m, ill_m = MoveGenerator.get_black_moves(board)

    output = [
        board.get_position_string(),
        f"{len(all_m)} : {';'.join(all_m)}",
        f"{len(leg_m)} : {';'.join(leg_m)}",
        f"{len(ill_m)} : {';'.join(ill_m)}"
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(output) + "\n")

if __name__ == "__main__":
    import re
    main()