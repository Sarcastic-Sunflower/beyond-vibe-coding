def get_legal_moves(board):
    moves = []
    wk_idx = board.pieces["WK"]
    wr_idx = board.pieces["WR"]
    bk_idx = board.pieces["BK"]
    
    # --- White King Moves ---
    f, r = wk_idx % 8, wk_idx // 8
    for df in [-1, 0, 1]:
        for dr in [-1, 0, 1]:
            if df == 0 and dr == 0: continue
            nf, nr = f + df, r + dr
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = nr * 8 + nf
                if target not in [wr_idx, bk_idx]:
                    moves.append(f"K{board.SQUARES[target]}")

    # --- White Rook Moves ---
    rf, rr = wr_idx % 8, wr_idx // 8
    for df, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for step in range(1, 8):
            nf, nr = rf + (df * step), rr + (dr * step)
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = nr * 8 + nf
                if target == wk_idx: break 
                if target == bk_idx:
                    moves.append(f"Rx{board.SQUARES[target]}")
                    break
                moves.append(f"R{board.SQUARES[target]}")
            else: break
            
    return sorted(moves)