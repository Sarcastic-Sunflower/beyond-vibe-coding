from constants import FILES, RANKS

class ChessBoard:
    def __init__(self):
        # Dictionary lookup is more efficient for sparse boards
        self.pieces = {
            (3, 0): "WK",  # a4
            (3, 3): "WP",  # d4
            (6, 1): "BK",  # b7
            (3, 2): "BN",  # c4
        }

    def get_piece(self, r, f):
        return self.pieces.get((r, f))

    def move_piece(self, start, end, piece):
        if start in self.pieces:
            del self.pieces[start]
        self.pieces[end] = piece

    def get_position_string(self):
        w_king, b_king, w_others, b_others = [], [], [], []
        
        # Sort by rank then file to maintain consistent output
        for r in range(8):
            for f in range(8):
                p = self.get_piece(r, f)
                if not p: continue
                
                sq = f"{FILES[f]}{RANKS[r]}"
                if p == "WK": w_king.append(f"WK{sq}")
                elif p == "BK": b_king.append(f"BK{sq}")
                elif p.startswith("W"): w_others.append(f"{p}{sq}")
                else: b_others.append(f"{p}{sq}")
        
        return ";".join(w_king + sorted(w_others) + b_king + sorted(b_others))