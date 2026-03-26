def get_legal_moves(board):
    moves = []
    color = board.turn
    opp_color = "B" if color == "W" else "W"
    
    for idx, piece in board.pieces.items():
        if piece[0] != color: continue
        
        ptype = piece[1]
        r, c = divmod(idx, 8)
        
        # Rook Logic
        if ptype == "R":
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = nr * 8 + nc
                        target = board.pieces.get(n_idx)
                        if target:
                            if target[0] == opp_color:
                                moves.append(f"R{board.from_idx(n_idx)}") # Basic move
                                moves.append(f"Rx{board.from_idx(n_idx)}") # Capture move
                            break # Blocked
                        moves.append(f"R{board.from_idx(n_idx)}")
                    else: break
        
        # King Logic
        elif ptype == "K":
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = nr * 8 + nc
                        target = board.pieces.get(n_idx)
                        if not target:
                            moves.append(f"K{board.from_idx(n_idx)}")
                        elif target[0] == opp_color:
                            moves.append(f"Kx{board.from_idx(n_idx)}")
                            
    return sorted(list(set(moves))) # Ensure uniqueness and alphabetical order