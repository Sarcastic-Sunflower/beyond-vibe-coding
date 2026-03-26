def get_legal_moves(board, piece_filter=None, include_details=False):
    moves = []
    color = board.turn
    opp = "B" if color == "W" else "W"
    
    offsets = {
        "R": [(0,1), (0,-1), (1,0), (-1,0)], 
        "K": [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    }

    for i in range(64):
        p = board.board[i]
        if not p or p[0] != color: continue
        ptype = p[1]
        if piece_filter and ptype != piece_filter: continue

        r, c = divmod(i, 8)
        if ptype == "R":
            for dr, dc in offsets["R"]:
                for step in range(1, 8):
                    nr, nc = r + dr*step, c + dc*step
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        ni = nr * 8 + nc
                        target = board.board[ni]
                        san_sq = board.IDX_TO_SAN[ni]
                        if not target:
                            moves.append({"san": f"R{san_sq}", "start": i, "end": ni})
                        elif target[0] == opp:
                            moves.append({"san": f"Rx{san_sq}", "start": i, "end": ni})
                            break
                        else: break
                    else: break
        elif ptype == "K":
            for dr, dc in offsets["K"]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    ni = nr * 8 + nc
                    target = board.board[ni]
                    san_sq = board.IDX_TO_SAN[ni]
                    if not target:
                        moves.append({"san": f"K{san_sq}", "start": i, "end": ni})
                    elif target[0] == opp:
                        moves.append({"san": f"Kx{san_sq}", "start": i, "end": ni})

    if include_details: return moves
    return sorted(list(set(m['san'] for m in moves)))