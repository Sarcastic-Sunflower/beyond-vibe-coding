def get_legal_moves(board, piece_filter=None):
    moves = []
    color = board.turn
    opp_color = "B" if color == "W" else "W"
    
    for idx, piece in board.pieces.items():
        if piece[0] != color: continue
        ptype = piece[1]
        
        # Apply filter if provided (to match Line 4's specific requirement)
        if piece_filter and ptype != piece_filter: continue
        
        r, c = divmod(idx, 8)
        
        if ptype == "R":
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = nr * 8 + nc
                        target = board.pieces.get(n_idx)
                        dest = board.from_idx(n_idx)
                        if target:
                            if target[0] == opp_color:
                                moves.append(f"R{dest}")
                                moves.append(f"Rx{dest}")
                            break
                        moves.append(f"R{dest}")
                    else: break
        
        elif ptype == "K":
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = nr * 8 + nc
                        target = board.pieces.get(n_idx)
                        dest = board.from_idx(n_idx)
                        if not target:
                            moves.append(f"K{dest}")
                        elif target[0] == opp_color:
                            moves.append(f"K{dest}")
                            moves.append(f"Kx{dest}")
                            
    return sorted(list(set(moves)))