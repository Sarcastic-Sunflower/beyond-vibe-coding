def get_legal_moves(board, piece_filter=None, include_details=False):
    moves = []
    color = board.turn
    opp_color = "B" if color == "W" else "W"
    
    offsets = {
        "R": [(0, 1), (0, -1), (1, 0), (-1, 0)],
        "K": [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    }

    for idx in board.piece_indices:
        piece = board.board[idx]
        if piece[0] != color: continue
        ptype = piece[1]
        if piece_filter and ptype != piece_filter: continue
        
        r, c = divmod(idx, 8)
        
        if ptype == "R":
            for dr, dc in offsets["R"]:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        n_idx = (nr << 3) + nc
                        target = board.board[n_idx]
                        dest_san = board.IDX_TO_SAN[n_idx]
                        
                        if not target:
                            moves.append({"san": f"R{dest_san}", "start_idx": idx, "dest_idx": n_idx, "type": "R"})
                        elif target[0] == opp_color:
                            moves.append({"san": f"Rx{dest_san}", "start_idx": idx, "dest_idx": n_idx, "type": "R"})
                            break
                        else: break
                    else: break
        
        elif ptype == "K":
            for dr, dc in offsets["K"]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    n_idx = (nr << 3) + nc
                    target = board.board[n_idx]
                    dest_san = board.IDX_TO_SAN[n_idx]
                    if not target:
                        moves.append({"san": f"K{dest_san}", "start_idx": idx, "dest_idx": n_idx, "type": "K"})
                    elif target[0] == opp_color:
                        moves.append({"san": f"Kx{dest_san}", "start_idx": idx, "dest_idx": n_idx, "type": "K"})
                            
    if include_details:
        return moves
    
    # Return formatted strings sorted alphabetically
    return sorted(list(set(m['san'] for m in moves)))