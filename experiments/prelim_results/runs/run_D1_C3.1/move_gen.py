from board import IDX_TO_SQ

# Extracted to (d_rank, d_file) to prevent Python modulo bugs on negative bounds
DIR_OFFSETS = {
    'R': [(1, 0), (-1, 0), (0, 1), (0, -1)],
    'K': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
}

def is_square_attacked(grid, sq_idx, attacker_color):
    """Reverse raycasting with strict 2D boundary limits."""
    sq_rank = sq_idx // 8
    sq_file = sq_idx % 8

    # 1. Check Straight Rays (Rooks)
    for dr, df in DIR_OFFSETS['R']:
        r, f = sq_rank + dr, sq_file + df
        while 0 <= r <= 7 and 0 <= f <= 7:
            idx = r * 8 + f
            p = grid[idx]
            if p:
                if p == attacker_color + 'R':
                    return True
                break
            r += dr
            f += df

    # 2. Check Adjacency (Kings)
    for dr, df in DIR_OFFSETS['K']:
        r, f = sq_rank + dr, sq_file + df
        if 0 <= r <= 7 and 0 <= f <= 7:
            p = grid[r * 8 + f]
            if p == attacker_color + 'K':
                return True

    return False

def get_legal_moves(board, color):
    legal_moves = []
    grid = board.grid
    opp_color = 'B' if color == 'W' else 'W'
    append_move = legal_moves.append
    
    for start_idx in range(64):
        p = grid[start_idx]
        if not p or p[0] != color:
            continue
            
        ptype = p[1]
        start_rank = start_idx // 8
        start_file = start_idx % 8
        
        if ptype == 'R':
            for dr, df in DIR_OFFSETS['R']:
                r, f = start_rank + dr, start_file + df
                while 0 <= r <= 7 and 0 <= f <= 7:
                    curr_idx = r * 8 + f
                    target_p = grid[curr_idx]
                    
                    if target_p and target_p[0] == color:
                        break # Blocked by friendly
                        
                    # Evaluate move in-place
                    grid[start_idx] = None
                    grid[curr_idx] = p
                    
                    # Validate safety
                    if not is_square_attacked(grid, board.king_idx[color], opp_color):
                        is_cap = "x" if target_p else ""
                        append_move(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                        
                    # Revert move
                    grid[start_idx] = p
                    grid[curr_idx] = target_p
                    
                    if target_p:
                        break # Stop sliding post-capture
                        
        elif ptype == 'K':
            for dr, df in DIR_OFFSETS['K']:
                r, f = start_rank + dr, start_file + df
                if 0 <= r <= 7 and 0 <= f <= 7:
                    target_idx = r * 8 + f
                    target_p = grid[target_idx]
                    
                    if not target_p or target_p[0] != color:
                        grid[start_idx] = None
                        grid[target_idx] = p
                        board.king_idx[color] = target_idx
                        
                        if not is_square_attacked(grid, target_idx, opp_color):
                            is_cap = "x" if target_p else ""
                            append_move(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                            
                        grid[start_idx] = p
                        grid[target_idx] = target_p
                        board.king_idx[color] = start_idx

    return sorted(list(set(legal_moves)))