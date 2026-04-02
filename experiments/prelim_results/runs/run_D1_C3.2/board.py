# Precomputed tables for O(1) coordinate mapping
FILES = "abcdefgh"
RANKS = "12345678"

SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

class Board:
    __slots__ = ['grid', 'king_idx']

    def __init__(self):
        # 1D array for contiguous memory mapping
        self.grid = [None] * 64
        self.king_idx = {'W': -1, 'B': -1}

    def setup_initial(self):
        self.set_piece(SQ_TO_IDX["b6"], "WR")
        self.set_piece(SQ_TO_IDX["g4"], "WK")
        self.set_piece(SQ_TO_IDX["g6"], "BK")

    def set_piece(self, idx, piece):
        self.grid[idx] = piece
        if piece and piece[1] == 'K':
            self.king_idx[piece[0]] = idx

    def apply_san_move(self, san, color):
        # Clean decorators and source tags inline
        s = san.strip("+#!?x \t\n")
        if ']' in s:
            s = s.split(']', 1)[-1].strip("+#!?x \t\n")
            
        if len(s) < 2: 
            return
            
        ptype = s[0] if s[0] in "RKQBN" else "P"
        dest_sq = s[-2:]
        dest_idx = SQ_TO_IDX.get(dest_sq)
        
        if dest_idx is None:
            return
            
        target_piece = color + ptype
        
        # Fast linear scan for the moving piece
        for idx in range(64):
            if self.grid[idx] == target_piece:
                self.grid[idx] = None
                self.set_piece(dest_idx, target_piece)
                return

    def pos_string(self):
        parts = [p + IDX_TO_SQ[idx] for idx, p in enumerate(self.grid) if p]
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)