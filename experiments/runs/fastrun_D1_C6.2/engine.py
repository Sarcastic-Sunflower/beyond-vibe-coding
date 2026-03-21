# engine.py
FILES, RANKS = "abcdefgh", "12345678"
SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}

WHITE, BLACK = 8, 16
ROOK, KING = 1, 2

class Board:
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
        if not p: return
        self.grid[idx] = 0
        self.pieces[p & (WHITE | BLACK)].remove(idx)

    def move_piece(self, src, dst):
        p = self.grid[src]
        self.remove_piece(src)
        if self.grid[dst]: self.remove_piece(dst)
        self.set_piece(dst, p)

    def is_attacked(self, target_idx, attacker_color):
        # Check Rook/King attacks for move legality
        enemy_rook = attacker_color | ROOK
        enemy_king = attacker_color | KING
        
        # Sliding attacks (Rook)
        for step in (8, -8, 1, -1):
            curr = target_idx
            while True:
                if (step == 1 and curr % 8 == 7) or (step == -1 and curr % 8 == 0) or \
                   (step == 8 and curr // 8 == 7) or (step == -8 and curr // 8 == 0): break
                curr += step
                p = self.grid[curr]
                if p:
                    if p == enemy_rook: return True
                    break
        
        # King adjacency
        tr, tf = divmod(target_idx, 8)
        er, ef = divmod(self.kings[attacker_color], 8)
        return max(abs(tr - er), abs(tf - ef)) <= 1

    def get_legal_moves(self, color):
        moves = []
        enemy = BLACK if color == WHITE else WHITE
        for src in list(self.pieces[color]):
            p_val = self.grid[src]
            ptype = p_val & (ROOK | KING)
            
            targets = []
            if ptype == KING:
                r, f = divmod(src, 8)
                for dr in (-1, 0, 1):
                    for df in (-1, 0, 1):
                        if dr == 0 and df == 0: continue
                        nr, nf = r + dr, f + df
                        if 0 <= nr < 8 and 0 <= nf < 8: targets.append(nr * 8 + nf)
            else:
                for step in (8, -8, 1, -1):
                    curr = src
                    while True:
                        if (step == 1 and curr % 8 == 7) or (step == -1 and curr % 8 == 0) or \
                           (step == 8 and curr // 8 == 7) or (step == -8 and curr // 8 == 0): break
                        curr += step
                        targets.append(curr)
                        if self.grid[curr]: break

            for dst in targets:
                if self.grid[dst] and (self.grid[dst] & (WHITE | BLACK)) == color: continue
                
                # Test legality
                orig_dst_p = self.grid[dst]
                self.move_piece(src, dst)
                if not self.is_attacked(self.kings[color], enemy):
                    prefix = "K" if ptype == KING else "R"
                    cap = "x" if orig_dst_p else ""
                    moves.append(f"{prefix}{cap}{IDX_TO_SQ[dst]}")
                # Revert
                self.move_piece(dst, src)
                if orig_dst_p: self.set_piece(dst, orig_dst_p)
        
        return sorted(list(set(moves)))

    def apply_san(self, san, color):
        clean = san.strip("+#!?x ")
        dest_idx = SQ_TO_IDX[clean[-2:]]
        p_type = KING if clean[0] == 'K' else ROOK
        target_val = color | p_type
        
        for idx in list(self.pieces[color]):
            if self.grid[idx] == target_val:
                # In this context, we assume the first piece of type found is the mover
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