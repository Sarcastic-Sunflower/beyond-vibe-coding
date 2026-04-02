import os
from board_engine import ChessBoard

def main():
    board = ChessBoard()
    board.setup_initial()

    # Read moves
    moves_path = "moves2.txt"
    if os.path.exists(moves_path):
        with open(moves_path, "r") as f:
            # Flatten moves and filter turn numbers
            raw_content = f.read().split()
            moves = [m for m in raw_content if not m.endswith(".")]
            
        # Process the next 3 moves as requested
        turn_color = "W"
        for i in range(min(3, len(moves))):
            board.move_piece(moves[i], turn_color)
            turn_color = "B" if turn_color == "W" else "W"

    # Generate Output
    pos = board.get_position_string()
    all_m, leg_m, ill_m = board.get_black_moves()

    def format_line(mvs):
        return f"{len(mvs)} : " + ";".join(mvs) if mvs else "0 :"

    with open("output2.txt", "w") as f:
        f.write(pos + "\n")
        f.write(format_line(all_m) + "\n")
        f.write(format_line(leg_m) + "\n")
        f.write(format_line(ill_m) + "\n")

if __name__ == "__main__":
    main()