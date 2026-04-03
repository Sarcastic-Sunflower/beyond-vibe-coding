FILES = "abcdefgh"
RANKS = "12345678"

# Directional Offsets for 1D Array
UP, DOWN, LEFT, RIGHT = 8, -8, -1, 1
VECTORS = [UP, DOWN, LEFT, RIGHT, UP+LEFT, UP+RIGHT, DOWN+LEFT, DOWN+RIGHT]
KNIGHT_OFFSETS = [17, 15, 10, 6, -6, -10, -15, -17]

# Pre-map squares to 1D index
SQR_MAP = {f"{f}{r}": i * 8 + j for i, r in enumerate(RANKS) for j, f in enumerate(FILES)}
REV_SQR_MAP = {v: k for k, v in SQR_MAP.items()}