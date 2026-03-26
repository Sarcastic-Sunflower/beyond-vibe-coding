class Board:
    # Indexing: a1=0, b1=1 ... h1=7, a2=8 ... h8=63
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        # Initial positions per legacy setup: WK on g4, WR on a5, BK on g7
        self.set_piece(30, "WK") # g4
        self.set_piece(32, "WR") # a5
        self.set_piece(54, "BK") # g7
        self.turn = "W"

    def set_piece(self, idx, piece):
        self.board[idx] = piece

    def apply_san(self, san):
        import engine
        # Resolve move to get start and end indices
        moves = engine.get_legal_moves(self, include_details=True)
        move = next((m for m in moves if m['san'] == san), None)
        
        if move:
            p = self.board[move['start']]
            self.board[move['start']] = None
            self.board[move['end']] = p
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        pieces = []
        for i, p in enumerate(self.board):
            if p: pieces.append(f"{p}{self.IDX_TO_SAN[i]}")
        return ";".join(sorted(pieces))