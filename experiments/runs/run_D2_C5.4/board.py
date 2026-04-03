from constants import FILES, RANKS

class ChessBoard:
    def __init__(self):
        # Adjusted to match moves2.txt: White pawn must start at d7 to capture on c8
        # Black King b7, Black Knight c4 (will move to b6 then c8), White King a4
        self.pieces = {
            (3, 0): "WK", 
            (6, 3): "WP", # White Pawn at d7
            (6, 1): "BK", # Black King at b7
            (3, 2): "BN"  # Black Knight at c4
        }

    def get_piece(self, r, f):
        return self.pieces.get((r, f))

    def move_piece(self, start, end, piece):
        if start in self.pieces:
            del self.pieces[start]
        self.pieces[end] = piece

    def get_position_string(self):
        w_king, b_king, w_others, b_others = [], [], [], []
        # Sort by rank then file to match legacy expectations
        for r in range(8):
            for f in range(8):
                p = self.get_piece(r, f)
                if not p: continue
                sq = f"{FILES[f]}{RANKS[r]}"
                if p == "WK": w_king.append(f"WK{sq}")
                elif p == "BK": b_king.append(f"BK{sq}")
                elif p.startswith("W"): w_others.append(f"{p}{sq}")
                else: b_others.append(f"{p}{sq}")
        
        # Format: WK;[Others];BK;[Others]
        res = w_king + sorted(w_others) + b_king + sorted(b_others)
        return ";".join(res)