def get_legal_moves(board):
    sq = board.SQUARES
    wr, wk, bk = board.wr, board.wk, board.bk
    moves = []

    # King Steps: [Up, Down, Left, Right, Diagonals]
    for diff in [-9, -8, -7, -1, 1, 7, 8, 9]:
        target = wk + diff
        if 0 <= target < 64:
            # Check for board wrap-around
            if abs((wk % 8) - (target % 8)) <= 1:
                if target != wr and target != bk:
                    moves.append(f"K{sq[target]}")

    # Rook Slides: [Right, Left, Up, Down]
    for step in [1, -1, 8, -8]:
        for i in range(1, 8):
            target = wr + (step * i)
            if not (0 <= target < 64): break
            # Horizontal wrap-around check
            if step in [1, -1] and (wr // 8 != target // 8): break
            
            if target == wk: break
            
            moves.append(f"R{sq[target]}")
            if target == bk:
                moves.append(f"Rx{sq[target]}")
                break
    
    # Sort by target square for legacy consistency
    return sorted(list(set(moves)), key=lambda x: (x[-2:], x))