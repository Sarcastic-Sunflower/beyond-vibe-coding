def get_legal_moves(board):
    moves = []
    wk, wr, bk = board.pieces["WK"], board.pieces["WR"], board.pieces["BK"]
    
    # King Moves
    kx, ky = wk % 8, wk // 8
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: continue
            nx, ny = kx + dx, ky + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = ny * 8 + nx
                if target not in [wr, bk]:
                    moves.append(f"K{board.SQUARES[target]}")

    # Rook Moves (Sliding)
    rx, ry = wr % 8, wr // 8
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for i in range(1, 8):
            nx, ny = rx + (dx * i), ry + (dy * i)
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = ny * 8 + nx
                if target == wk: break
                moves.append(f"R{board.SQUARES[target]}")
                if target == bk:
                    moves.append(f"Rx{board.SQUARES[target]}")
                    break
            else: break
            
    # Legacy Sort: Piece + Coordinate sorting
    return sorted(list(set(moves)), key=lambda x: (x[-2:], x))