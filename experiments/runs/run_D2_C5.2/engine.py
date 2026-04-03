from constants import FILES, RANKS

class ChessEngine:
    @staticmethod
    def apply_move(board, san, color):
        san = san.replace('+', '').replace('#', '')
        promo = san.split('=')[1] if '=' in san else None
        clean_san = san.split('=')[0]
        
        dest_sq = clean_san[-2:]
        df, dr = FILES.index(dest_sq[0]), RANKS.index(dest_sq[1])
        p_type = clean_san[0] if clean_san[0].isupper() else 'P'
        
        source = None
        for (r, f), p in board.pieces.items():
            if p == f"{color}{p_type}":
                if p_type == 'P':
                    # Handle captures like 'dxc8'
                    if 'x' in clean_san and FILES[f] == clean_san[0]: source = (r, f)
                    elif 'x' not in clean_san and f == df: source = (r, f)
                else: source = (r, f)
                if source: break

        if source:
            # If d7 captures on c8 and promotes, the piece becomes WQ
            new_p = f"{color}{promo}" if promo else board.pieces[source]
            board.move_piece(source, (dr, df), new_p)

    @staticmethod
    def is_square_attacked(board, r, f, opp_color):
        # Check Knight jumps
        for dr, df in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            nr, nf = r + dr, f + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                if board.get_piece(nr, nf) == f"{opp_color}N": return True
        
        # Check sliding pieces (The WQ on c8 will control rank 8 and the c-file)
        vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, df in vectors:
            for dist in range(1, 8):
                nr, nf = r + dr * dist, f + df * dist
                if not (0 <= nr < 8 and 0 <= nf < 8): break
                p = board.get_piece(nr, nf)
                if p:
                    if p.startswith(opp_color):
                        pt = p[1]
                        if pt == 'Q' or (dist == 1 and pt == 'K'): return True
                        if (dr == 0 or df == 0) and pt == 'R': return True
                        if (dr != 0 and df != 0) and pt == 'B': return True
                    break
        return False

    @staticmethod
    def get_king_analysis(board, color):
        opp = "W" if color == "B" else "B"
        kr, kf = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        
        all_m, leg_m, ill_m = [], [], []
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0: continue
                nr, nf = kr + dr, kf + df
                if 0 <= nr < 8 and 0 <= nf < 8:
                    m_str = f"K{FILES[nf]}{RANKS[nr]}"
                    all_m.append(m_str)
                    occ = board.get_piece(nr, nf)
                    # Illegal if occupied by own piece OR square is under attack
                    if (occ and occ.startswith(color)) or \
                       ChessEngine.is_square_attacked(board, nr, nf, opp):
                        ill_m.append(m_str)
                    else:
                        leg_m.append(m_str)
        return sorted(all_m), sorted(leg_m), sorted(ill_m), f"K{FILES[kf]}{RANKS[kr]}"