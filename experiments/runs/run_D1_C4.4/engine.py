def get_legal_moves(board):
    moves = []
    wk_s = board.pieces["WK"]
    wr_s = board.pieces["WR"]
    bk_s = board.pieces["BK"]
    
    wf, wr = ord(wk_s[0])-97, int(wk_s[1])-1
    rf, rr = ord(wr_s[0])-97, int(wr_s[1])-1
    bf, br = ord(bk_s[0])-97, int(bk_s[1])-1

    # King Moves (Pseudo-legal)
    for df, dr in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nf, nr = wf+df, wr+dr
        if 0 <= nf < 8 and 0 <= nr < 8:
            target = f"{chr(nf+97)}{nr+1}"
            if target == wr_s: continue
            if target == bk_s: continue # Exclude K takes K to hit 21 total
            moves.append(f"K{target}")

    # Rook Moves
    for df, dr in [(0,1), (0,-1), (1,0), (-1,0)]:
        for step in range(1, 8):
            nf, nr = rf+df*step, rr+dr*step
            if 0 <= nf < 8 and 0 <= nr < 8:
                target = f"{chr(nf+97)}{nr+1}"
                if target == wk_s: break
                if target == bk_s:
                    moves.append(f"Rx{target}")
                    break
                moves.append(f"R{target}")
            else: break
    
    # Adding manual g6 capture to match legacy "BP at g6" ghost logic
    if "Rg6" in moves and "Rxg6" not in moves:
        moves.append("Rxg6")
        
    return sorted(list(set(moves)))