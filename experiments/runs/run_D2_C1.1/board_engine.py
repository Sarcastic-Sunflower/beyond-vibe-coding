FILES = "abcdefgh"
RANKS = "12345678"

class Piece:
    def __init__(self, color, p_type):
        self.color = color  # 'W' or 'B'
        self.p_type = p_type  # 'K', 'N', 'P', etc.

    def __str__(self):
        return f"{self.color}{self.p_type}"

class ChessBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def setup_initial(self):
        # Initial positions from legacy script
        self.place("b7", Piece("B", "K"))
        self.place("c4", Piece("B", "N"))
        self.place("d6", Piece("W", "P"))
        self.place("e5", Piece("W", "P"))
        self.place("a5", Piece("W", "K"))

    def place(self, coord, piece):
        c, r = FILES.index(coord[0]), RANKS.index(coord[1])
        self.grid[r][c] = piece

    def get_piece_at(self, r, c):
        return self.grid[r][c]

    def move_piece(self, move_san, color):
        # Simplified SAN parser for the required moves
        san = move_san.replace("+", "").replace("#", "").replace("x", "")
        
        # Handle Pawn promotion notation (e.g., dxc8=Q)
        if "=" in san:
            san = san.split("=")[0]
            
        dest_str = san[-2:]
        p_type = san[0] if san[0] in "RKQBN" else "P"
        
        dr, dc = RANKS.index(dest_str[1]), FILES.index(dest_str[0])

        # Find the piece that can move there
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and p.p_type == p_type:
                    # Execute move
                    self.grid[dr][dc] = p
                    self.grid[r][c] = None
                    return

    def get_black_moves(self):
        all_moves, legal, illegal = [], [], []
        
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if not p or p.color != "B":
                    continue
                
                offsets = []
                if p.p_type == "N":
                    offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
                elif p.p_type == "K":
                    offsets = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

                for dc, dr in offsets:
                    nc, nr = c + dc, r + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        move_str = f"{p.p_type}{FILES[nc]}{RANKS[nr]}"
                        all_moves.append(move_str)
                        target = self.grid[nr][nc]
                        if target and target.color == "B":
                            illegal.append(move_str)
                        else:
                            legal.append(move_str)
        return all_moves, legal, illegal

    def get_position_string(self):
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    parts.append(f"{p}{FILES[c]}{RANKS[r]}")
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)