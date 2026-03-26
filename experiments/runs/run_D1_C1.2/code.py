#!/usr/bin/env python3
import sys
import os

class ChessEngine:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Initialize board as per legacy setup 
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.board[5][1] = "WR" # b6
        self.board[3][6] = "WK" # g4
        self.board[5][6] = "BK" # g6
        self.turn = "W"

    def get_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p or p[0] != color:
                    continue
                
                # Rook Logic: Slide until edge or piece 
                if p[1] == "R":
                    for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nc, nr = c + dc, r + dr
                        while 0 <= nc <= 7 and 0 <= nr <= 7:
                            tp = self.board[nr][nc]
                            if tp and tp[0] == color: break
                            moves.append(f"R{'x' if tp else ''}{self.FILES[nc]}{self.RANKS[nr]}")
                            if tp: break
                            nc, nr = nc + dc, nr + dr
                
                # King Logic: One square in any direction 
                elif p[1] == "K":
                    for dc in [-1, 0, 1]:
                        for dr in [-1, 0, 1]:
                            if dc == 0 and dr == 0: continue
                            nc, nr = c + dc, r + dr
                            if 0 <= nc <= 7 and 0 <= nr <= 7:
                                tp = self.board[nr][nc]
                                if not tp or tp[0] != color:
                                    moves.append(f"K{'x' if tp else ''}{self.FILES[nc]}{self.RANKS[nr]}")
        return sorted(set(moves))

    def apply_move(self, san):
        """Processes a single SAN move and updates the board."""
        clean_san = san.translate(str.maketrans('', '', '+#!?'))
        pt = clean_san[0] if clean_san[0] in "RKQBN" else "P"
        dest = clean_san[-2:]
        dr, dc = self.RANKS.index(dest[1]), self.FILES.index(dest[0])
        
        # Find the specific piece of the current turn's color that can reach 'dest'
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p[0] == self.turn and p[1] == pt:
                    # Move the piece 
                    self.board[r][c] = ""
                    self.board[dr][dc] = p
                    self.turn = "B" if self.turn == "W" else "W"
                    return

    def get_pos_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p: parts.append(f"{p}{self.FILES[c]}{self.RANKS[r]}")
        # Legacy sorting: Color, Type, then Position 
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)

def main():
    engine = ChessEngine()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    # Requirement: Process the next 3 moves from the file
    if os.path.isfile(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            # Flatten all moves in the file into a list
            all_moves = f.read().split()
            for mv in all_moves[:3]:
                engine.apply_move(mv)

    # Line 1: Final Position
    pos = engine.get_pos_string()
    # Lines 2-4: Possible moves for the current turn 
    mvs = engine.get_moves(engine.turn)
    move_line = f"{len(mvs)} :" + (f" {';'.join(mvs)}" if mvs else "")

    with open(os.path.join(script_dir, "output1.txt"), "w", encoding="utf-8") as f:
        f.write(pos + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n") # Corrected Line 4 logic

if __name__ == "__main__":
    main()