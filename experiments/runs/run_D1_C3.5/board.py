class Board:
    # Pre-calculated static lookups to avoid runtime string manipulation
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        # Using a fixed-size list for O(1) access
        self.board = [None] * 64
        self.occupied = set()
        
        # Initial positions
        self._set_initial("g4", "WK")
        self._set_initial("a5", "WR")
        self._set_initial("g7", "BK")
        self.turn = "W"

    def _set_initial(self, san, piece):
        idx = self.SAN_TO_IDX[san]
        self.board[idx] = piece
        self.occupied.add(idx)

    def apply_san(self, san):
        import engine
        # Pass include_details=True to get raw indices directly
        moves = engine.get_legal_moves(self, include_details=True)
        
        # Generator expression is faster for single-match searches
        move = next((m for m in moves if m['san'] == san), None)
        
        if move:
            start, end = move['start'], move['end']
            piece = self.board[start]
            
            # Update board and occupied set
            self.board[start] = None
            self.occupied.remove(start)
            
            # Handle potential capture (removes captured piece from occupied set)
            if self.board[end]:
                self.occupied.discard(end)
                
            self.board[end] = piece
            self.occupied.add(end)
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        # List comprehension is faster than manual loops for building the final string
        pieces = [f"{self.board[i]}{self.IDX_TO_SAN[i]}" for i in sorted(self.occupied)]
        return ";".join(pieces)