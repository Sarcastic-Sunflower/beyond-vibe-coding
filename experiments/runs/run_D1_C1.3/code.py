#!/usr/bin/env python3
import sys
import os

class ChessEngine:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Initialize internal board state 
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.board[5][1] = "WR"  # b6
        self.board[3][6] = "WK"  # g4
        self.board[5][6] = "BK"  # g6
        self.turn = "W"

    def get_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p or p[0] != color:
                    continue
                
                # Rook: Sliding moves
                if p[1] == "R":
                    for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nc, nr = c + dc, r + dr
                        while 0 <= nc <= 7 and 0 <= nr <= 7:
                            tp = self.board[nr][nc]
                            if tp and tp[0] == color: break
                            moves.append(f"R{'x' if tp else ''}{self.FILES[nc]}{self.RANKS[nr]}")
                            if tp: break
                            nc, nr = nc + dc, nr + dr
                
                # King: Step moves
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
        """Update board state based on SAN input."""
        s = san.translate(str.maketrans('', '', '+#!?'))
        pt = s[0] if s[0] in "RKQBN" else "P"
        dest = s[-2:]
        dr, dc = self.RANKS.index(dest[1]), self.FILES.index(dest[0])
        
        # Locate the piece of the current turn's color to move
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p[0] == self.turn and p[1] == pt:
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
        # Sort by Color (W then B), then Piece Type, then Square 
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)

def main():
    engine = ChessEngine()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    # Requirement: Process strictly the next 3 moves from the file 
    if os.path.isfile(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            # Tokenize all moves to handle varying whitespace/line breaks 
            content = f.read().split()
            for mv in content[:3]:
                engine.apply_move(mv)

    pos = engine.get_pos_string()
    mvs = engine.get_moves(engine.turn)
    move_line = f"{len(mvs)} :" + (f" {';'.join(mvs)}" if mvs else "")

    # Output to output1.txt with corrected Line 4 logic 
    with open(os.path.join(script_dir, "output1.txt"), "w", encoding="utf-8") as f:
        f.write(pos + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n")

if __name__ == "__main__":
    main()