# engine.py
FILES, RANKS = "abcdefgh", "12345678"
SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

WHITE, BLACK = 8, 16
ROOK, KING = 1, 2

# Precompute non-sliding attacks for O(1) lookup
KING_MOVES = {}
for sq in range(64):
    r, f = divmod(sq, 8)
    moves = []
    for dr in [-1, 0, 1]:
        for df in [-1, 0, 1]:
            if dr == 0 and df == 0: continue
            nr, nf = r + dr, f + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                moves.append(nr * 8 + nf)
    KING_MOVES[sq] = tuple(moves)

class Board:
    __slots__ = ['grid', 'pieces', 'kings'] # Memory optimization 

    def __init__(self):
        self.grid = [0] * 64
        self.pieces = {WHITE: set(), BLACK: set()}
        self.kings = {WHITE: -1, BLACK: -1}

    def setup_initial(self):
        self.set_piece(SQ_TO_IDX["b6"], WHITE | ROOK)
        self.set_piece(SQ_TO_IDX["g4"], WHITE | KING)
        self.set_piece(SQ_TO_IDX["g6"], BLACK | KING)

    def set_piece(self, idx, p_val):
        self.grid[idx] = p_val
        color = p_val & (WHITE | BLACK)
        self.pieces[color].add(idx)
        if p_val & KING: self.kings[color] = idx

    def remove_piece(self, idx):
        p = self.grid[idx]
        if p:
            self.grid[idx] = 0
            self.pieces[p & (WHITE | BLACK)].discard(idx)

    def move_piece(self, src, dst):
        p = self.grid[src]
        self.remove_piece(src)
        if self.grid[dst]: self.remove_piece(dst)
        self.set_piece(dst, p)

    def is_in_check(self, color):
        king_pos = self.kings[color]
        enemy_color = BLACK if color == WHITE else WHITE
        enemy_rook = enemy_color | ROOK
        
        # Check sliding attacks (Rooks)
        for step in (8, -8, 1, -1):
            curr = king_pos
            while True:
                if (step == 1 and curr % 8 == 7) or (step == -1 and curr % 8 == 0) or \
                   (step == 8 and curr // 8 == 7) or (step == -8 and curr // 8 == 0): break
                curr += step
                p = self.grid[curr]
                if p:
                    if p == enemy_rook: return True
                    break
        
        # Check King proximity
        enemy_king_pos = self.kings[enemy_color]
        return enemy_king_pos in KING_MOVES[king_pos]

    def get_legal_moves(self, color):
        legal_moves = []
        enemy_color = BLACK if color == WHITE else WHITE
        
        for src in list(self.pieces[color]):
            p_val = self.grid[src]
            is_king = p_val & KING
            
            targets = []
            if is_king:
                targets = KING_MOVES[src]
            else: # ROOK
                for step in (8, -8, 1, -1):
                    curr = src
                    while True:
                        if (step == 1 and curr % 8 == 7) or (step == -1 and curr % 8 == 0) or \
                           (step == 8 and curr // 8 == 7) or (step == -8 and curr // 8 == 0): break
                        curr += step
                        targets.append(curr)
                        if self.grid[curr]: break

            for dst in targets:
                target_p = self.grid[dst]
                if target_p and (target_p & (WHITE | BLACK)) == color: continue
                
                # Execute move
                self.remove_piece(src)
                if target_p: self.remove_piece(dst)
                self.set_piece(dst, p_val)
                
                # Verify legality
                if not self.is_in_check(color):
                    cap = "x" if target_p else ""
                    prefix = "K" if is_king else "R"
                    legal_moves.append(f"{prefix}{cap}{IDX_TO_SQ[dst]}")
                
                # Revert move
                self.remove_piece(dst)
                if target_p: self.set_piece(dst, target_p)
                self.set_piece(src, p_val)
        
        return sorted(list(set(legal_moves)))

    def apply_san(self, san, color):
        s = san.strip("+#!?x ")
        dest_idx = SQ_TO_IDX.get(s[-2:])
        p_type = KING if s[0] == 'K' else ROOK
        
        # Efficiently find which piece can move to the destination
        for idx in self.pieces[color]:
            if (self.grid[idx] & (ROOK | KING)) == p_type:
                # Note: In specific puzzles, we assume one valid piece per SAN token
                self.move_piece(idx, dest_idx)
                break

    def pos_string(self):
        res = []
        for c in [WHITE, BLACK]:
            for idx in self.pieces[c]:
                p = self.grid[idx]
                p_str = ("W" if p & WHITE else "B") + ("R" if p & ROOK else "K")
                res.append(f"{p_str}{IDX_TO_SQ[idx]}")
        res.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(res)