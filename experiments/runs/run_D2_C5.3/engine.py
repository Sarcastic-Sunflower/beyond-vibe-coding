from constants import FILES, RANKS

class ChessEngine:
    @staticmethod
    def apply_move(board, san, color):
        # 1. Clean SAN notation
        san = san.replace('+', '').replace('#', '')
        promo = san.split('=')[1] if '=' in san else None
        clean_san = san.split('=')[0]
        
        # 2. Identify destination
        dest_sq = clean_san[-2:]
        df, dr = FILES.index(dest_sq[0]), RANKS.index(dest_sq[1])
        
        # 3. Identify piece type and source file for pawn captures
        p_type = clean_san[0] if clean_san[0].isupper() else 'P'
        source_file = FILES.index(clean_san[0]) if 'x' in clean_san and p_type == 'P' else None

        source = None
        for (r, f), p in board.pieces.items():
            if p == f"{color}{p_type}":
                if p_type == 'P':
                    # If it's a capture, file must match source_file. 
                    # If it's a push, file must match destination file.
                    if source_file is not None:
                        if f == source_file: source = (r, f)
                    elif f == df:
                        source = (r, f)
                else:
                    # For Kings/Knights in this specific history, 
                    # there is only one of each color.
                    source = (r, f)
                if source: break

        if source:
            # Handle the move: Remove piece at source, 
            # place (potentially promoted) piece at destination.
            # This implicitly handles captures by overwriting board.pieces[(dr, df)]
            new_p = f"{color}{promo}" if promo else board.pieces[source]
            board.move_piece(source, (dr, df), new_p)

    @staticmethod
    def is_square_attacked(board, r, f, opp_color):
        # Knight attacks
        for dr, df in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            nr, nf = r + dr, f + df
            if (nr, nf) in board.pieces and board.pieces[(nr, nf)] == f"{opp_color}N":
                return True
        
        # Sliding/King attacks (Q, R, B, K)
        vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for v_r, v_f in vectors:
            for dist in range(1, 8):
                nr, nf = r + v_r * dist, f + v_f * dist
                if not (0 <= nr < 8 and 0 <= nf < 8): break
                p = board.get_piece(nr, nf)
                if p:
                    if p.startswith(opp_color):
                        pt = p[1]
                        if pt == 'Q' or (dist == 1 and pt == 'K'): return True
                        if (v_r == 0 or v_f == 0) and pt == 'R': return True
                        if (v_r != 0 and v_f != 0) and pt == 'B': return True
                    break # Blocked by any piece
        return False

    @staticmethod
    def get_king_analysis(board, color):
        opp = "W" if color == "B" else "B"
        kr, kf = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        
        all_m, leg_m, ill_m = [], [], []
        # King moves in 8 directions
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0: continue
                nr, nf = kr + dr, kf + df
                if 0 <= nr < 8 and 0 <= nf < 8:
                    m_str = f"K{FILES[nf]}{RANKS[nr]}"
                    all_m.append(m_str)
                    occ = board.get_piece(nr, nf)
                    # Check if square is occupied by own piece or attacked by opponent
                    if (occ and occ.startswith(color)) or \
                       ChessEngine.is_square_attacked(board, nr, nf, opp):
                        ill_m.append(m_str)
                    else:
                        leg_m.append(m_str)
        return sorted(all_m), sorted(leg_m), sorted(ill_m), f"K{FILES[kf]}{RANKS[kr]}"