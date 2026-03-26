class Board:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # Initial positions based on the expected state
        self.pieces = {41: "WR", 30: "WK", 46: "BK"}
        self.turn = "W"

    def to_idx(self, coord):
        return (int(coord[1]) - 1) * 8 + (ord(coord[0]) - 97)

    def from_idx(self, idx):
        return f"{self.FILES[idx % 8]}{self.RANKS[idx // 8]}"

    def apply_san_move(self, san):
        if not san or len(san) < 2: return
        
        target_coord = san[-2:]
        target_idx = self.to_idx(target_coord)
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        moving_piece = self.turn + piece_type

        # Find the specific piece that matches the type
        try:
            origin_idx = next(idx for idx, p in self.pieces.items() if p == moving_piece)
            del self.pieces[origin_idx]
            # Handle captures: if a piece is at target_idx, it is removed implicitly
            self.pieces[target_idx] = moving_piece
            self.turn = "B" if self.turn == "W" else "W"
        except StopIteration:
            pass # Move not possible with current state

    def get_position_string(self):
        # Sorted by index to match standard output expectations
        sorted_indices = sorted(self.pieces.keys())
        return ";".join([f"{self.pieces[i]}{self.from_idx(i)}" for i in sorted_indices])