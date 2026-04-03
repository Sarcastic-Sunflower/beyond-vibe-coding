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
        # Group by color, then sort by piece type (K, Q, R, B, N, P), then by square
        def sort_key(item):
            color = 0 if item[0] == "W" else 1
            # Piece priority: King first
            p_type = 0 if item[1] == "K" else 1
            return (color, p_type, item[2:])

        items = [f"{p}{FILES[c]}{RANKS[r]}" for (c, r), p in self.pieces.items()]
        return ";".join(sorted(items, key=sort_key))

    def is_on_board(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8