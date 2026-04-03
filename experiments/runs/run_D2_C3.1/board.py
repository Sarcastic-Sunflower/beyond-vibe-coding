class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Initializing the board based on the provided starting state
        self.pieces = {
            (1, 6): "BK", (2, 3): "BN", (3, 4): "WP", 
            (4, 3): "WP", (0, 3): "WK"
        }

    def get_position_string(self):
        # Keeps the exact legacy sorting logic: White first, then Black, then rank/file
        items = sorted(
            [f"{p}{self.FILES[c]}{self.RANKS[r]}" for (c, r), p in self.pieces.items()],
            key=lambda x: (x[0] != "W", x[1], x[2:])
        )
        return ";".join(items)

    def is_occupied_by_color(self, pos, color):
        piece = self.pieces.get(pos)
        return piece is not None and piece.startswith(color)