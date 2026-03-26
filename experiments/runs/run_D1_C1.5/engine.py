#!/usr/bin/env python3

class ChessEngine:
    # Use __slots__ to reduce memory footprint and speed up attribute access
    __slots__ = ['board', 'turn', 'white_pieces', 'black_pieces']
    
    FILES = "abcdefgh"
    RANKS = "12345678"
    
    def __init__(self):
        # 1D array (index = row * 8 + col) is faster than 2D access
        self.board = [None] * 64
        self.turn = "W"
        
        # Initializing specific position
        self.board[41] = "WR" # b6: (5*8) + 1
        self.board[30] = "WK" # g4: (3*8) + 6
        self.board[46] = "BK" # g6: (5*8) + 6

    def _to_idx(self, coord: str) -> int:
        # Optimized index calculation using ASCII offsets
        return (ord(coord[1]) - 49) * 8 + (ord(coord[0]) - 97)

    def apply_move(self, san: str):
        if not san: return
        
        target_idx = self._to_idx(san[-2:])
        piece_type = san[0] if san[0] in "RKQBN" else "P"
        target_prefix = self.turn + piece_type

        # Efficient single-pass search for the moving piece
        for idx, piece in enumerate(self.board):
            if piece == target_prefix:
                self.board[idx] = None
                self.board[target_idx] = target_prefix
                self.turn = "B" if self.turn == "W" else "W"
                break

    def get_moves(self, color: str):
        moves = []
        opp_color = "B" if color == "W" else "W"
        
        for idx, piece in enumerate(self.board):
            if not piece or piece[0] != color:
                continue
            
            ptype = piece[1]
            r, c = divmod(idx, 8)
            
            if ptype == "R":
                for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = nr * 8 + nc
                        target = self.board[n_idx]
                        if target and target[0] == color: break
                        
                        # Use join/list for string building in tight loops
                        moves.append(f"R{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}")
                        if target: break
                        nr, nc = nr + dr, nc + dc
            
            elif ptype == "K":
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            n_idx = nr * 8 + nc
                            target = self.board[n_idx]
                            if not target or target[0] == opp_color:
                                moves.append(f"K{'x' if target else ''}{self.FILES[nc]}{self.RANKS[nr]}")
        
        moves.sort()
        return moves

    def get_position_string(self):
        # Generator expression for speed and memory efficiency
        res = [f"{p}{self.FILES[i % 8]}{self.RANKS[i // 8]}" 
               for i, p in enumerate(self.board) if p]
        res.sort()
        return ";".join(res)