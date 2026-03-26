# engine.py
class ChessEngine:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        self.board = {} # (col, row) -> "WR", "BK", etc.
        self.turn = "W"

    def setup_initial(self):
        # Initial state from legacy code
        # board[5][1] = "WR" -> b6
        # board[3][6] = "WK" -> g4
        # board[5][6] = "BK" -> g6
        self.set_piece("b6", "WR")
        self.set_piece("g4", "WK")
        self.set_piece("g6", "BK")

    def set_piece(self, square, piece):
        c = self.FILES.index(square[0])
        r = self.RANKS.index(square[1])
        self.board[(c, r)] = piece

    def get_piece(self, c, r):
        return self.board.get((c, r))

    def parse_and_move(self, san, color):
        s = san.strip().replace("x", "").replace("+", "").replace("#", "")
        if not s: return
        
        pt = s[0] if s[0] in "RKQBN" else "P"
        dest = s[-2:]
        dc = self.FILES.index(dest[0])
        dr = self.RANKS.index(dest[1])
        
        # Find the piece to move
        source = None
        for (c, r), p in self.board.items():
            if p == color + pt:
                source = (c, r)
                break
        
        if source:
            del self.board[source]
            self.board[(dc, dr)] = color + pt
            self.turn = "B" if color == "W" else "W"

    def is_square_attacked(self, c, r, attacker_color):
        for (pc, pr), p in self.board.items():
            if p[0] != attacker_color: continue
            
            pt = p[1]
            if pt == "R":
                if pc == c or pr == r:
                    # Check blockers
                    blocked = False
                    if pc == c:
                        step = 1 if r > pr else -1
                        for i in range(pr + step, r, step):
                            if self.get_piece(c, i):
                                blocked = True
                                break
                    else:
                        step = 1 if c > pc else -1
                        for i in range(pc + step, c, step):
                            if self.get_piece(i, r):
                                blocked = True
                                break
                    if not blocked: return True
            elif pt == "K":
                if abs(pc - c) <= 1 and abs(pr - r) <= 1:
                    return True
        return False

    def get_legal_moves(self, color):
        moves = []
        enemy = "B" if color == "W" else "W"
        
        # Find King for check detection
        king_pos = None
        for (c, r), p in self.board.items():
            if p == color + "K":
                king_pos = (c, r)
                break

        for (c, r), p in self.board.items():
            if p[0] != color: continue
            
            pt = p[1]
            if pt == "R":
                for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nc, nr = c + dc, r + dr
                    while 0 <= nc < 8 and 0 <= nr < 8:
                        target = self.get_piece(nc, nr)
                        if target:
                            if target[0] != color:
                                if not self.leaves_king_in_check(c, r, nc, nr, color, king_pos):
                                    moves.append(f"Rx{self.FILES[nc]}{self.RANKS[nr]}")
                            break
                        else:
                            if not self.leaves_king_in_check(c, r, nc, nr, color, king_pos):
                                moves.append(f"R{self.FILES[nc]}{self.RANKS[nr]}")
                        nc += dc
                        nr += dr
            elif pt == "K":
                for dc in [-1, 0, 1]:
                    for dr in [-1, 0, 1]:
                        if dc == 0 and dr == 0: continue
                        nc, nr = c + dc, r + dr
                        if 0 <= nc < 8 and 0 <= nr < 8:
                            target = self.get_piece(nc, nr)
                            if not target or target[0] != color:
                                # King cannot move into check or adjacent to enemy King
                                if not self.is_square_attacked(nc, nr, enemy):
                                    moves.append(f"K{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}")
        
        return sorted(list(set(moves)))

    def leaves_king_in_check(self, sc, sr, dc, dr, color, king_pos):
        piece = self.board[(sc, sr)]
        target = self.board.get((dc, dr))
        
        del self.board[(sc, sr)]
        self.board[(dc, dr)] = piece
        
        # Update king_pos if we moved the king
        actual_king_pos = (dc, dr) if piece[1] == "K" else king_pos
        
        in_check = self.is_square_attacked(actual_king_pos[0], actual_king_pos[1], "B" if color == "W" else "W")
        
        # Restore
        self.board[(sc, sr)] = piece
        if target:
            self.board[(dc, dr)] = target
        else:
            del self.board[(dc, dr)]
            
        return in_check

    def get_position_string(self):
        parts = []
        for (c, r), p in self.board.items():
            parts.append(p + self.FILES[c] + self.RANKS[r])
        # Sort by color (W=0, B=1), then piece type (K < R), then square
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)
