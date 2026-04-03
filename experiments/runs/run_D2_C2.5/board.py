class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Piece representation: (col, row) -> "Type"
        self.pieces = {
            (1, 6): "BK", (2, 3): "BN", (3, 5): "WP", 
            (4, 4): "WP", (0, 4): "WK"
        }

    def get_position_string(self):
        # Faster sorted join using generator expression
        items = sorted(
            [f"{p}{self.FILES[c]}{self.RANKS[r]}" for (c, r), p in self.pieces.items()],
            key=lambda x: (x[0] != "W", x[1], x[2:])
        )
        return ";".join(items)