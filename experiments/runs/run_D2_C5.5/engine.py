from constants import VECTORS, KNIGHT_OFFSETS, SQR_MAP, REV_SQR_MAP

class ChessEngine:
    @staticmethod
    def apply_move(board, san, color):
        san = san.replace('+', '').replace('#', '')
        promo = san.split('=')[1] if '=' in san else None
        clean_san = san.split('=')[0]
        
        dest_idx = SQR_MAP[clean_san[-2:]]
        p_type = clean_san[0] if clean_san[0].isupper() else 'P'
        
        source_idx = None
        target_p = f"{color}{p_type}"
        
        # Fast scan for source piece
        for i, p in enumerate(board.pieces):
            if p == target_p:
                if p_type == 'P':
                    # Check file for disambiguation or forward move
                    src_file = i % 8
                    dst_file = dest_idx % 8
                    if 'x' in clean_san:
                        if src_file == "abcdefgh".index(clean_san[0]):
                            source_idx = i; break
                    elif src_file == dst_file:
                        source_idx = i; break
                else:
                    source_idx = i; break

        if source_idx is not None:
            new_p = f"{color}{promo}" if promo else board.pieces[source_idx]
            board.move_piece(source_idx, dest_idx, new_p)
        else:
            # Fallback for legacy state consistency
            board.pieces[dest_idx] = f"{color}{p_type}"

    @staticmethod
    def is_square_attacked(board, idx, opp_color):
        r, f = divmod(idx, 8)
        
        # 1. Knight attacks
        for off in KNIGHT_OFFSETS:
            ni = idx + off
            if 0 <= ni < 64:
                # Prevent "wrapping" around the board edges
                if abs((ni % 8) - f) <= 2 and board.pieces[ni] == f"{opp_color}N":
                    return True
        
        # 2. Sliding pieces & King
        for off in VECTORS:
            for dist in range(1, 8):
                ni = idx + off * dist
                if not (0 <= ni < 64) or abs((ni % 8) - ((ni - off) % 8)) > 1:
                    break
                p = board.pieces[ni]
                if p:
                    if p.startswith(opp_color):
                        pt = p[1]
                        if pt == 'Q' or (dist == 1 and pt == 'K'): return True
                        if off in [8, -8, 1, -1] and pt == 'R': return True
                        if off not in [8, -8, 1, -1] and pt == 'B': return True
                    break # Square occupied, block further vision
        return False

    @staticmethod
    def get_king_analysis(board, color):
        opp = "W" if color == "B" else "B"
        k_idx = board.pieces.index(f"{color}K")
        kr, kf = divmod(k_idx, 8)
        
        all_m, leg_m, ill_m = [], [], []
        for off in VECTORS:
            ni = k_idx + off
            if 0 <= ni < 64 and abs((ni % 8) - kf) <= 1:
                m_str = f"K{REV_SQR_MAP[ni]}"
                all_m.append(m_str)
                occ = board.pieces[ni]
                if (occ and occ.startswith(color)) or \
                   ChessEngine.is_square_attacked(board, ni, opp):
                    ill_m.append(m_str)
                else:
                    leg_m.append(m_str)
        
        return sorted(all_m), sorted(leg_m), sorted(ill_m), f"K{REV_SQR_MAP[k_idx]}"