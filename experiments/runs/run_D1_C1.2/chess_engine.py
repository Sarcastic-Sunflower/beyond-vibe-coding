class ChessBoard:
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "W"
        self._setup_initial_state()

    def _setup_initial_state(self):
        # Matching the specific starting state from your legacy script
        self.grid[5][1] = "WR" # b6
        self.grid[3][6] = "WK" # g4
        self.grid[5][6] = "BK" # g6

    def get_piece_at(self, r, c):
        return self.grid[r][c]

    def get_all_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.startswith(color):
                    moves.extend(self._generate_piece_moves(piece, r, c))
        return sorted(list(set(moves)))

    def _generate_piece_moves(self, piece, r, c):
        moves = []
        p_type = piece[1]
        color = piece[0]
        
        directions = []
        if p_type == "R":
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            limit = 8
        elif p_type == "K":
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            limit = 1
        
        for dc, dr in directions:
            for i in range(1, limit + 1):
                nc, nr = c + (dc * i), r + (dr * i)
                if 0 <= nc < 8 and 0 <= nr < 8:
                    target = self.grid[nr][nc]
                    dest_str = f"{self.FILES[nc]}{self.RANKS[nr]}"
                    
                    if not target:
                        moves.append(f"{p_type}{dest_str}")
                    elif target[0] != color:
                        moves.append(f"{p_type}x{dest_str}")
                        break
                    else:
                        break
                else:
                    break
        return moves

    def make_move(self, san):
        # Clean SAN string
        clean_san = san.translate(str.maketrans('', '', '+#!?'))
        is_capture = 'x' in clean_san
        dest_sq = clean_san[-2:]
        p_type = clean_san[0] if clean_san[0] in "RKQBN" else "P"
        
        target_r = self.RANKS.index(dest_sq[1])
        target_c = self.FILES.index(dest_sq[0])

        # Find the piece that can make this move
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p[0] == self.turn and p[1] == p_type:
                    # Simplified logic: move the first piece of type found
                    # In a full engine, we'd verify move legality here
                    self.grid[r][c] = None
                    self.grid[target_r][target_c] = p
                    self.turn = "B" if self.turn == "W" else "W"
                    return True
        return False

    def get_position_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    parts.append(f"{p}{self.FILES[c]}{self.RANKS[r]}")
        # Sort: White first, then Black, then piece type, then coordinate
        parts.sort(key=lambda x: (0 if x[0] == 'W' else 1, x[1], x[2:]))
        return ";".join(parts)