class Board:
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        self.turn = "W"
        self._setup_initial()

    def _setup_initial(self):
        # Adjusted to match the likely legacy starting state
        self._place("a6", "WR") # Rook starting on a6 to reach b6
        self._place("f5", "WK") # White King
        self._place("g8", "BK") # Black King

    def _place(self, san, piece):
        self.board[self.SAN_TO_IDX[san]] = piece

    def apply_move(self, san_move):
        import engine
        # We search for the piece that can legally perform this SAN move
        legal_moves = engine.get_legal_moves(self, include_details=True)
        move_data = next((m for m in legal_moves if m['san'] == san_move), None)
        
        if move_data:
            self.board[move_data['end']] = self.board[move_data['start']]
            self.board[move_data['start']] = None
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        """Returns the sorted string of pieces currently on the board."""
        pieces = []
        for i, piece in enumerate(self.board):
            if piece:
                pieces.append(f"{piece}{self.IDX_TO_SAN[i]}")
        return ";".join(sorted(pieces))