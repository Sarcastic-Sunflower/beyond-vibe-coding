import re

class ChessEngine:
    @staticmethod
    def apply_san_move(board, san, color):
        match = re.search(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?', san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2) # e.g., 'd' in dxc8
        dest_str = match.group(4)
        target_pos = (board.FILES.index(dest_str[0]), board.RANKS.index(dest_str[1]))
        promo = match.group(5)[1] if match.group(5) else p_type

        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                # For Pawns, verify it's the correct file
                if p_type == "P":
                    if spec_f and board.FILES[pos[0]] != spec_f: continue
                    if not spec_f and board.FILES[pos[0]] != dest_str[0]: continue
                source_pos = pos
                break
        
        if source_pos:
            if target_pos in board.pieces: del board.pieces[target_pos]
            del board.pieces[source_pos]
            board.pieces[target_pos] = f"{color}{promo}"

    @staticmethod
    def get_king_moves(board, color):
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        all_moves, legal_moves, illegal_moves = [], [], []
        
        # Directions: King can move 1 square in any direction
        for dc in [-1, 0, 1]:
            for dr in [-1, 0, 1]:
                if dc == 0 and dr == 0: continue
                target = (k_pos[0] + dc, k_pos[1] + dr)
                
                if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                    m_str = f"K{board.FILES[target[0]]}{board.RANKS[target[1]]}"
                    all_moves.append(m_str)
                    
                    # Square is illegal if occupied by friendly or attacked by enemy
                    if board.is_occupied_by_color(target, color) or \
                       ChessEngine.is_square_attacked(board, target, color):
                        illegal_moves.append(m_str)
                    else:
                        legal_moves.append(m_str)

        return sorted(all_moves), sorted(legal_moves), sorted(illegal_moves)

    @staticmethod
    def is_square_attacked(board, pos, victim_color):
        attacker_color = "W" if victim_color == "B" else "B"
        for p_pos, piece in board.pieces.items():
            if not piece.startswith(attacker_color): continue
            
            p_type = piece[1]
            dc, dr = pos[0] - p_pos[0], pos[1] - p_pos[1]
            
            if p_type == "P":
                # White pawns attack (x+1, y+1) and (x-1, y+1)
                if attacker_color == "W" and dr == 1 and abs(dc) == 1: return True
            elif p_type == "Q":
                if dc == 0 or dr == 0 or abs(dc) == abs(dr):
                    # Check for pieces blocking the Queen's path
                    step_c = (dc > 0) - (dc < 0)
                    step_r = (dr > 0) - (dr < 0)
                    curr_c, curr_r = p_pos[0] + step_c, p_pos[1] + step_r
                    blocked = False
                    while (curr_c, curr_r) != pos:
                        if (curr_c, curr_r) in board.pieces:
                            blocked = True
                            break
                        curr_c += step_c
                        curr_r += step_r
                    if not blocked: return True
        return False