# Directional vectors for sliding pieces and others
DIRECTIONS = {
    'orthogonal': [(0, 1), (0, -1), (1, 0), (-1, 0)],
    'diagonal': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
    'knight': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
}
KING_OFFSETS = DIRECTIONS['orthogonal'] + DIRECTIONS['diagonal']

FILES = "abcdefgh"
RANKS = "12345678"