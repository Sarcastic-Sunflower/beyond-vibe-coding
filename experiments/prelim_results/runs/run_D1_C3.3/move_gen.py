from board import IDX_TO_SQ, WHITE, BLACK, ROOK, KING, COLOR_MASK, PIECE_MASK

# 1D array directional offsets: N, S, E, W, NE, NW, SE, SW
DIR_OFFSETS = (8, -8, 1, -1, 9, 7, -7, -9)

# Precalculate distance to edge for all 64 squares across all 8 directions
NUM_SQUARES_TO_EDGE = [[0] * 8 for _ in range(64)]
for sq in range(64):
    r, f = sq // 8, sq % 8
    NUM_SQUARES_TO_EDGE[sq][0] = 7 - r             # N
    NUM_SQUARES_TO_EDGE[sq][1] = r                 # S
    NUM_SQUARES_TO_EDGE[sq][2] = 7 - f             # E
    NUM_SQUARES_TO_EDGE[sq][3] = f                 # W
    NUM_SQUARES_TO_EDGE[sq][4] = min(7 - r, 7 - f) # NE
    NUM_SQUARES_TO_EDGE[sq][5] = min(7 - r, f)     # NW
    NUM_SQUARES_TO_EDGE[sq][6] = min(r, 7 - f)     # SE
    NUM_SQUARES_TO_EDGE[sq][7] = min(r, f)         # SW

def is_square_attacked(grid, sq_idx, attacker_color):
    """O(1) boundary limits via precomputed edge distances."""
    
    # 1. Straight Rays (Rooks) - Directions 0 to 3
    target_rook = attacker_color | ROOK
    for dir_idx in range(4):
        offset = DIR_OFFSETS[dir_idx]
        curr_idx = sq_idx
        for _ in range(NUM_SQUARES_TO_EDGE[sq_idx][dir_idx]):
            curr_idx += offset
            p = grid[curr_idx]
            if p:
                if p == target_rook:
                    return True
                break # Blocked by any other piece

    # 2. Adjacency (Kings) - Directions 0 to 7 (1 step max)
    target_king = attacker_color | KING
    for dir_idx in range(8):
        if NUM_SQUARES_TO_EDGE[sq_idx][dir_idx] > 0:
            if grid[sq_idx + DIR_OFFSETS[dir_idx]] == target_king:
                return True

    return False

def get_legal_moves(board, color):
    legal_moves = []
    grid = board.grid
    opp_color = BLACK if color == WHITE else WHITE
    king_pos = board.king_idx[color]
    
    # Cache locally to bypass global namespace lookups in the loop
    append_move = legal_moves.append
    
    for start_idx in range(64):
        p = grid[start_idx]
        if not p or (p & COLOR_MASK) != color:
            continue
            
        ptype = p & PIECE_MASK
        
        if ptype == ROOK:
            for dir_idx in range(4):
                offset = DIR_OFFSETS[dir_idx]
                curr_idx = start_idx
                
                for _ in range(NUM_SQUARES_TO_EDGE[start_idx][dir_idx]):
                    curr_idx += offset
                    target_p = grid[curr_idx]
                    
                    if target_p:
                        if (target_p & COLOR_MASK) == color:
                            break # Blocked by friendly
                            
                    # Make move in-place
                    grid[start_idx] = 0
                    grid[curr_idx] = p
                    
                    if not is_square_attacked(grid, king_pos, opp_color):
                        is_cap = "x" if target_p else ""
                        append_move(f"R{is_cap}{IDX_TO_SQ[curr_idx]}")
                        
                    # Revert move
                    grid[start_idx] = p
                    grid[curr_idx] = target_p
                    
                    if target_p:
                        break # Stop sliding post-capture
                        
        elif ptype == KING:
            for dir_idx in range(8):
                if NUM_SQUARES_TO_EDGE[start_idx][dir_idx] > 0:
                    target_idx = start_idx + DIR_OFFSETS[dir_idx]
                    target_p = grid[target_idx]
                    
                    if not target_p or (target_p & COLOR_MASK) != color:
                        grid[start_idx] = 0
                        grid[target_idx] = p
                        
                        if not is_square_attacked(grid, target_idx, opp_color):
                            is_cap = "x" if target_p else ""
                            append_move(f"K{is_cap}{IDX_TO_SQ[target_idx]}")
                            
                        grid[start_idx] = p
                        grid[target_idx] = target_p

    return sorted(list(set(legal_moves)))