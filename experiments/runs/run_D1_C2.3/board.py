# Precomputed Lookup Tables for O(1) coordinate mapping
FILES = "abcdefgh"
RANKS = "12345678"

# Map string coordinates (e.g., 'a1') to 0-63 integer indices, and vice versa
SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

# Clean SAN translation table executed at C-level
CLEAN_SAN_TRANS = str.maketrans("", "", "+#!?x")

class Board:
    __slots__ = ['grid', 'king_idx']

    def __init__(self):
        # 1D array for maximum iteration speed and spatial locality
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
        """Ultra-fast SAN parser mapping directly to the 1D array."""
        s = san.strip().translate(CLEAN_SAN_TRANS)
        if len(s) < 2: 
            return
            
        ptype = s[0] if s[0] in "RKQBN" else "P"
        dest_idx = SQ_TO_IDX.get(s[-2:])
        if dest_idx is None:
            return
            
        target_piece = color + ptype
        
        # Linear scan is exceptionally fast on a 64-element 1D list
        for idx in range(64):
            if self.grid[idx] == target_piece:
                self.grid[idx] = None
                self.set_piece(dest_idx, target_piece)
                return

    def pos_string(self):
        parts = []
        # Appends directly using precomputed string lookups
        for idx, p in enumerate(self.grid):
            if p:
                parts.append(p + IDX_TO_SQ[idx])
                
        # Preserves exact legacy sorting requirements
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)