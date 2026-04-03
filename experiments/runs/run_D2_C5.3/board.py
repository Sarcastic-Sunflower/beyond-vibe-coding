from constants import FILES, RANKS

class ChessBoard:
    def __init__(self):
        # Initial state: White King a4, White Pawn d4; Black King b7, Black Knight c4
        self.pieces = {
            (3, 0): "WK", (3, 3): "WP", 
            (6, 1): "BK", (3, 2): "BN"
        }

    def get_piece(self, r, f):
        return self.pieces.get((r, f))

    def move_piece(self, start, end, piece):
        if start in self.pieces:
            del self.pieces[start]
        self.pieces[end] = piece

    def get_position_string(self):
        w_king, b_king, w_others, b_others = [], [], [], []
        for r in range(8):
            for f in range(8):
                p = self.get_piece(r, f)
                if not p: continue
                sq = f"{FILES[f]}{RANKS[r]}"
                if p == "WK": w_king.append(f"WK{sq}")
                elif p == "BK": b_king.append(f"BK{sq}")
                elif p.startswith("W"): w_others.append(f"{p}{sq}")
                else: b_others.append(f"{p}{sq}")
        # Legacy format: WK;WhiteOthers;BK;BlackOthers
        return ";".join(w_king + sorted(w_others) + b_king + sorted(b_others))