class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Initial position based on the provided legacy starting dict
        self.pieces = {
            (1, 6): "BK", (2, 3): "BN", (3, 5): "WP", 
            (4, 4): "WP", (0, 4): "WK"
        }

    def is_on_board(self, c, r):
        return 0 <= c < 8 and 0 <= r < 8

    def get_piece(self, c, r):
        return self.pieces.get((c, r))

    def get_position_string(self):
        res = [f"{p}{self.FILES[c]}{self.RANKS[r]}" for (c, r), p in self.pieces.items()]
        # Maintain legacy sorting: Color (W then B), then File, then Rank
        res.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(res)