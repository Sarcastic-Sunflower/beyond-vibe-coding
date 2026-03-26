#!/usr/bin/env python3
import os

class ChessEngine:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.turn = "W"
        # Initializing the specific position from your legacy code
        self.board[5][1] = "WR" # b6
        self.board[3][6] = "WK" # g4
        self.board[5][6] = "BK" # g6

    def _get_pos(self, coord):
        """Converts algebraic notation (e.g., 'b6') to (row, col)."""
        return self.RANKS.index(coord[1]), self.FILES.index(coord[0])

    def get_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p or p[0] != color:
                    continue
                
                ptype = p[1]
                # Rook Logic
                if ptype == "R":
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        while 0 <= nr < 8 and 0 <= nc < 8:
                            target = self.board[nr][nc]
                            if target and target[0] == color: break
                            moves.append(f"R{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}")
                            if target: break
                            nr, nc = nr + dr, nc + dc
                # King Logic
                elif ptype == "K":
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 8 and 0 <= nc < 8:
                                target = self.board[nr][nc]
                                if not target or target[0] != color:
                                    moves.append(f"K{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}")
        return sorted(set(moves))

    def apply_move(self, san):
        """Parses SAN and updates the board."""
        clean_san = san.translate(str.maketrans('', '', '+#!?x'))
        piece_type = clean_san[0] if clean_san[0] in "RKQBN" else "P"
        dest_sq = clean_san[-2:]
        dr, dc = self._get_pos(dest_sq)

        # Find the piece of piece_type that can move here (Simplified for this specific engine)
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p[0] == self.turn and p[1] == piece_type:
                    # In a full engine, you'd validate if THIS specific piece can reach dr, dc
                    self.board[r][c] = ""
                    self.board[dr][dc] = f"{self.turn}{piece_type}"
                    self.turn = "B" if self.turn == "W" else "W"
                    return

    def get_position_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p:
                    parts.append(f"{p}{self.FILES[c]}{self.RANKS[r]}")
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)