from constants import FILES, RANKS

class ChessBoard:
    __slots__ = ['pieces'] # Optimization: limit memory footprint

    def __init__(self):
        # Initializing 64-square board
        self.pieces = [None] * 64
        # WK a4, WP d7, BK b7, BN c4
        self.pieces[24] = "WK"  # (3,0)
        self.pieces[51] = "WP"  # (6,3)
        self.pieces[49] = "BK"  # (6,1)
        self.pieces[26] = "BN"  # (3,2)

    def move_piece(self, start_idx, end_idx, piece):
        self.pieces[start_idx] = None
        self.pieces[end_idx] = piece

    def get_position_string(self):
        w_king, b_king, w_others, b_others = [], [], [], []
        for i, p in enumerate(self.pieces):
            if not p: continue
            sq = f"{FILES[i % 8]}{RANKS[i // 8]}"
            if p == "WK": w_king.append(f"WK{sq}")
            elif p == "BK": b_king.append(f"BK{sq}")
            elif p.startswith("W"): w_others.append(f"{p}{sq}")
            else: b_others.append(f"{p}{sq}")
        
        return ";".join(w_king + sorted(w_others) + b_king + sorted(b_others))