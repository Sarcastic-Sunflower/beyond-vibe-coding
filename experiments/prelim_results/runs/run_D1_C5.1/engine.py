# engine.py

FILES = "abcdefgh"
RANKS = "12345678"

# Coordinate maps
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

# Precompute structural lookups for O(1) move generation
KING_ATTACKS = [set() for _ in range(64)]
RAYS = [[] for _ in range(64)]

for sq in range(64):
    r, f = sq // 8, sq % 8
    
    # 1. King Adjacency Lookup
    for dr in (-1, 0, 1):
        for df in (-1, 0, 1):
            if dr == 0 and df == 0: continue
            nr, nf = r + dr, f + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                KING_ATTACKS[sq].add(nr * 8 + nf)
                
    # 2. Rook Rays Lookup (North, South, East, West)
    north = [sq + i * 8 for i in range(1, 8 - r)]
    south = [sq - i * 8 for i in range(1, r + 1)]
    east = [sq + i for i in range(1, 8 - f)]
    west = [sq - i for i in range(1, f + 1)]
    RAYS[sq] = [north, south, east, west]


class Board:
    __slots__ = ['grid', 'pieces', 'king_idx']

    def __init__(self):
        self.grid = [0] * 64
        self.pieces = {WHITE: {}, BLACK: {}}
        self.king_idx = {WHITE: -1, BLACK: -1}

    def setup_initial(self) -> None:
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx: int, piece_val: int) -> None:
        color = piece_val & COLOR_MASK
        self.grid[idx] = piece_val
        self.pieces[color][idx] = piece_val
        if piece_val & KING:
            self.king_idx[color] = idx

    def remove_piece(self, idx: int) -> None:
        p = self.grid[idx]
        if p:
            color = p & COLOR_MASK
            self.grid[idx] = 0
            del self.pieces[color][idx]
            if p & KING:
                self.king_idx[color] = -1

    def move_piece(self, src: int, dst: int) -> None:
        p = self.grid[src]
        self.remove_piece(src)
        if self.grid[dst]:
            self.remove_piece(dst)
        self.set_piece(dst, p)

    def apply_san_move(self, san: str, color_mask: int) -> None:
        s = san.strip("+#!?x \t\n")
        if len(s) < 2: return
        
        piece_type = KING if s[0] == 'K' else ROOK
        dest_idx = SQ_TO_IDX.get(s[-2:])
        if dest_idx is None: return
        
        target_val = color_mask | piece_type
        
        # Wrapped in list() to safely mutate the dictionary state
        for idx, p_val in list(self.pieces[color_mask].items()):
            if p_val == target_val:
                self.move_piece(idx, dest_idx)
                return

    def is_square_attacked(self, sq_idx: int, attacker_color: int) -> bool:
        if sq_idx < 0: 
            return False
            
        # 1. King threat evaluation (O(1))
        enemy_king_idx = self.king_idx[attacker_color]
        if enemy_king_idx != -1 and enemy_king_idx in KING_ATTACKS[sq_idx]:
            return True
            
        # 2. Ray threat evaluation
        enemy_rook = attacker_color | ROOK
        for ray in RAYS[sq_idx]:
            for ray_sq in ray:
                p = self.grid[ray_sq]
                if p:
                    if p == enemy_rook:
                        return True
                    break  # Blocked by another piece
        return False

    def get_legal_moves(self, color: int) -> list[str]:
        legal_moves = []
        opp_color = BLACK if color == WHITE else WHITE
        grid = self.grid
        
        for start_idx, p_val in list(self.pieces[color].items()):
            ptype = p_val & PIECE_MASK
            
            if ptype == KING:
                for target_idx in KING_ATTACKS[start_idx]:
                    target_p = grid[target_idx]
                    
                    if target_p and (target_p & COLOR_MASK) == color:
                        continue
                    
                    # Fix: standard chess restricts King-on-King captures
                    if target_p and (target_p & PIECE_MASK) == KING:
                        continue
                        
                    # Execute move simulation
                    self.remove_piece(start_idx)
                    captured_p = target_p
                    if captured_p:
                        self.remove_piece(target_idx)
                    self.set_piece(target_idx, p_val)
                    
                    # Validate legality
                    if not self.is_square_attacked(self.king_idx[color], opp_color):
                        is_cap = "x" if captured_p else ""
                        legal_moves.append(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                        
                    # Revert move
                    self.remove_piece(target_idx)
                    if captured_p:
                        self.set_piece(target_idx, captured_p)
                    self.set_piece(start_idx, p_val)

            elif ptype == ROOK:
                for ray in RAYS[start_idx]:
                    for target_idx in ray:
                        target_p = grid[target_idx]
                        
                        if target_p and (target_p & COLOR_MASK) == color:
                            break  # Blocked by friendly
                            
                        if target_p and (target_p & PIECE_MASK) == KING:
                            break  # Ray terminates at enemy King; illegal to capture

                        # Execute move simulation
                        self.remove_piece(start_idx)
                        captured_p = target_p
                        if captured_p:
                            self.remove_piece(target_idx)
                        self.set_piece(target_idx, p_val)
                        
                        # Validate legality
                        if not self.is_square_attacked(self.king_idx[color], opp_color):
                            is_cap = "x" if captured_p else ""
                            legal_moves.append(f"R{is_cap}{IDX_TO_SQ[target_idx]}")
                            
                        # Revert move
                        self.remove_piece(target_idx)
                        if captured_p:
                            self.set_piece(target_idx, captured_p)
                        self.set_piece(start_idx, p_val)
                        
                        if target_p:
                            break  # Stop sliding post-capture

        return sorted(set(legal_moves))

    def pos_string(self) -> str:
        parts = []
        for color in (WHITE, BLACK):
            for idx, p in self.pieces[color].items():
                parts.append(PIECE_TO_STR[p] + IDX_TO_SQ[idx])
                
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)