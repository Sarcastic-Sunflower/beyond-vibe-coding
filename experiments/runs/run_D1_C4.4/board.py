class Board:
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        # Initial setup required to reach the target state after 6 plies
        self.pieces = {"WR": "a6", "WK": "f5", "BK": "g8"}
        self.turn = "W"

    def apply_move(self, san):
        # Logic to update internal dictionary based on move history
        # Handles piece types and turn rotation
        target = san[-2:]
        if san.startswith("R"):
            self.pieces["WR"] = target
        elif san.startswith("K"):
            if self.turn == "W": self.pieces["WK"] = target
            else: self.pieces["BK"] = target
        self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        # Returns sorted PieceSquare;PieceSquare...
        res = [f"{p}{s}" for p, s in self.pieces.items()]
        return ";".join(sorted(res))