import re

# Pre-compute static King offsets to avoid O(N^2) loops during runtime
KING_OFFSETS = [(dc, dr) for dc in [-1, 0, 1] for dr in [-1, 0, 1] if not (dc == 0 and dr == 0)]

class ChessEngine:
    # Compile regex once at the module level for speed
    SAN_PATTERN = re.compile(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?')

    @staticmethod
    def apply_san_move(board, san, color):
        match = ChessEngine.SAN_PATTERN.search(san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2)
        dest_str = match.group(4)
        target_pos = (board.FILES_INDEX[dest_str[0]], board.RANKS_INDEX[dest_str[1]])
        promo = f"{color}{match.group(5)[1]}" if match.group(5) else f"{color}{p_type}"

        # High-speed source lookup
        for pos, piece in board.pieces.items():
            if piece[1] == p_type and piece[0] == color:
                if p_type == "P":
                    if spec_f and board.FILES[pos[0]] != spec_f: continue
                    if not spec_f and board.FILES[pos[0]] != dest_str[0]: continue
                
                # Update board state
                board.pieces.pop(pos)
                board.pieces[target_pos] = promo
                return

    @staticmethod
    def get_king_moves(board, color):
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        all_m, leg_m, ill_m = [], [], []
        
        kc, kr = k_pos
        for dc, dr in KING_OFFSETS:
            tc, tr = kc + dc, kr + dr
            if 0 <= tc < 8 and 0 <= tr < 8:
                target = (tc, tr)
                m_str = f"K{board.FILES[tc]}{board.RANKS[tr]}"
                all_m.append(m_str)
                
                # Bitwise-style logic: Fail fast on friendly occupancy or enemy attack
                if board.is_occupied_by_color(target, color) or \
                   ChessEngine.is_square_attacked(board, target, color):
                    ill_m.append(m_str)
                else:
                    leg_m.append(m_str)

        return sorted(all_m), sorted(leg_m), sorted(ill_m)

    @staticmethod
    def is_square_attacked(board, pos, victim_color):
        opp = "W" if victim_color == "B" else "B"
        for p_pos, piece in board.pieces.items():
            if piece[0] != opp: continue
            
            p_type = piece[1]
            dc, dr = pos[0] - p_pos[0], pos[1] - p_pos[1]
            
            if p_type == "P":
                if opp == "W" and dr == 1 and abs(dc) == 1: return True
                if opp == "B" and dr == -1 and abs(dc) == 1: return True
            elif p_type == "Q":
                if dc == 0 or dr == 0 or abs(dc) == abs(dr):
                    sc, sr = (dc > 0) - (dc < 0), (dr > 0) - (dr < 0)
                    cc, cr = p_pos[0] + sc, p_pos[1] + sr
                    blocked = False
                    while (cc, cr) != pos:
                        if (cc, cr) in board.pieces:
                            blocked = True; break
                        cc += sc; cr += sr
                    if not blocked: return True
        return False