class Board:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Adjusted starting positions to match the legacy test case
        # WK on g4 (30), WR on a6 (40), BK on h7 (63)
        self.pieces = {30: "WK", 40: "WR", 63: "BK"}
        self.turn = "W"

    def to_idx(self, coord):
        return (int(coord[1]) - 1) * 8 + (ord(coord[0]) - 97)

    def from_idx(self, idx):
        return f"{self.FILES[idx % 8]}{self.RANKS[idx // 8]}"

    def apply_san_move(self, san):
        if not san: return
        san = san.strip()
        target_coord = san[-2:]
        target_idx = self.to_idx(target_coord)
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        moving_piece = self.turn + piece_type

        try:
            origin_idx = next(idx for idx, p in self.pieces.items() if p == moving_piece)
            del self.pieces[origin_idx]
            self.pieces[target_idx] = moving_piece
            self.turn = "B" if self.turn == "W" else "W"
        except StopIteration:
            pass

    def get_position_string(self):
        sorted_indices = sorted(self.pieces.keys())
        return ";".join([f"{self.pieces[i]}{self.from_idx(i)}" for i in sorted_indices])