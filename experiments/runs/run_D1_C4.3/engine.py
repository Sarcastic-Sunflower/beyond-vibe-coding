def get_legal_moves(board, include_details=False):
    moves = []
    current_turn = board.turn
    opp_color = "B" if current_turn == "W" else "W"

    for i in range(64):
        piece = board.board[i]
        if not piece or piece[0] != current_turn:
            continue

        ptype = piece[1]
        
        if ptype == "R":
            for offset in [8, -8, 1, -1]:
                for step in range(1, 8):
                    target = i + (offset * step)
                    if not (0 <= target < 64): break
                    if offset in [1, -1] and (target // 8 != i // 8): break
                    
                    target_piece = board.board[target]
                    sq = board.IDX_TO_SAN[target]
                    if not target_piece:
                        moves.append({"san": f"R{sq}", "start": i, "end": target})
                    else:
                        if target_piece[0] == opp_color:
                            moves.append({"san": f"Rx{sq}", "start": i, "end": target})
                        break

        elif ptype == "K":
            for offset in [8, -8, 1, -1, 7, 9, -7, -9]:
                target = i + offset
                if 0 <= target < 64 and abs((target % 8) - (i % 8)) <= 1:
                    target_piece = board.board[target]
                    sq = board.IDX_TO_SAN[target]
                    pref = "Kx" if (target_piece and target_piece[0] == opp_color) else "K"
                    if not target_piece or target_piece[0] == opp_color:
                        moves.append({"san": f"{pref}{sq}", "start": i, "end": target})

    return moves if include_details else sorted(list(set(m['san'] for m in moves)))