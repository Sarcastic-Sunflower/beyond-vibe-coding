from constants import KING_OFFSETS, KNIGHT_OFFSETS, FILES, RANKS

class ChessEngine:
    @staticmethod
    def apply_san_move(board, san, color):
        # Fast parsing without heavy Regex
        san = san.rstrip('+#')
        promo = None
        if '=' in san:
            san, promo = san.split('=')
        
        dest_sq = san[-2:]
        target_idx = RANKS.index(dest_sq[1]) * 8 + FILES.index(dest_sq[0])
        p_type = san[0] if san[0].isupper() else 'P'
        
        # Find source
        source_idx = -1
        for i, p in enumerate(board.state):
            if p == f"{color}{p_type}":
                # Basic disambiguation for pawn captures
                if p_type == 'P' and 'x' in san:
                    if FILES[i % 8] == san[0]:
                        source_idx = i
                        break
                elif p_type == 'P':
                    if i % 8 == target_idx % 8:
                        source_idx = i
                        break
                else:
                    source_idx = i
                    break

        if source_idx != -1:
            board.state[target_idx] = f"{color}{promo}" if promo else board.state[source_idx]
            board.state[source_idx] = None

    @staticmethod
    def is_attacked(board, idx, opp_color):
        r, f = divmod(idx, 8)
        
        # Knight attacks
        for o in KNIGHT_OFFSETS:
            target = idx + o
            if 0 <= target < 64:
                tr, tf = divmod(target, 8)
                if abs(r - tr) <= 2 and abs(f - tf) <= 2:
                    if board.state[target] == f"{opp_color}N": return True

        # Sliding/King attacks
        vectors = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, df in vectors:
            for dist in range(1, 8):
                nr, nf = r + dr * dist, f + df * dist
                if not (0 <= nr < 8 and 0 <= nf < 8): break
                piece = board.state[nr * 8 + nf]
                if piece:
                    if piece[0] == opp_color:
                        pt = piece[1]
                        if pt == 'Q' or (dist == 1 and pt == 'K'): return True
                        if dr == 0 or df == 0:
                            if pt == 'R': return True
                        else:
                            if pt == 'B': return True
                    break
        return False

    @staticmethod
    def get_king_moves(board, color):
        opp_color = "W" if color == "B" else "B"
        k_idx = board.state.index(f"{color}K")
        kr, kf = divmod(k_idx, 8)
        
        all_m, leg_m, ill_m = [], [], []

        for dr, df in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            nr, nf = kr + dr, kf + df
            if 0 <= nr < 8 and 0 <= nf < 8:
                target_idx = nr * 8 + nf
                m_str = f"K{FILES[nf]}{RANKS[nr]}"
                all_m.append(m_str)
                
                occupant = board.state[target_idx]
                if (occupant and occupant[0] == color) or ChessEngine.is_attacked(board, target_idx, opp_color):
                    ill_m.append(m_str)
                else:
                    leg_m.append(m_str)
                    
        return sorted(all_m), sorted(leg_m), sorted(ill_m)