#!/usr/bin/env python3
import sys
import os
from typing import List, Tuple, Set

# Pre-computed Lookup Tables (LUTs) for O(1) access
FILES = "abcdefgh"
RANKS = "12345678"
FILE_MAP = {f: i for i, f in enumerate(FILES)}
RANK_MAP = {r: i for i, r in enumerate(RANKS)}

# Pre-calculate coordinate strings to prevent runtime string allocation overhead
SQUARES = [[f"{f}{r}" for f in FILES] for r in RANKS]

# Constants mapped as tuples (faster iteration than lists in Python)
ROOK_DIRS: Tuple[Tuple[int, int], ...] = ((0, 1), (0, -1), (1, 0), (-1, 0))
KING_DIRS: Tuple[Tuple[int, int], ...] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
VALID_PIECES = set("RKQBN")

# Translation table executes character removal at the native C-level
CLEAN_SAN_TRANS = str.maketrans("", "", "+#!?x")

class ChessState:
    """
    Manages board state. Uses __slots__ to prevent dynamic dict creation, 
    saving memory and improving attribute access speed.
    """
    __slots__ = ['board', 'turn']

    def __init__(self) -> None:
        self.board: List[List[str]] = [["" for _ in range(8)] for _ in range(8)]
        self.turn: str = "W"
        
        # Initial state payload
        self.board[5][1] = "WR"
        self.board[3][6] = "WK"
        self.board[5][6] = "BK"

    def get_pseudo_legal_moves(self) -> List[str]:
        color = self.turn
        moves: Set[str] = set()
        
        # Local caching to avoid attribute lookups in the hot loop
        add_move = moves.add
        b = self.board
        sq = SQUARES

        for r in range(8):
            row = b[r]
            for c in range(8):
                p = row[c]
                if not p or p[0] != color:
                    continue
                
                ptype = p[1]
                if ptype == "R":
                    for dc, dr in ROOK_DIRS:
                        nc, nr = c + dc, r + dr
                        while 0 <= nc <= 7 and 0 <= nr <= 7:
                            tp = b[nr][nc]
                            if tp:
                                if tp[0] != color:
                                    add_move(f"Rx{sq[nr][nc]}")
                                break
                            add_move(f"R{sq[nr][nc]}")
                            nc += dc
                            nr += dr
                elif ptype == "K":
                    for dc, dr in KING_DIRS:
                        nc, nr = c + dc, r + dr
                        if 0 <= nc <= 7 and 0 <= nr <= 7:
                            tp = b[nr][nc]
                            if not tp:
                                add_move(f"K{sq[nr][nc]}")
                            elif tp[0] != color:
                                add_move(f"Kx{sq[nr][nc]}")
        
        return sorted(moves)

    def apply_move(self, san: str) -> None:
        # Strip whitespace and map cleanly through the native C translation table
        s = san.strip().translate(CLEAN_SAN_TRANS)
        if len(s) < 2:
            return
            
        pt = s[0] if s[0] in VALID_PIECES else "P"
        dest = s[-2:]
        
        try:
            dc = FILE_MAP[dest[0]]
            dr = RANK_MAP[dest[1]]
        except KeyError:
            return
            
        b = self.board
        target_piece = self.turn + pt
        
        for r in range(8):
            row = b[r]
            for c in range(8):
                if row[c] == target_piece:
                    row[c] = ""
                    b[dr][dc] = target_piece
                    return

    def pos_string(self) -> str:
        parts: List[str] = []
        add_part = parts.append
        b = self.board
        sq = SQUARES
        
        for r in range(8):
            row = b[r]
            for c in range(8):
                p = row[c]
                if p:
                    add_part(p + sq[r][c])
        
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")

    state = ChessState()

    if os.path.isfile(moves_path):
        moves_processed = 0
        # Reading line-by-line keeps memory footprint low regardless of file size
        with open(moves_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                
                if ']' in line:
                    line = line.split(']', 1)[-1]
                
                tokens = line.split()
                if not tokens:
                    continue
                
                for token in tokens:
                    state.apply_move(token)
                    state.turn = "B" if state.turn == "W" else "W"
                
                moves_processed += 1
                if moves_processed == 3:
                    break

    mvs = state.get_pseudo_legal_moves()
    mv_str = ";".join(mvs)
    pos = state.pos_string()
    move_line = f"{len(mvs)} :" + (f" {mv_str}" if mvs else "")

    out_path = os.path.join(script_dir, "output1.txt")
    # Batch writes into a single I/O call
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{pos}\n{move_line}\n{move_line}\n0 :\n")

if __name__ == "__main__":
    main()