class Board:
    FILES = "abcdefgh"
    RANKS = "12345678"
    SQUARES = [f"{f}{r}" for r in RANKS for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(SQUARES)}

    def __init__(self):
        self.pieces = {"WR": self.SAN_TO_IDX["a6"], 
                       "WK": self.SAN_TO_IDX["f5"], 
                       "BK": self.SAN_TO_IDX["g8"]}
        self.turn = "W"

    def apply_move(self, san):
        target_idx = self.SAN_TO_IDX[san[-2:]]
        if "R" in san:
            self.pieces["WR"] = target_idx
        elif "K" in san:
            if self.turn == "W":
                self.pieces["WK"] = target_idx
            else:
                self.pieces["BK"] = target_idx
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        res = [f"{p}{self.SQUARES[idx]}" for p, idx in self.pieces.items()]
        return ";".join(sorted(res))