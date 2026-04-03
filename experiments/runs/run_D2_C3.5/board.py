class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"
    FILES_INDEX = {f: i for i, f in enumerate(FILES)}
    RANKS_INDEX = {r: i for i, r in enumerate(RANKS)}

    def __init__(self):
        # Coordinates as tuples (col, row) for hash-map speed
        self.pieces = {
            (0, 3): "WK", (3, 3): "WP",
            (1, 6): "BK", (2, 3): "BN"
        }

    def get_position_string(self):
        # Optimized sorting using a single-pass lambda
        items = sorted(
            [f"{p}{self.FILES[c]}{self.RANKS[r]}" for (c, r), p in self.pieces.items()],
            key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2])
        )
        return ";".join(items)

    def is_occupied_by_color(self, pos, color):
        p = self.pieces.get(pos)
        return p is not None and p[0] == color