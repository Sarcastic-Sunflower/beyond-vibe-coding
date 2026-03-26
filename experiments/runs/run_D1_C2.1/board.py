class Board:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Piece tracking: {index: "WR"} for faster access than full board scans
        self.pieces = {41: "WR", 30: "WK", 46: "BK"}
        self.turn = "W"

    def to_idx(self, coord):
        return (int(coord[1]) - 1) * 8 + (ord(coord[0]) - 97)

    def from_idx(self, idx):
        return f"{self.FILES[idx % 8]}{self.RANKS[idx // 8]}"

    def apply_san_move(self, san):
        if not san: return
        
        target_coord = san[-2:]
        target_idx = self.to_idx(target_coord)
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        moving_piece = self.turn + piece_type

        # Find the specific piece that matches the type
        origin_idx = next(idx for idx, p in self.pieces.items() if p == moving_piece)
        
        # Update state
        del self.pieces[origin_idx]
        self.pieces[target_idx] = moving_piece
        self.turn = "B" if self.turn == "W" else "W"

    def get_position_string(self):
        # Returns: WRb6;WKg4;BKg6
        sorted_pieces = sorted([(idx, p) for idx, p in self.pieces.items()], key=lambda x: x[0])
        return ";".join([f"{p}{self.from_idx(i)}" for i, p in sorted_pieces])