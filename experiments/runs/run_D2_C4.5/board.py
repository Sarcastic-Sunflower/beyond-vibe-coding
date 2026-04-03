from constants import FILES, RANKS

class ChessBoard:
    def __init__(self):
        # Flattened board: index = rank * 8 + file
        self.state = [None] * 64
        self.state[3 * 8 + 0] = "WK"  # a4
        self.state[3 * 8 + 3] = "WP"  # d4
        self.state[6 * 8 + 1] = "BK"  # b7
        self.state[3 * 8 + 2] = "BN"  # c4

    def get_position_string(self):
        w_king, b_king = [], []
        w_others, b_others = [], []
        
        for i, p in enumerate(self.state):
            if not p: continue
            square = f"{FILES[i % 8]}{RANKS[i // 8]}"
            if p == "WK": w_king.append(f"WK{square}")
            elif p == "BK": b_king.append(f"BK{square}")
            elif p[0] == "W": w_others.append(f"{p}{square}")
            else: b_others.append(f"{p}{square}")
            
        # Strict sort: WK, White others, BK, Black others
        return ";".join(w_king + sorted(w_others) + b_king + sorted(b_others))