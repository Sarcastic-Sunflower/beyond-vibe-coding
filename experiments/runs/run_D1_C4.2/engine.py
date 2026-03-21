# engine.py

FILES = "abcdefgh"
RANKS = "12345678"

SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

WHITE, BLACK = 8, 16
ROOK, KING = 1, 2
COLOR_MASK = WHITE | BLACK
PIECE_MASK = ROOK | KING

PIECE_TO_STR = {
    WHITE | ROOK: "WR", WHITE | KING: "WK",
    BLACK | ROOK: "BR", BLACK | KING: "BK"
}

DIR_OFFSETS = (8, -8, 1, -1, 9, 7, -7, -9)

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
    __slots__ = ['grid']

    def __init__(self):
        self.grid = [0] * 64

    def setup_initial(self):
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx: int, piece_val: int):
        self.grid[idx] = piece_val

    def find_king(self, color: int) -> int:
        """Dynamically finds the king to prevent stale indices post-capture."""
        target = color | KING
        for i, p in enumerate(self.grid):
            if p == target:
                return i
        return -1

    def apply_san_move(self, san: str, color_mask: int):
        s = san.strip("+#!?x \t\n")
        
        if len(s) < 2: 
            return
            
        ptype_char = s[0]
        piece_type = KING if ptype_char == 'K' else ROOK if ptype_char == 'R' else ROOK
            
        dest_idx = SQ_TO_IDX.get(s[-2:])
        if dest_idx is None:
            return
            
        target_val = color_mask | piece_type
        
        for idx in range(64):
            if self.grid[idx] == target_val:
                self.grid[idx] = 0
                self.set_piece(dest_idx, target_val)
                return

    def is_square_attacked(self, sq_idx: int, attacker_color: int) -> bool:
        if sq_idx < 0: 
            return False

        # 1. Straight Rays (Rooks)
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
                    break

        # 2. Adjacency (Kings)
        target_king = attacker_color | KING
        for dir_idx in range(8):
            if NUM_SQUARES_TO_EDGE[sq_idx][dir_idx] > 0:
                if self.grid[sq_idx + DIR_OFFSETS[dir_idx]] == target_king:
                    return True

        return False

    def get_legal_moves(self, color: int) -> list:
        legal_moves = []
        opp_color = BLACK if color == WHITE else WHITE
        
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
                                break
                                
                        self.grid[start_idx] = 0
                        self.grid[curr_idx] = p
                        
                        # Dynamically find king in case it was modified/captured
                        k_pos = self.find_king(color)
                        if not self.is_square_attacked(k_pos, opp_color):
                            is_cap = "x" if target_p else ""
                            legal_moves.append(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                            
                        self.grid[start_idx] = p
                        self.grid[curr_idx] = target_p
                        
                        if target_p:
                            break
                            
            elif ptype == KING:
                for dir_idx in range(8):
                    if NUM_SQUARES_TO_EDGE[start_idx][dir_idx] > 0:
                        target_idx = start_idx + DIR_OFFSETS[dir_idx]
                        target_p = self.grid[target_idx]
                        
                        if not target_p or (target_p & COLOR_MASK) != color:
                            self.grid[start_idx] = 0
                            self.grid[target_idx] = p
                            
                            if not self.is_square_attacked(target_idx, opp_color):
                                is_cap = "x" if target_p else ""
                                legal_moves.append(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                                
                            self.grid[start_idx] = p
                            self.grid[target_idx] = target_p

        return sorted(list(set(legal_moves)))

    def pos_string(self) -> str:
        parts = []
        for idx, p in enumerate(self.grid):
            if p:
                parts.append(PIECE_TO_STR[p] + IDX_TO_SQ[idx])
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)