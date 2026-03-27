def get_legal_moves(board):
    moves = []
    wk, wr, bk = board.pieces["WK"], board.pieces["WR"], board.pieces["BK"]
    
    # White King Moves
    f, r = wk % 8, wk // 8
    for df in [-1, 0, 1]:
        for dr in [-1, 0, 1]:
            if df == 0 and dr == 0: continue
            nf, nr = f + df, r + dr
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = nr * 8 + nf
                if target not in [wr, bk]:
                    moves.append(f"K{board.SQUARES[target]}")
                elif target == bk:
                    moves.append(f"Kx{board.SQUARES[target]}")

    # White Rook Moves
    rf, rr = wr % 8, wr // 8
    for df, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for step in range(1, 8):
            nf, nr = rf + (df * step), rr + (dr * step)
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = nr * 8 + nf
                if target == wk: break
                moves.append(f"R{board.SQUARES[target]}")
                if target == bk:
                    moves.append(f"Rx{board.SQUARES[target]}")
                    break
            else: break
            
    # Legacy sorting requirement: by target square string
    return sorted(list(set(moves)), key=lambda m: m[1:])