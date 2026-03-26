class Board:
    IDX_TO_SAN = [f"{f}{r}" for r in "12345678" for f in "abcdefgh"]
    SAN_TO_IDX = {san: i for i, san in enumerate(IDX_TO_SAN)}

    def __init__(self):
        self.board = [None] * 64
        # Initial Setup: WK on g4 (30), WR on a5 (32), BK on g7 (54)
        # Note: Indexing 0-63 (a1-h8). a5 is idx 32, g4 is idx 30, g7 is idx 54.
        self.board[30], self.board[32], self.board[54] = "WK", "WR", "BK"
        self.turn = "W"
        self.piece_indices = {30, 32, 54}

    def apply_san_move(self, san):
        if not san: return
        import engine
        
        target_san = san.replace("x", "").replace("+", "")[-2:]
        target_idx = self.SAN_TO_IDX[target_san]
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        
        # Find which piece of this type can actually reach the target
        legal_moves = engine.get_legal_moves(self, include_details=True)
        move_to_execute = next((m for m in legal_moves if m['san'] == san or m['dest_idx'] == target_idx and m['type'] == piece_type), None)

        if move_to_execute:
            start_idx = move_to_execute['start_idx']
            moving_piece = self.board[start_idx]
            
            # Remove from old position
            self.board[start_idx] = None
            self.piece_indices.remove(start_idx)
            
            # Handle capture
            if self.board[target_idx]:
                self.piece_indices.remove(target_idx)
            
            # Place at new position
            self.board[target_idx] = moving_piece
            self.piece_indices.add(target_idx)
            self.turn = "B" if self.turn == "W" else "W"

    def get_position_string(self):
        return ";".join(f"{self.board[i]}{self.IDX_TO_SAN[i]}" 
                        for i in sorted(self.piece_indices))