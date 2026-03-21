# constants.py
from enum import IntEnum

class Color(IntEnum):
    WHITE = 0
    BLACK = 1

class Piece(IntEnum):
    ROOK = 0
    KING = 1

# Bitboard helpers
def set_bit(bb: int, sq: int) -> int: return bb | (1 << sq)
def get_sq(bb: int):
    while bb:
        r = (bb & -bb).bit_length() - 1
        yield r
        bb &= bb - 1

FILES = "abcdefgh"
RANKS = "12345678"
SQ_TO_IDX = {f"{f}{r}": r_idx * 8 + f_idx for r_idx, r in enumerate(RANKS) for f_idx, f in enumerate(FILES)}
IDX_TO_SQ = {idx: sq for sq, idx in SQ_TO_IDX.items()}