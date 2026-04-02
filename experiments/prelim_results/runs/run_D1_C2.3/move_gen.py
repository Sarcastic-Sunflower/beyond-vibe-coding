from board import IDX_TO_SQ

# Precomputed directional offsets for a 1D 8x8 array
DIR_OFFSETS = {
    'R': (-8, 8, -1, 1),
    'K': (-9, -8, -7, -1, 1, 7, 8, 9)
}

def is_square_attacked(grid, sq_idx, attacker_color):
    """
    Reverse raycasting: Look outward from the square to find attackers.
    This is magnitudes faster than generating all opponent pseudo-legal moves.
    """
    sq_rank = sq_idx // 8
    sq_file = sq_idx % 8

    # 1. Check for attacking Rooks (Straight rays)
    for delta in DIR_OFFSETS['R']:
        curr_idx = sq_idx
        curr_rank, curr_file = sq_rank, sq_file
        
        while True:
            # Boundary checks mapped to 1D math
            next_rank = curr_rank + (delta // 8)
            next_file = curr_file + (delta % 8 if delta in (-1, 1) else 0)
            
            if not (0 <= next_rank <= 7 and 0 <= next_file <= 7):
                break
                
            curr_idx += delta
            curr_rank, curr_file = next_rank, next_file
            
            p = grid[curr_idx]
            if p:
                if p[0] == attacker_color and p[1] == 'R':
                    return True
                break # Blocked by another piece

    # 2. Check for attacking Kings (Adjacent squares)
    for delta in DIR_OFFSETS['K']:
        next_rank = sq_rank + (delta // 8)
        # Handle file wrap-around for diagonal offsets
        next_file = sq_file + (delta % 8 if delta % 8 < 4 else (delta % 8) - 8)
        
        if 0 <= next_rank <= 7 and 0 <= next_file <= 7:
            p = grid[sq_idx + delta]
            if p and p[0] == attacker_color and p[1] == 'K':
                return True

    return False

def get_legal_moves(board, color):
    legal_moves = []
    grid = board.grid
    opp_color = 'B' if color == 'W' else 'W'
    
    # Local variable caching for tight loop performance
    append_move = legal_moves.append

    for start_idx in range(64):
        p = grid[start_idx]
        if not p or p[0] != color:
            continue
            
        ptype = p[1]
        start_rank = start_idx // 8
        start_file = start_idx % 8
        
        if ptype == 'R':
            for delta in DIR_OFFSETS['R']:
                curr_idx = start_idx
                curr_rank, curr_file = start_rank, start_file
                
                while True:
                    next_rank = curr_rank + (delta // 8)
                    next_file = curr_file + (delta % 8 if delta in (-1, 1) else 0)
                    
                    if not (0 <= next_rank <= 7 and 0 <= next_file <= 7):
                        break
                        
                    curr_idx += delta
                    curr_rank, curr_file = next_rank, next_file
                    
                    target_p = grid[curr_idx]
                    if target_p and target_p[0] == color:
                        break # Blocked by friendly piece
                        
                    # --- MAKE MOVE (In-Place) ---
                    grid[start_idx] = None
                    grid[curr_idx] = p
                    
                    # Strictly validate King safety
                    if not is_square_attacked(grid, board.king_idx[color], opp_color):
                        is_cap = "x" if target_p else ""
                        append_move(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                        
                    # --- UNMAKE MOVE ---
                    grid[start_idx] = p
                    grid[curr_idx] = target_p
                    
                    if target_p:
                        break # Stop sliding after capture
                        
        elif ptype == 'K':
            for delta in DIR_OFFSETS['K']:
                next_rank = start_rank + (delta // 8)
                next_file = start_file + (delta % 8 if delta % 8 < 4 else (delta % 8) - 8)
                
                if 0 <= next_rank <= 7 and 0 <= next_file <= 7:
                    target_idx = start_idx + delta
                    target_p = grid[target_idx]
                    
                    if not target_p or target_p[0] != color:
                        # --- MAKE MOVE (In-Place) ---
                        grid[start_idx] = None
                        grid[target_idx] = p
                        board.king_idx[color] = target_idx
                        
                        # Validate new King position
                        if not is_square_attacked(grid, target_idx, opp_color):
                            is_cap = "x" if target_p else ""
                            append_move(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                            
                        # --- UNMAKE MOVE ---
                        grid[start_idx] = p
                        grid[target_idx] = target_p
                        board.king_idx[color] = start_idx

    return sorted(list(set(legal_moves)))