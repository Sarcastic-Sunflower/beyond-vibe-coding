class Board:
    """Manages 0-63 board indexing where a1=0, h1=7, a8=56, h8=63."""
    FILES = "abcdefgh"
    RANKS = "12345678"
    SQUARES = [f"{f}{r}" for r in RANKS for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(SQUARES)}

    def __init__(self):
        # Initial positions: WR: a6, WK: f5, BK: g8
        self.pieces = {"WR": self.SAN_TO_IDX["a6"], 
                       "WK": self.SAN_TO_IDX["f5"], 
                       "BK": self.SAN_TO_IDX["g8"]}
        self.turn = "W"

    def apply_move(self, san):
        target = san[-2:]
        if target in self.SAN_TO_IDX:
            idx = self.SAN_TO_IDX[target]
            if "R" in san: self.pieces["WR"] = idx
            elif "K" in san:
                if self.turn == "W": self.pieces["WK"] = idx
                else: self.pieces["BK"] = idx
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        res = [f"{p}{self.SQUARES[i]}" for p, i in self.pieces.items()]
        return ";".join(sorted(res))