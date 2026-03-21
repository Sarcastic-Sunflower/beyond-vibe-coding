# Precomputed lookup tables
FILES = "abcdefgh"
RANKS = "12345678"

SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

# Integer Bitmasks for ultra-fast evaluation
WHITE, BLACK = 8, 16
ROOK, KING = 1, 2
COLOR_MASK = WHITE | BLACK
PIECE_MASK = ROOK | KING

PIECE_TO_STR = {
    WHITE | ROOK: "WR", WHITE | KING: "WK",
    BLACK | ROOK: "BR", BLACK | KING: "BK"
}

class Board:
    __slots__ = ['grid', 'king_idx']

    def __init__(self):
        # 1D array of integers (0 = empty)
        self.grid = [0] * 64
        self.king_idx = {WHITE: -1, BLACK: -1}

    def setup_initial(self):
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx, piece_val):
        self.grid[idx] = piece_val
        if piece_val & KING:
            color = piece_val & COLOR_MASK
            self.king_idx[color] = idx

    def apply_san_move(self, san, color_mask):
        s = san.strip("+#!?x \t\n")
        if ']' in s:
            s = s.split(']', 1)[-1].strip("+#!?x \t\n")
            
        if len(s) < 2: 
            return
            
        ptype_char = s[0]
        piece_type = KING if ptype_char == 'K' else ROOK if ptype_char == 'R' else 0
        if not piece_type:
            piece_type = ROOK # Default to sliding piece logic for this limited scope
            
        dest_idx = SQ_TO_IDX.get(s[-2:])
        if dest_idx is None:
            return
            
        target_val = color_mask | piece_type
        
        # Fast linear scan 
        for idx in range(64):
            if self.grid[idx] == target_val:
                self.grid[idx] = 0
                self.set_piece(dest_idx, target_val)
                return

    def pos_string(self):
        parts = []
        for idx, p in enumerate(self.grid):
            if p:
                parts.append(PIECE_TO_STR[p] + IDX_TO_SQ[idx])
                
        # Preserves exact legacy sorting requirements
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)