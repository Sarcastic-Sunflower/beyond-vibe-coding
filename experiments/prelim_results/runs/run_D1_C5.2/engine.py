# engine.py

FILES = "abcdefgh"
RANKS = "12345678"

# Precompute coordinate maps
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

# Precompute King adjacency sets for O(1) attack resolution
KING_ATTACKS = [set() for _ in range(64)]
for sq in range(64):
    r, f = sq // 8, sq % 8
    for dr in (-1, 0, 1):
        for df in (-1, 0, 1):
            if dr == 0 and df == 0: continue
            nr, nf = r + dr, f + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                KING_ATTACKS[sq].add(nr * 8 + nf)


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
            self.remove_piece(dst)  # Handle capture state safely
        self.set_piece(dst, p)

    def apply_san_move(self, san: str, color_mask: int) -> None:
        s = san.strip("+#!?x \t\n")
        if len(s) < 2: 
            return
            
        piece_type = KING if s[0] == 'K' else ROOK
        dest_idx = SQ_TO_IDX.get(s[-2:])
        
        if dest_idx is None: 
            return
            
        target_val = color_mask | piece_type
        
        # Cast to list to safely perform deep mutation dynamically
        for idx, p_val in list(self.pieces[color_mask].items()):
            if p_val == target_val:
                self.move_piece(idx, dest_idx)
                return

    def is_square_attacked(self, sq_idx: int, attacker_color: int) -> bool:
        if sq_idx < 0: 
            return False
            
        grid = self.grid
        
        for idx, p_val in self.pieces[attacker_color].items():
            ptype = p_val & PIECE_MASK
            
            if ptype == KING:
                if sq_idx in KING_ATTACKS[idx]:
                    return True
            elif ptype == ROOK:
                if idx // 8 == sq_idx // 8:  # Same rank
                    step = 1 if sq_idx > idx else -1
                    curr = idx + step
                    blocked = False
                    while curr != sq_idx:
                        if grid[curr]:
                            blocked = True
                            break
                        curr += step
                    if not blocked: return True
                    
                elif idx % 8 == sq_idx % 8:  # Same file
                    step = 8 if sq_idx > idx else -8
                    curr = idx + step
                    blocked = False
                    while curr != sq_idx:
                        if grid[curr]:
                            blocked = True
                            break
                        curr += step
                    if not blocked: return True
                    
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
                    
                    if not target_p or (target_p & COLOR_MASK) != color:
                        # Clean execution simulation
                        self.remove_piece(start_idx)
                        captured_p = target_p
                        if captured_p:
                            self.remove_piece(target_idx)
                        self.set_piece(target_idx, p_val)
                        
                        if not self.is_square_attacked(self.king_idx[color], opp_color):
                            is_cap = "x" if captured_p else ""
                            legal_moves.append(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                            
                        # Revert move
                        self.remove_piece(target_idx)
                        if captured_p:
                            self.set_piece(target_idx, captured_p)
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
                            break  # Blocked by friendly piece
                            
                        # Clean execution simulation
                        self.remove_piece(start_idx)
                        captured_p = target_p
                        if captured_p:
                            self.remove_piece(curr_idx)
                        self.set_piece(curr_idx, p_val)
                        
                        if not self.is_square_attacked(self.king_idx[color], opp_color):
                            is_cap = "x" if captured_p else ""
                            legal_moves.append(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                            
                        # Revert move
                        self.remove_piece(curr_idx)
                        if captured_p:
                            self.set_piece(curr_idx, captured_p)
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