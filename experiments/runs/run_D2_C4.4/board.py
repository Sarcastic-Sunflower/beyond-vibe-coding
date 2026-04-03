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
        # Specific sort: White King, then other White, then Black King, then other Black
        def sort_key(item):
            color_val = 0 if item[0] == 'W' else 1
            piece_val = 0 if item[1] == 'K' else 1
            return (color_val, piece_val, item[2:]) # Sort by color, then K-priority, then square

        items = [f"{p}{FILES[c]}{RANKS[r]}" for (c, r), p in self.pieces.items()]
        return ";".join(sorted(items, key=sort_key))

    def is_on_board(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8