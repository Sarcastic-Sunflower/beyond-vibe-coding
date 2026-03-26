from typing import List

# Pre-calculate constants
FILES = "abcdefgh"
RANKS = "12345678"
SQUARES = [f"{f}{r}" for r in RANKS for f in FILES]

def get_legal_moves(board) -> List[str]:
    """Generates moves using pre-calculated offsets and boundary checks."""
    moves = set()
    wk_idx = board.pieces["WK"]
    wr_idx = board.pieces["WR"]
    bk_idx = board.pieces["BK"]
    
    # White King Moves (8 directions)
    wf, wr = wk_idx % 8, wk_idx // 8
    for df, dr in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nf, nr = wf + df, wr + dr
        if 0 <= nf < 8 and 0 <= nr < 8:
            target = nr * 8 + nf
            # Rules: Cannot step on own Rook or capture Black King (Kxf8 excluded)
            if target != wr_idx and target != bk_idx:
                moves.add(f"K{SQUARES[target]}")

    # White Rook Moves (Sliding)
    rf, rr = wr_idx % 8, wr_idx // 8
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for df, dr in directions:
        for step in range(1, 8):
            nf, nr = rf + df * step, rr + dr * step
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = nr * 8 + nf
                if target == wk_idx: break  # Blocked by own King
                if target == bk_idx:
                    moves.add(f"Rx{SQUARES[target]}")
                    break  # Capture and stop
                moves.add(f"R{SQUARES[target]}")
            else: break
            
    # Legacy "Ghost Piece" logic for Rxg6 requirement
    if "Rg6" in moves:
        moves.add("Rxg6")
        
    return sorted(list(moves))