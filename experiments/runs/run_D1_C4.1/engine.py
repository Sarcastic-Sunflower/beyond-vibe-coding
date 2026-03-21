# engine.py

# Precomputed lookup tables
FILES = "abcdefgh"
RANKS = "12345678"

SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

# Integer Bitmasks for fast evaluation
WHITE, BLACK = 8, 16
ROOK, KING = 1, 2
COLOR_MASK = WHITE | BLACK
PIECE_MASK = ROOK | KING

PIECE_TO_STR = {
    WHITE | ROOK: "WR", WHITE | KING: "WK",
    BLACK | ROOK: "BR", BLACK | KING: "BK"
}

# 1D array directional offsets: N, S, E, W, NE, NW, SE, SW
DIR_OFFSETS = (8, -8, 1, -1, 9, 7, -7, -9)

# Precalculate distance to edge for all 64 squares across all 8 directions
NUM_SQUARES_TO_EDGE = [[0] * 8 for _ in range(64)]
for sq in range(64):
    r, f = sq // 8, sq % 8
    NUM_SQUARES_TO_EDGE[sq][0] = 7 - r             # N
    NUM_SQUARES_TO_EDGE[sq][1] = r                 # S
    NUM_SQUARES_TO_EDGE[sq][2] = 7 - f             # E
    NUM_SQUARES_TO_EDGE[sq][3] = f                 # W
    NUM_SQUARES_TO_EDGE[sq][4] = min(7 - r, 7 - f) # NE
    NUM_SQUARES_TO_EDGE[sq][5] = min(7 - r, f)     # NW
    NUM_SQUARES_TO_EDGE[sq][6] = min(r, 7 - f)     # SE
    NUM_SQUARES_TO_EDGE[sq][7] = min(r, f)         # SW


class Board:
    __slots__ = ['grid', 'king_idx']

    def __init__(self):
        self.grid = [0] * 64
        self.king_idx = {WHITE: -1, BLACK: -1}

    def setup_initial(self):
        """Sets up the initial board state."""
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx: int, piece_val: int):
        """Places a piece on the board and updates king tracking."""
        self.grid[idx] = piece_val
        if piece_val & KING:
            color = piece_val & COLOR_MASK
            self.king_idx[color] = idx

    def apply_san_move(self, san: str, color_mask: int):
        """Applies a stripped-down Standard Algebraic Notation move."""
        s = san.strip("+#!?x \t\n")
        
        # Guard against short tokens or malformed input
        if len(s) < 2: 
            return
            
        ptype_char = s[0]
        piece_type = KING if ptype_char == 'K' else ROOK if ptype_char == 'R' else ROOK
            
        dest_idx = SQ_TO_IDX.get(s[-2:])
        if dest_idx is None:
            return
            
        target_val = color_mask | piece_type
        
        # Fast linear scan to find the piece to move
        for idx in range(64):
            if self.grid[idx] == target_val:
                self.grid[idx] = 0
                self.set_piece(dest_idx, target_val)
                return

    def is_square_attacked(self, sq_idx: int, attacker_color: int) -> bool:
        """Checks if a given square is attacked by a specific color."""
        # 1. Straight Rays (Rooks) - Directions 0 to 3
        target_rook = attacker_color | ROOK
        for dir_idx in range(4):
            offset = DIR_OFFSETS[dir_idx]
            curr_idx = sq_idx
            for _ in range(NUM_SQUARES_TO_EDGE[sq_idx][dir_idx]):
                curr_idx += offset
                p = self.grid[curr_idx]
                if p:
                    if p == target_rook:
                        return True
                    break # Blocked by any other piece

        # 2. Adjacency (Kings) - Directions 0 to 7 (1 step max)
        target_king = attacker_color | KING
        for dir_idx in range(8):
            if NUM_SQUARES_TO_EDGE[sq_idx][dir_idx] > 0:
                if self.grid[sq_idx + DIR_OFFSETS[dir_idx]] == target_king:
                    return True

        return False

    def get_legal_moves(self, color: int) -> list[str]:
        """Generates all legal pseudo-legal moves that don't leave the king in check."""
        legal_moves = []
        opp_color = BLACK if color == WHITE else WHITE
        king_pos = self.king_idx[color]
        
        for start_idx in range(64):
            p = self.grid[start_idx]
            if not p or (p & COLOR_MASK) != color:
                continue
                
            ptype = p & PIECE_MASK
            
            if ptype == ROOK:
                for dir_idx in range(4):
                    offset = DIR_OFFSETS[dir_idx]
                    curr_idx = start_idx
                    
                    for _ in range(NUM_SQUARES_TO_EDGE[start_idx][dir_idx]):
                        curr_idx += offset
                        target_p = self.grid[curr_idx]
                        
                        if target_p:
                            if (target_p & COLOR_MASK) == color:
                                break # Blocked by friendly piece
                                
                        # Make move in-place
                        self.grid[start_idx] = 0
                        self.grid[curr_idx] = p
                        
                        # Verify king safety
                        if not self.is_square_attacked(king_pos, opp_color):
                            is_cap = "x" if target_p else ""
                            legal_moves.append(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                            
                        # Revert move
                        self.grid[start_idx] = p
                        self.grid[curr_idx] = target_p
                        
                        if target_p:
                            break # Stop sliding post-capture
                            
            elif ptype == KING:
                for dir_idx in range(8):
                    if NUM_SQUARES_TO_EDGE[start_idx][dir_idx] > 0:
                        target_idx = start_idx + DIR_OFFSETS[dir_idx]
                        target_p = self.grid[target_idx]
                        
                        if not target_p or (target_p & COLOR_MASK) != color:
                            # Move King
                            self.grid[start_idx] = 0
                            self.grid[target_idx] = p
                            
                            if not self.is_square_attacked(target_idx, opp_color):
                                is_cap = "x" if target_p else ""
                                legal_moves.append(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                                
                            # Revert King
                            self.grid[start_idx] = p
                            self.grid[target_idx] = target_p

        return sorted(list(set(legal_moves)))

    def pos_string(self) -> str:
        """Returns the board state as a formatted string."""
        parts = []
        for idx, p in enumerate(self.grid):
            if p:
                parts.append(PIECE_TO_STR[p] + IDX_TO_SQ[idx])
                
        # Preserves exact legacy sorting requirements
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)