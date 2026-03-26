def get_legal_moves(board, include_details=False):
    moves = []
    current_turn = board.turn
    opp_color = "B" if current_turn == "W" else "W"

    for i in range(64):
        piece = board.board[i]
        if not piece or piece[0] != current_turn:
            continue

        ptype = piece[1]
        
        # Rook Logic: Sliding moves
        if ptype == "R":
            # Up, Down, Right, Left
            directions = [8, -8, 1, -1]
            for offset in directions:
                for step in range(1, 8):
                    target = i + (offset * step)
                    if not (0 <= target < 64): break
                    
                    # Horizontal wrap-around protection
                    if offset in [1, -1] and (target // 8 != i // 8): break
                    
                    target_piece = board.board[target]
                    sq_san = board.IDX_TO_SAN[target]
                    
                    if not target_piece:
                        moves.append({"san": f"R{sq_san}", "start": i, "end": target})
                    else:
                        if target_piece[0] == opp_color:
                            moves.append({"san": f"Rx{sq_san}", "start": i, "end": target})
                        break # Blocked by any piece

        # King Logic: Single step
        elif ptype == "K":
            offsets = [8, -8, 1, -1, 7, 9, -7, -9]
            for offset in offsets:
                target = i + offset
                if 0 <= target < 64:
                    # Multi-row jump protection
                    if abs((target % 8) - (i % 8)) > 1: continue
                    
                    target_piece = board.board[target]
                    sq_san = board.IDX_TO_SAN[target]
                    
                    if not target_piece:
                        moves.append({"san": f"K{sq_san}", "start": i, "end": target})
                    elif target_piece[0] == opp_color:
                        moves.append({"san": f"Kx{sq_san}", "start": i, "end": target})

    if include_details:
        return moves
    # Sort for exact output matching
    return sorted(list(set(m['san'] for m in moves)))