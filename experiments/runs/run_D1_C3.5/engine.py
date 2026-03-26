def get_legal_moves(board, piece_filter=None, include_details=False):
    moves = []
    current_turn = board.turn
    opponent = "B" if current_turn == "W" else "W"
    
    # Pre-calculated offsets for 1D array navigation
    # Up: +8, Down: -8, Right: +1, Left: -1
    ROOK_OFFSETS = [8, -8, 1, -1]
    KING_OFFSETS = [8, -8, 1, -1, 7, 9, -7, -9]

    for i in board.occupied:
        piece = board.board[i]
        if piece[0] != current_turn:
            continue
            
        ptype = piece[1]
        if piece_filter and ptype != piece_filter:
            continue

        if ptype == "R":
            for offset in ROOK_OFFSETS:
                for step in range(1, 8):
                    target_idx = i + (offset * step)
                    
                    # Boundary checks for 1D array
                    if not (0 <= target_idx < 64): break
                    # Horizontal wrap-around prevention
                    if offset in [1, -1] and (target_idx // 8 != i // 8): break
                    
                    target_piece = board.board[target_idx]
                    san_sq = board.IDX_TO_SAN[target_idx]
                    
                    if not target_piece:
                        moves.append({"san": f"R{san_sq}", "start": i, "end": target_idx})
                    elif target_piece[0] == opponent:
                        moves.append({"san": f"Rx{san_sq}", "start": i, "end": target_idx})
                        break
                    else:
                        break
                        
        elif ptype == "K":
            for offset in KING_OFFSETS:
                target_idx = i + offset
                if 0 <= target_idx < 64:
                    # Prevent illegal wrap-around for king moves
                    if abs((target_idx % 8) - (i % 8)) > 1: continue
                    
                    target_piece = board.board[target_idx]
                    san_sq = board.IDX_TO_SAN[target_idx]
                    prefix = "K" if not target_piece else "Kx"
                    
                    if not target_piece or target_piece[0] == opponent:
                        moves.append({"san": f"{prefix}{san_sq}", "start": i, "end": target_idx})

    if include_details:
        return moves
    
    # Using set() to ensure uniqueness before sorting
    return sorted(list(set(m['san'] for m in moves)))