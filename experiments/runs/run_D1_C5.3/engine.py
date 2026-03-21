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

# Precompute King adjacency using tuples for O(1) immutable lookups
_king_attacks = [[] for _ in range(64)]
for sq in range(64):
    r, f = sq // 8, sq % 8
    for dr in (-1, 0, 1):
        for df in (-1, 0, 1):
            if dr == 0 and df == 0: continue
            nr, nf = r + dr, f + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                _king_attacks[sq].append(nr * 8 + nf)
KING_ATTACKS = tuple(tuple(attacks) for attacks in _king_attacks)


class Board:
    # Memory optimization locking class structure
    __slots__ = ['grid', 'w_pieces', 'b_pieces', 'w_king', 'b_king']

    def __init__(self):
        self.grid = [0] * 64
        self.w_pieces = set()
        self.b_pieces = set()
        self.w_king = -1
        self.b_king = -1

    def setup_initial(self) -> None:
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx: int, p_val: int) -> None:
        self.grid[idx] = p_val
        if p_val & WHITE:
            self.w_pieces.add(idx)
            if p_val & KING:
                self.w_king = idx
        else:
            self.b_pieces.add(idx)
            if p_val & KING:
                self.b_king = idx

    def remove_piece(self, idx: int) -> None:
        p = self.grid[idx]
        if not p: return
        self.grid[idx] = 0
        
        if p & WHITE:
            self.w_pieces.remove(idx)
            if p & KING:
                self.w_king = -1
        else:
            self.b_pieces.remove(idx)
            if p & KING:
                self.b_king = -1

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
        
        # Fast reference binding
        active_pieces = list(self.w_pieces) if color_mask == WHITE else list(self.b_pieces)
        grid = self.grid
        
        for idx in active_pieces:
            if grid[idx] == target_val:
                self.move_piece(idx, dest_idx)
                return

    def get_legal_moves(self, color: int) -> list[str]:
        legal_moves = []
        grid = self.grid
        
        # Bind variables locally to avoid 'self.' lookup penalties in the loop
        if color == WHITE:
            active_pieces = list(self.w_pieces)
            enemy_king_val = BLACK | KING
            enemy_rook_val = BLACK | ROOK
        else:
            active_pieces = list(self.b_pieces)
            enemy_king_val = WHITE | KING
            enemy_rook_val = WHITE | ROOK

        for start_idx in active_pieces:
            p_val = grid[start_idx]
            ptype = p_val & PIECE_MASK
            
            if ptype == KING:
                for target_idx in KING_ATTACKS[start_idx]:
                    target_p = grid[target_idx]
                    
                    if target_p and (target_p & COLOR_MASK) == color:
                        continue
                        
                    # Execute
                    self.remove_piece(start_idx)
                    if target_p: self.remove_piece(target_idx)
                    self.set_piece(target_idx, p_val)
                    
                    # Inlined attack validation
                    curr_king_idx = self.w_king if color == WHITE else self.b_king
                    is_attacked = False
                    
                    if curr_king_idx != -1:
                        enemy_king_idx = self.b_king if color == WHITE else self.w_king
                        
                        # 1. Evaluate adjacent Kings
                        if enemy_king_idx != -1 and enemy_king_idx in KING_ATTACKS[curr_king_idx]:
                            is_attacked = True
                        
                        # 2. Evaluate sliding Rooks
                        if not is_attacked:
                            for step in (8, -8, 1, -1):
                                curr = curr_king_idx
                                while True:
                                    if step == 1 and curr % 8 == 7: break
                                    if step == -1 and curr % 8 == 0: break
                                    if step == 8 and curr // 8 == 7: break
                                    if step == -8 and curr // 8 == 0: break
                                    
                                    curr += step
                                    ray_p = grid[curr]
                                    if ray_p:
                                        if ray_p == enemy_rook_val:
                                            is_attacked = True
                                        break

                    if not is_attacked:
                        is_cap = "x" if target_p else ""
                        legal_moves.append(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                        
                    # Revert
                    self.remove_piece(target_idx)
                    if target_p: self.set_piece(target_idx, target_p)
                    self.set_piece(start_idx, p_val)

            elif ptype == ROOK:
                for step in (8, -8, 1, -1):
                    curr_idx = start_idx
                    while True:
                        if step == 1 and curr_idx % 8 == 7: break
                        if step == -1 and curr_idx % 8 == 0: break
                        if step == 8 and curr_idx // 8 == 7: break
                        if step == -8 and curr_idx // 8 == 0: break
                        
                        curr_idx += step
                        target_p = grid[curr_idx]
                        
                        if target_p and (target_p & COLOR_MASK) == color:
                            break
                            
                        # Execute
                        self.remove_piece(start_idx)
                        if target_p: self.remove_piece(curr_idx)
                        self.set_piece(curr_idx, p_val)
                        
                        # Inlined attack validation
                        curr_king_idx = self.w_king if color == WHITE else self.b_king
                        is_attacked = False
                        
                        if curr_king_idx != -1:
                            enemy_king_idx = self.b_king if color == WHITE else self.w_king
                            if enemy_king_idx != -1 and enemy_king_idx in KING_ATTACKS[curr_king_idx]:
                                is_attacked = True
                            
                            if not is_attacked:
                                for r_step in (8, -8, 1, -1):
                                    curr = curr_king_idx
                                    while True:
                                        if r_step == 1 and curr % 8 == 7: break
                                        if r_step == -1 and curr % 8 == 0: break
                                        if r_step == 8 and curr // 8 == 7: break
                                        if r_step == -8 and curr // 8 == 0: break
                                        
                                        curr += r_step
                                        ray_p = grid[curr]
                                        if ray_p:
                                            if ray_p == enemy_rook_val:
                                                is_attacked = True
                                            break

                        if not is_attacked:
                            is_cap = "x" if target_p else ""
                            legal_moves.append(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                            
                        # Revert
                        self.remove_piece(curr_idx)
                        if target_p: self.set_piece(curr_idx, target_p)
                        self.set_piece(start_idx, p_val)
                                
                        if target_p:
                            break

        return sorted(set(legal_moves))

    def pos_string(self) -> str:
        parts = []
        for idx in self.w_pieces:
            parts.append(PIECE_TO_STR[self.grid[idx]] + IDX_TO_SQ[idx])
        for idx in self.b_pieces:
            parts.append(PIECE_TO_STR[self.grid[idx]] + IDX_TO_SQ[idx])
            
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)