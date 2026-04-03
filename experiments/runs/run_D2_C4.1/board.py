from constants import FILES, RANKS

class ChessBoard:
    FILES_INDEX = {f: i for i, f in enumerate(FILES)}
    RANKS_INDEX = {r: i for i, r in enumerate(RANKS)}

    def __init__(self):
        # Initial state as defined in your legacy code
        self.pieces = {
            (0, 3): "WK", (3, 3): "WP",
            (1, 6): "BK", (2, 3): "BN"
        }

    def get_position_string(self):
        # Sorts by Color (W then B), then Piece Type, then Square
        items = sorted(
            [f"{p}{FILES[c]}{RANKS[r]}" for (c, r), p in self.pieces.items()],
            key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2])
        )
        return ";".join(items)

    def is_on_board(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8