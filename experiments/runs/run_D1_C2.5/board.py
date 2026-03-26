class Board:
    # Pre-computed coordinate map: 0 -> 'a1', 1 -> 'b1', ...
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        # Using a fixed-size list (64) is faster than a dict for lookups
        self.board = [None] * 64
        self.board[30], self.board[40], self.board[63] = "WK", "WR", "BK"
        self.turn = "W"
        self.piece_indices = {30, 40, 63} # Track active indices for O(K) iteration

    def apply_san_move(self, san):
        if not san: return
        target_idx = self.SAN_TO_IDX[san[-2:]]
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        moving_piece = self.turn + piece_type

        # Fast lookup for the piece to move
        for idx in self.piece_indices:
            if self.board[idx] == moving_piece:
                self.board[idx] = None
                self.piece_indices.remove(idx)
                break
        
        # Handle captures and placement
        if self.board[target_idx]:
            self.piece_indices.remove(target_idx)
        
        self.board[target_idx] = moving_piece
        self.piece_indices.add(target_idx)
        self.turn = "B" if self.turn == "W" else "W"

    def get_position_string(self):
        # Sorted by index as per legacy requirement
        return ";".join(f"{self.board[i]}{self.IDX_TO_SAN[i]}" 
                        for i in sorted(self.piece_indices))