class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"
    # Pre-compute coordinate mapping to avoid repeated index calls
    COORDS = {f"{f}{r}": (fi, ri) for ri, r in enumerate(RANKS) for fi, f in enumerate("abcdefgh")}
    INV_COORDS = {v: k for k, v in COORDS.items()}

    def __init__(self):
        # Use a dict for O(1) access to active pieces
        self.pieces = {
            (1, 6): "BK", (2, 3): "BN", (3, 5): "WP", 
            (4, 4): "WP", (0, 4): "WK"
        }

    def parse_san(self, san, color):
        san = san.translate(str.maketrans('', '', '+#x'))
        promotion = san.split('=')[1] if '=' in san else None
        san = san.split('=')[0]
        
        dest_sq = san[-2:]
        dest_coord = (self.FILES.index(dest_sq[0]), self.RANKS.index(dest_sq[1]))
        p_type = san[0] if san[0] in "RKQBN" else "P"

        # Search only active pieces instead of the whole grid 
        for coord, p_info in list(self.pieces.items()):
            if p_info[0] == color and p_info[1] == p_type:
                # Pawn disambiguation logic 
                if p_type == "P":
                    if (dest_coord[1] - coord[1]) * (1 if color == "W" else -1) <= 0:
                        continue
                
                del self.pieces[coord]
                self.pieces[dest_coord] = f"{color}{promotion or p_type}"
                return

    def get_position_string(self):
        # Efficiently sort and join using list comprehension 
        res = [f"{p}{self.FILES[c]}{self.RANKS[r]}" for (c, r), p in self.pieces.items()]
        res.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(res)