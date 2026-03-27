class Board:
    # Pre-calculated for speed
    SQUARES = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    S_MAP = {s: i for i, s in enumerate(SQUARES)}

    def __init__(self):
        # Piece positions as integers 0-63
        self.wr, self.wk, self.bk = 40, 37, 62  # a6, f5, g8
        self.turn = 0  # 0 for White, 1 for Black

    def apply_moves(self, move_list):
        """Processes a list of moves efficiently."""
        for move in move_list:
            target = self.S_MAP[move[-2:]]
            if 'R' in move:
                self.wr = target
            elif 'K' in move:
                if self.turn == 0: self.wk = target
                else: self.bk = target
            self.turn ^= 1

    def get_header(self):
        """Returns the sorted position string: BK..;WK..;WR.."""
        parts = [f"BK{self.SQUARES[self.bk]}", 
                 f"WK{self.SQUARES[self.wk]}", 
                 f"WR{self.SQUARES[self.wr]}"]
        return ";".join(sorted(parts))