# board.py
FILES = "abcdefgh"
RANKS = "12345678"

class Board:
    def __init__(self):
        self.grid = {(f, r): None for f in FILES for r in RANKS}

    def setup_initial(self):
        # Initial positions matching the legacy setup
        self.grid[("b", "6")] = "WR"
        self.grid[("g", "4")] = "WK"
        self.grid[("g", "6")] = "BK"

    def get_piece(self, f, r):
        return self.grid.get((f, r))

    def set_piece(self, f, r, piece):
        self.grid[(f, r)] = piece

    def find_pieces(self, color, ptype):
        res = []
        for (f, r), p in self.grid.items():
            if p == color + ptype:
                res.append((f, r))
        return res

    def move_piece(self, start, end):
        p = self.grid[start]
        self.grid[start] = None
        self.grid[end] = p

    def apply_san_move(self, san, color):
        """Simplistic parser to map SAN to the dict grid."""
        san = san.strip().replace("+", "").replace("#", "").replace("x", "")
        if len(san) < 2: 
            return
            
        ptype = san[0] if san[0] in "RKQBN" else "P"
        dest_f, dest_r = san[-2], san[-1]
        
        # Find the acting piece and force the move (legacy parsing behavior)
        pieces = self.find_pieces(color, ptype)
        if pieces:
            start = pieces[0]
            self.move_piece(start, (dest_f, dest_r))

    def copy(self):
        new_board = Board()
        new_board.grid = self.grid.copy()
        return new_board

    def pos_string(self):
        parts = [p + f + r for (f, r), p in self.grid.items() if p]
        # Keeps exact legacy sorting behavior for the output file
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)