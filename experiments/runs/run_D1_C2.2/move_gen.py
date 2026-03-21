from board import FILES, RANKS

def generate_pseudo_legal_moves(board, color):
    moves = []
    for f in FILES:
        for r in RANKS:
            p = board.get_piece(f, r)
            if p and p[0] == color:
                ptype = p[1]
                if ptype == 'R':
                    for df, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        cf, cr = FILES.index(f), RANKS.index(r)
                        while True:
                            cf += df
                            cr += dr
                            if 0 <= cf < 8 and 0 <= cr < 8:
                                nf, nr = FILES[cf], RANKS[cr]
                                target = board.get_piece(nf, nr)
                                if target:
                                    if target[0] != color:
                                        moves.append((f, r, nf, nr, target))
                                    break
                                else:
                                    moves.append((f, r, nf, nr, None))
                            else:
                                break
                elif ptype == 'K':
                    for df in [-1, 0, 1]:
                        for dr in [-1, 0, 1]:
                            if df == 0 and dr == 0: continue
                            cf, cr = FILES.index(f) + df, RANKS.index(r) + dr
                            if 0 <= cf < 8 and 0 <= cr < 8:
                                nf, nr = FILES[cf], RANKS[cr]
                                target = board.get_piece(nf, nr)
                                if not target or target[0] != color:
                                    moves.append((f, r, nf, nr, target))
    return moves

def is_in_check(board, color):
    kings = board.find_pieces(color, 'K')
    if not kings: 
        return False
    kf, kr = kings[0]
    opp_color = 'B' if color == 'W' else 'W'
    opp_moves = generate_pseudo_legal_moves(board, opp_color)
    
    for m in opp_moves:
        if m[2] == kf and m[3] == kr:
            return True
    return False

def get_legal_moves(board, color):
    pseudo = generate_pseudo_legal_moves(board, color)
    legal = []
    for m in pseudo:
        sf, sr, ef, er, target = m
        if target and target[1] == 'K':
            continue 
            
        b_copy = board.copy()
        b_copy.move_piece((sf, sr), (ef, er))
        
        # If the move doesn't leave the acting color's king in check, it is legal
        if not is_in_check(b_copy, color):
            ptype = board.get_piece(sf, sr)[1]
            is_cap = "x" if target else ""
            legal.append(f"{ptype}{is_cap}{ef}{er}")
            
    return sorted(list(set(legal)))