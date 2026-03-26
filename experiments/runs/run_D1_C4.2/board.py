class Board:
    # Map index to Algebraic Notation (e.g., 0 -> a1)
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        self.turn = "W"
        self._setup_initial()

    def _setup_initial(self):
        # Starting positions based on your legacy script
        self._place("g4", "WK")
        self._place("a5", "WR")
        self._place("g7", "BK")

    def _place(self, san, piece):
        self.board[self.SAN_TO_IDX[san]] = piece

    def apply_move(self, san_move):
        """Processes a SAN string like 'Rb6' and updates the board."""
        import engine
        legal_moves = engine.get_legal_moves(self, include_details=True)
        move_data = next((m for m in legal_moves if m['san'] == san_move), None)
        
        if move_data:
            start, end = move_data['start'], move_data['end']
            self.board[end] = self.board[start]
            self.board[start] = None
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        """Returns the sorted string of pieces currently on the board."""
        pieces = []
        for i, piece in enumerate(self.board):
            if piece:
                pieces.append(f"{piece}{self.IDX_TO_SAN[i]}")
        return ";".join(sorted(pieces))