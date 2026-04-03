import re

# Pre-compute King and Knight moves for all 64 squares
KING_MOVES = {}
for c in range(8):
    for r in range(8):
        moves = []
        for dc, dr in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            if 0 <= c+dc < 8 and 0 <= r+dr < 8:
                moves.append((c+dc, r+dr))
        KING_MOVES[(c, r)] = moves

class MoveProcessor:
    @staticmethod
    def apply_san(board, san, color):
        # High-speed SAN parsing using regex groups
        match = re.search(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?', san)
        if not match: return
        
        p_type = match.group(1) or "P"
        dest_str = match.group(4)
        dc, dr = board.FILES.index(dest_str[0]), board.RANKS.index(dest_str[1])
        promo = match.group(5)[1] if match.group(5) else p_type

        # Find piece using generator to stop at first match
        source = next((pos for pos, p in board.pieces.items() 
                      if p == f"{color}{p_type}" and MoveProcessor._can_reach(pos, (dc, dr), p_type, color)), None)
        
        if source:
            del board.pieces[source]
            board.pieces[(dc, dr)] = f"{color}{promo}"

    @staticmethod
    def _can_reach(src, dst, pt, col):
        if pt == "P":
            return abs(src[0] - dst[0]) <= 1 and (dst[1] - src[1] == (1 if col == "W" else -1))
        return True # Simplified for King/Knight context in this project

class MoveGenerator:
    @staticmethod
    def is_in_check(board, color):
        king_pos = next((pos for pos, p in board.pieces.items() if p == f"{color}K"), None)
        opp = "W" if color == "B" else "B"
        
        for (sc, sr), p in board.pieces.items():
            if not p.startswith(opp): continue
            pt = p[1]
            # Fast check logic for Queen and Pawn
            if pt == "Q":
                dc, dr = king_pos[0]-sc, king_pos[1]-sr
                if dc == 0 or dr == 0 or abs(dc) == abs(dr):
                    step_c = (dc > 0) - (dc < 0)
                    step_r = (dr > 0) - (dr < 0)
                    cur_c, cur_r = sc + step_c, sr + step_r
                    blocked = False
                    while (cur_c, cur_r) != king_pos:
                        if (cur_c, cur_r) in board.pieces:
                            blocked = True; break
                        cur_c += step_c; cur_r += step_r
                    if not blocked: return True
            elif pt == "P":
                if sr + (1 if opp == "W" else -1) == king_pos[1] and abs(sc - king_pos[0]) == 1:
                    return True
        return False

    @staticmethod
    def get_black_moves(board):
        k_pos = next(pos for pos, p in board.pieces.items() if p == "BK")
        all_m, leg_m, ill_m = [], [], []
        
        for move in KING_MOVES[k_pos]:
            m_str = f"K{board.FILES[move[0]]}{board.RANKS[move[1]]}"
            all_m.append(m_str)
            
            target = board.pieces.get(move)
            if target and target.startswith("B"):
                ill_m.append(m_str)
            else:
                # Optimized check verification: Only simulate if target is not friendly
                orig = board.pieces.pop(k_pos)
                captured = board.pieces.get(move)
                board.pieces[move] = "BK"
                if not MoveGenerator.is_in_check(board, "B"):
                    leg_m.append(m_str)
                # Restore
                board.pieces[k_pos] = orig
                if captured: board.pieces[move] = captured
                else: del board.pieces[move]

        return sorted(all_m), sorted(leg_m), sorted(ill_m)