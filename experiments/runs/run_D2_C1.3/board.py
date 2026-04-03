class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_initial_pos()

    def _setup_initial_pos(self):
        # Initial positions from legacy script
        self.grid[6][1] = "BK"  # b7
        self.grid[3][2] = "BN"  # c4
        self.grid[5][3] = "WP"  # d6
        self.grid[4][4] = "WP"  # e5
        self.grid[4][0] = "WK"  # a5

    def parse_san(self, san, color):
        san = san.replace("+", "").replace("#", "").replace("x", "")
        promotion = None
        if "=" in san:
            san, promotion = san.split("=")

        dest_str = san[-2:]
        dest_c = self.FILES.index(dest_str[0])
        dest_r = self.RANKS.index(dest_str[1])
        piece_type = san[0] if san[0] in "RKQBN" else "P"

        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p[0] == color and p[1] == piece_type:
                    # Specific logic for pawns: they only move forward
                    if piece_type == "P":
                        direction = 1 if color == "W" else -1
                        # Check if this pawn can actually reach the target rank
                        if (dest_r - r) * direction <= 0:
                            continue
                    
                    self.grid[r][c] = None
                    self.grid[dest_r][dest_c] = f"{color}{promotion if promotion else piece_type}"
                    return

    def get_position_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    parts.append(f"{p}{self.FILES[c]}{self.RANKS[r]}")
        # Sort W then B, then Piece type, then Square
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)