# engine.py
from constants import Color, Piece, SQ_TO_IDX, IDX_TO_SQ, set_bit, get_sq

class ChessEngine:
    def __init__(self):
        # Index 0: White, Index 1: Black
        self.pieces = [[0, 0], [0, 0]] 
        self.turn = Color.WHITE

    def setup(self):
        self.add_piece(Color.WHITE, Piece.ROOK, SQ_TO_IDX["b6"])
        self.add_piece(Color.WHITE, Piece.KING, SQ_TO_IDX["g4"])
        self.add_piece(Color.BLACK, Piece.KING, SQ_TO_IDX["g6"])

    def add_piece(self, color, p_type, sq):
        self.pieces[color][p_type] = set_bit(self.pieces[color][p_type], sq)

    @property
    def occupied(self):
        return (self.pieces[0][0] | self.pieces[0][1] | 
                self.pieces[1][0] | self.pieces[1][1])

    def is_square_attacked(self, sq, by_color):
        # King attacks
        enemy_king = self.pieces[by_color][Piece.KING]
        if self.get_king_mask(sq) & enemy_king:
            return True
        # Rook attacks (Sliding)
        enemy_rooks = self.pieces[by_color][Piece.ROOK]
        if self.get_rook_mask(sq, self.occupied) & enemy_rooks:
            return True
        return False

    def get_king_mask(self, sq):
        mask = 0
        r, f = divmod(sq, 8)
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0: continue
                nr, nf = r + dr, f + df
                if 0 <= nr < 8 and 0 <= nf < 8:
                    mask |= (1 << (nr * 8 + nf))
        return mask

    def get_rook_mask(self, sq, occ):
        mask = 0
        r, f = divmod(sq, 8)
        for dr, df in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nf = r + dr, f + df
            while 0 <= nr < 8 and 0 <= nf < 8:
                t_sq = nr * 8 + nf
                mask |= (1 << t_sq)
                if occ & (1 << t_sq): break
                nr, nf = nr + dr, nf + df
        return mask

    def get_legal_moves(self, color):
        moves = []
        us, them = color, 1 - color
        
        # King Moves
        k_sq = next(get_sq(self.pieces[us][Piece.KING]))
        for target in get_sq(self.get_king_mask(k_sq) & ~self.get_color_bb(us)):
            if not self.test_move(us, Piece.KING, k_sq, target):
                cap = "x" if self.get_color_bb(them) & (1 << target) else ""
                moves.append(f"K{cap}{IDX_TO_SQ[target]}")

        # Rook Moves
        for r_sq in get_sq(self.pieces[us][Piece.ROOK]):
            for target in get_sq(self.get_rook_mask(r_sq, self.occupied) & ~self.get_color_bb(us)):
                if not self.test_move(us, Piece.ROOK, r_sq, target):
                    cap = "x" if self.get_color_bb(them) & (1 << target) else ""
                    moves.append(f"R{cap}{IDX_TO_SQ[target]}")
        
        return sorted(list(set(moves)))

    def get_color_bb(self, color):
        return self.pieces[color][0] | self.pieces[color][1]

    def test_move(self, color, p_type, src, dst):
        # Temporary move execution to check for legality (king safety)
        orig_us = [p for p in self.pieces[color]]
        orig_them = [p for p in self.pieces[1-color]]
        
        self.pieces[color][p_type] &= ~(1 << src)
        self.pieces[color][p_type] |= (1 << dst)
        # Capture logic
        self.pieces[1-color][0] &= ~(1 << dst)
        self.pieces[1-color][1] &= ~(1 << dst)
        
        king_sq = next(get_sq(self.pieces[color][Piece.KING]))
        in_check = self.is_square_attacked(king_sq, 1-color)
        
        self.pieces[color], self.pieces[1-color] = orig_us, orig_them
        return in_check

    def apply_san(self, san):
        clean_san = san.strip("+#!?x ")
        p_type = Piece.KING if clean_san[0] == 'K' else Piece.ROOK
        dest = SQ_TO_IDX[clean_san[-2:]]
        
        # Find the piece that can move there
        for sq in get_sq(self.pieces[self.turn][p_type]):
            # In this specific simplified engine, we assume the first found valid piece moves
            self.pieces[self.turn][p_type] &= ~(1 << sq)
            self.pieces[self.turn][p_type] |= (1 << dest)
            # Handle capture
            self.pieces[1-self.turn][0] &= ~(1 << dest)
            self.pieces[1-self.turn][1] &= ~(1 << dest)
            break
        self.turn = 1 - self.turn

    def get_pos_string(self):
        res = []
        for p in get_sq(self.pieces[0][Piece.ROOK]): res.append(f"WR{IDX_TO_SQ[p]}")
        for p in get_sq(self.pieces[0][Piece.KING]): res.append(f"WK{IDX_TO_SQ[p]}")
        for p in get_sq(self.pieces[1][Piece.ROOK]): res.append(f"BR{IDX_TO_SQ[p]}")
        for p in get_sq(self.pieces[1][Piece.KING]): res.append(f"BK{IDX_TO_SQ[p]}")
        res.sort(key=lambda x: (0 if x[0]=='W' else 1, x[1], x[2:]))
        return ";".join(res)