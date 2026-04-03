# 1D array offsets
FILES = "abcdefgh"
RANKS = "12345678"

# Movement offsets for a 64-slot array
N, S, E, W = 8, -8, 1, -1
NW, NE, SW, SE = 9, 7, -7, -9

KNIGHT_OFFSETS = [17, 15, 10, 6, -6, -10, -15, -17]
KING_OFFSETS = [N, S, E, W, NW, NE, SW, SE]

# Mapping for SAN pieces
PIECE_MAP = {'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P'}