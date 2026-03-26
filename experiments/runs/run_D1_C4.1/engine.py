def get_legal_moves(board, include_details=False):
    moves = []
    current_turn = board.turn
    opp_color = "B" if current_turn == "W" else "W"

    for i in range(64):
        piece = board.board[i]
        if not piece or piece[0] != current_turn:
            continue

        ptype = piece[1]
        
        # Rook Logic
        if ptype == "R":
            directions = [(8, "up"), (-8, "down"), (1, "right"), (-1, "left")]
            for offset, desc in directions:
                for step in range(1, 8):
                    target = i + (offset * step)
                    if not (0 <= target < 64): break
                    # Prevent horizontal wrap
                    if desc in ["right", "left"] and (target // 8 != i // 8): break
                    
                    target_piece = board.board[target]
                    san_sq = board.IDX_TO_SAN[target]
                    
                    if not target_piece:
                        moves.append({"san": f"R{san_sq}", "start": i, "end": target})
                    elif target_piece[0] == opp_color:
                        moves.append({"san": f"Rx{san_sq}", "start": i, "end": target})
                        break
                    else: break

        # King Logic
        elif ptype == "K":
            offsets = [8, -8, 1, -1, 7, 9, -7, -9]
            for offset in offsets:
                target = i + offset
                if 0 <= target < 64:
                    # Prevent illegal horizontal jumps (e.g., h-file to a-file)
                    if abs((target % 8) - (i % 8)) > 1: continue
                    
                    target_piece = board.board[target]
                    san_sq = board.IDX_TO_SAN[target]
                    prefix = "Kx" if (target_piece and target_piece[0] == opp_color) else "K"
                    
                    if not target_piece or target_piece[0] == opp_color:
                        moves.append({"san": f"{prefix}{san_sq}", "start": i, "end": target})

    if include_details:
        return moves
    return sorted(list(set(m['san'] for m in moves)))