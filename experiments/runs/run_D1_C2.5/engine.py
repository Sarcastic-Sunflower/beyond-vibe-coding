# Offsets for Rook and King
R_OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
K_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def get_legal_moves(board, piece_filter=None):
    moves = []
    color = board.turn
    opp_color = "B" if color == "W" else "W"
    
    for idx in board.piece_indices:
        piece = board.board[idx]
        if piece[0] != color: continue
        ptype = piece[1]
        if piece_filter and ptype != piece_filter: continue
        
        r, c = divmod(idx, 8)
        
        if ptype == "R":
            for dr, dc in R_OFFSETS:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = (nr << 3) + nc # Bitshift for faster multiplication
                        dest = board.IDX_TO_SAN[n_idx]
                        target = board.board[n_idx]
                        if target:
                            if target[0] == opp_color:
                                moves.extend([f"R{dest}", f"Rx{dest}"])
                            break
                        moves.append(f"R{dest}")
                    else: break
        
        elif ptype == "K":
            for dr, dc in K_OFFSETS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    n_idx = (nr << 3) + nc
                    dest = board.IDX_TO_SAN[n_idx]
                    target = board.board[n_idx]
                    if not target:
                        moves.append(f"K{dest}")
                    elif target[0] == opp_color:
                        moves.extend([f"K{dest}", f"Kx{dest}"])
                            
    return sorted(set(moves))