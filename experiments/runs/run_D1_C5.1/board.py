class Board:
    """Manages board state using 0-63 integer indexing (a1=0, h8=63)."""
    FILES = "abcdefgh"
    RANKS = "12345678"
    # Generate squares such that index 0 is a1, index 8 is a2, etc.
    SQUARES = [f"{f}{r}" for r in RANKS for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(SQUARES)}

    def __init__(self):
        # Initial positions adjusted to match the 0-63 coordinate system
        # WR: a6, WK: f5, BK: g8
        self.pieces = {"WR": self.SAN_TO_IDX["a6"], 
                       "WK": self.SAN_TO_IDX["f5"], 
                       "BK": self.SAN_TO_IDX["g8"]}
        self.turn = "W"

    def apply_move(self, san: str) -> None:
        """Updates piece positions. Handles captures (x) and piece prefixes."""
        target_san = san[-2:]
        target_idx = self.SAN_TO_IDX[target_san]
        
        if san.startswith("R"):
            self.pieces["WR"] = target_idx
        elif san.startswith("K"):
            if self.turn == "W":
                self.pieces["WK"] = target_idx
            else:
                self.pieces["BK"] = target_idx
        
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self) -> str:
        """Returns sorted piece positions: 'BKg8;WKf5;WRa6'"""
        res = [f"{p}{self.SQUARES[idx]}" for p, idx in self.pieces.items()]
        return ";".join(sorted(res))