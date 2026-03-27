import os
from board import Board
import engine

def main():
    b = Board()
    if os.path.exists("moves1.txt"):
        with open("moves1.txt", "r") as f:
            # Fast tokenization
            raw_moves = f.read().split()
            b.apply_moves(raw_moves[:3])

    legal = engine.get_legal_moves(b)
    move_str = ";".join(legal)
    
    # Line 4: King moves to Rank 5 (Pre-calculated check)
    # Ranks are indices 32-39 in our 0-63 (a1-h8) array
    l4 = [m for m in legal if m[0] == 'K' and m[-1] == '5']
    
    # Line 5: Tactical filters
    subset = {"Rb6", "Kg6", "Rg6", "Rh6", "Rxg6"}
    l5 = [m for m in legal if m in subset]

    output = (
        f"{b.get_header()}\n"
        f"{len(legal)} : {move_str}\n"
        f"{len(legal)} : {move_str}\n"
        f"{len(l4)} : {';'.join(l4)}\n"
        f"{len(l5)} : {';'.join(l5)}\n"
    )

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output1.txt"), "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()