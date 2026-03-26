class Board:
    # Proper mapping: a1=0, b1=1...h1=7, a2=8...h8=63
    IDX_TO_SAN = [f"{chr(97+f)}{r+1}" for r in range(8) for f in range(8)]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        # Setup initial positions: WK on g4, WR on a5, BK on g7
        self.board[self.SAN_TO_IDX["g4"]] = "WK"
        self.board[self.SAN_TO_IDX["a5"]] = "WR"
        self.board[self.SAN_TO_IDX["g7"]] = "BK"
        self.turn = "W"

    def apply_san(self, san):
        import engine
        # Generate legal moves to find the matching SAN string
        moves = engine.get_legal_moves(self, include_details=True)
        move = next((m for m in moves if m['san'] == san), None)
        
        if move:
            p = self.board[move['start']]
            # Handle potential capture logic for piece count consistency
            self.board[move['end']] = p
            self.board[move['start']] = None
            self.turn = "B" if self.turn == "W" else "W"

    def get_pos_string(self):
        pieces = []
        for i, p in enumerate(self.board):
            if p:
                pieces.append(f"{p}{self.IDX_TO_SAN[i]}")
        return ";".join(sorted(pieces))