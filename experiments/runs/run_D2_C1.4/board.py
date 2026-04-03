class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_initial_pos()

    def _setup_initial_pos(self):
        self.grid[6][1] = "BK"  # b7
        self.grid[3][2] = "BN"  # c4
        self.grid[5][3] = "WP"  # d6
        self.grid[4][4] = "WP"  # e5
        self.grid[4][0] = "WK"  # a5

    def parse_san(self, san, color):
        # Remove notation symbols
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
                    # Logic to ensure the correct pawn is chosen
                    if piece_type == "P":
                        direction = 1 if color == "W" else -1
                        if (dest_r - r) * direction <= 0:
                            continue
                    
                    # Update board
                    self.grid[r][c] = None
                    self.grid[dest_r][dest_c] = f"{color}{promotion if promotion else piece_type}"
                    return

    def get_position_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    # Format: Piece+Color+Square (e.g., WKa5)
                    parts.append(f"{p}{self.FILES[c]}{self.RANKS[r]}")
        # Standard sorting: White then Black, then piece type, then coordinate
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)