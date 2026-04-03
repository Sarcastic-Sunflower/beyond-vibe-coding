import re

class ChessEngine:
    @staticmethod
    def apply_san_move(board, san, color):
        match = re.search(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?', san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2)
        dest_str = match.group(4)
        target_pos = (board.FILES.index(dest_str[0]), board.RANKS.index(dest_str[1]))
        promo = match.group(5)[1] if match.group(5) else p_type

        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                # If SAN specifies a file (like 'd' in dxc8), match it
                if spec_f and board.FILES[pos[0]] != spec_f:
                    continue
                source_pos = pos
                break
        
        if source_pos:
            # Handle Capture: Remove whatever was at the target
            if target_pos in board.pieces:
                del board.pieces[target_pos]
            del board.pieces[source_pos]
            board.pieces[target_pos] = f"{color}{promo}"

    @staticmethod
    def get_king_moves(board, color):
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        all_moves, legal_moves, illegal_moves = [], [], []
        
        directions = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
        
        for dc, dr in directions:
            target = (k_pos[0] + dc, k_pos[1] + dr)
            if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                m_str = f"K{board.FILES[target[0]]}{board.RANKS[target[1]]}"
                all_moves.append(m_str)
                
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
            
            # White Pawn attacks diagonally up
            if p_type == "P" and attacker_color == "W":
                if dr == 1 and abs(dc) == 1: return True
            # Queen line-of-sight check for the new c8 Queen
            if p_type == "Q":
                if dc == 0 or dr == 0 or abs(dc) == abs(dr):
                    # Simplified LOS: check if anything is between p_pos and pos
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