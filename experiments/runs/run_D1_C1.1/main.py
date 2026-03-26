import os
import sys
from chess_engine import ChessBoard

def process_game():
    board = ChessBoard()
    
    # Path Resolution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")
    output_path = os.path.join(script_dir, "output1.txt")

    # Read and process moves from file
    if os.path.exists(input_path):
        with open(input_path, 'r', encoding='utf-8') as f:
            all_content = f.read().split() # Split by whitespace to get individual moves
            
            # Process strictly the next 3 moves if available
            for move in all_content[:3]:
                board.make_move(move)

    # Generate Output Data
    pos_str = board.get_position_string()
    available_moves = board.get_all_moves(board.turn)
    move_count = len(available_moves)
    move_list_str = ";".join(available_moves)
    
    formatted_moves = f"{move_count} :" + (f" {move_list_str}" if available_moves else "")

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{pos_str}\n")      # Line 1: Current Position
        f.write(f"{formatted_moves}\n") # Line 2: Moves for current turn
        f.write(f"{formatted_moves}\n") # Line 3: Duplicate per legacy format
        f.write(f"{formatted_moves}\n") # Line 4: Corrected logical output

if __name__ == "__main__":
    process_game()