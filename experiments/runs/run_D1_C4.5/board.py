class Board:
    """Manages board state using 0-63 integer indexing for speed."""
    # Maps for fast conversion between string and integer
    FILES = "abcdefgh"
    RANKS = "12345678"
    SQUARES = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(SQUARES)}

    def __init__(self):
        # Initial positions: WR: a6 (40), WK: f5 (37), BK: g8 (62)
        self.pieces = {"WR": 40, "WK": 37, "BK": 62}
        self.turn = "W"

    def apply_move(self, san: str) -> None:
        """Updates piece positions using integer indexing."""
        target_idx = self.SAN_TO_IDX[san[-2:]]
        prefix = san[0]
        
        if prefix == "R":
            self.pieces["WR"] = target_idx
        elif prefix == "K":
            if self.turn == "W":
                self.pieces["WK"] = target_idx
            else:
                self.pieces["BK"] = target_idx
        
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self) -> str:
        """Constructs the output state string efficiently."""
        res = [f"{p}{self.SQUARES[idx]}" for p, idx in self.pieces.items()]
        res.sort()
        return ";".join(res)