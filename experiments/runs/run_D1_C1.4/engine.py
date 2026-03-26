#!/usr/bin/env python3

class ChessEngine:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Setup initial board state
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "W"
        self.board[5][1] = "WR" # b6
        self.board[3][6] = "WK" # g4
        self.board[5][6] = "BK" # g6

    def _to_idx(self, coord):
        """Converts 'b6' to (row_idx, col_idx)."""
        return self.RANKS.index(coord[1]), self.FILES.index(coord[0])

    def apply_move(self, san):
        """Standard Algebraic Notation parser."""
        if not san: return
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        dest_sq = san[-2:]
        tr, tc = self._to_idx(dest_sq)

        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p[0] == self.turn and p[1] == piece_type:
                    self.board[r][c] = None
                    self.board[tr][tc] = f"{self.turn}{piece_type}"
                    self.turn = "B" if self.turn == "W" else "W"
                    return

    def get_moves(self, color):
        """Generates move list matching the expected logic."""
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p or p[0] != color: continue
                
                ptype = p[1]
                if ptype == "R":
                    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                        nr, nc = r + dr, c + dc
                        while 0 <= nr < 8 and 0 <= nc < 8:
                            target = self.board[nr][nc]
                            if target and target[0] == color: break
                            # Logic: Include 'x' for captures
                            move_str = f"R{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}"
                            moves.append(move_str)
                            if target: break
                            nr, nc = nr + dr, nc + dc
                elif ptype == "K":
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 8 and 0 <= nc < 8:
                                target = self.board[nr][nc]
                                if not target or target[0] != color:
                                    move_str = f"K{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}"
                                    moves.append(move_str)
        return sorted(list(set(moves)))

    def get_position_string(self):
        res = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c]:
                    res.append(f"{self.board[r][c]}{self.FILES[c]}{self.RANKS[r]}")
        res.sort() 
        return ";".join(res)