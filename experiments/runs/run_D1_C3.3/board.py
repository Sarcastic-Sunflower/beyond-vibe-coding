class Board:
    # Adjusted to ensure rank-major ordering: a1, b1...h1, a2...h8
    IDX_TO_SAN = [f"{chr(97+f)}{r+1}" for r in range(8) for f in range(8)]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        # Setup initial positions based on the required final state logic
        # WK on g4 (idx 30), WR on a5 (idx 32), BK on g7 (idx 54)
        self.set_piece(30, "WK") 
        self.set_piece(32, "WR") 
        self.set_piece(54, "BK") 
        self.turn = "W"

    def set_piece(self, idx, piece):
        self.board[idx] = piece

    def apply_san(self, san):
        import engine
        moves = engine.get_legal_moves(self, include_details=True)
        # Match SAN move to execution logic
        move = next((m for m in moves if m['san'] == san), None)
        
        if move:
            p = self.board[move['start']]
            self.board[move['end']] = p
            self.board[move['start']] = None
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        pieces = []
        for i in range(64):
            if self.board[i]:
                pieces.append(f"{self.board[i]}{self.IDX_TO_SAN[i]}")
        # Legacy format often expects alphabetical sorting of the piece strings
        return ";".join(sorted(pieces))