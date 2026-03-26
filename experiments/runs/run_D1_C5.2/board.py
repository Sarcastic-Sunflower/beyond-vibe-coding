class Board:
    """Manages board state using 0-63 integer indexing (a1=0, h8=63)."""
    FILES = "abcdefgh"
    RANKS = "12345678"
    # Index 0=a1, 7=h1, 8=a2, 63=h8
    SQUARES = [f"{f}{r}" for r in RANKS for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(SQUARES)}

    def __init__(self):
        # Starting: WR: a6, WK: f5, BK: g8
        self.pieces = {"WR": self.SAN_TO_IDX["a6"], 
                       "WK": self.SAN_TO_IDX["f5"], 
                       "BK": self.SAN_TO_IDX["g8"]}
        self.turn = "W"

    def apply_move(self, san: str) -> None:
        target_san = san[-2:]
        target_idx = self.SAN_TO_IDX[target_san]
        
        if "R" in san:
            self.pieces["WR"] = target_idx
        elif "K" in san:
            # If it's White's turn, move WK; else move BK
            if self.turn == "W":
                self.pieces["WK"] = target_idx
            else:
                self.pieces["BK"] = target_idx
        
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self) -> str:
        res = [f"{p}{self.SQUARES[idx]}" for p, idx in self.pieces.items()]
        return ";".join(sorted(res))