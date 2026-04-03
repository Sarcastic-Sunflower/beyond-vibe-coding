import re

class MoveProcessor:
    @staticmethod
    def apply_san(board, san, color):
        clean_san = san.replace("+", "").replace("#", "").replace("x", "")
        promotion = None
        if "=" in clean_san:
            clean_san, promotion = clean_san.split("=")

        p_type = "P" if not clean_san[0].isupper() else clean_san[0]
        dest_sq = clean_san[-2:]
        dc = board.FILES.index(dest_sq[0])
        dr = board.RANKS.index(dest_sq[1])

        moving_piece_key = None
        for (sc, sr), p_info in board.pieces.items():
            if p_info == f"{color}{p_type}":
                if p_type == "P":
                    # Check for diagonal capture vs vertical push
                    if abs(sc - dc) <= 1 and (dr - sr == (1 if color == "W" else -1)):
                        moving_piece_key = (sc, sr)
                        break
                else:
                    # For King/Knight, any piece of that type is a candidate
                    moving_piece_key = (sc, sr)
                    break

        if moving_piece_key:
            del board.pieces[moving_piece_key]
            board.pieces[(dc, dr)] = f"{color}{promotion if promotion else p_type}"

class MoveGenerator:
    @staticmethod
    def is_in_check(board, color):
        king_pos = next((pos for pos, p in board.pieces.items() if p == f"{color}K"), None)
        if not king_pos: return False
        
        enemy_color = "W" if color == "B" else "B"
        for (sc, sr), p in board.pieces.items():
            if not p.startswith(enemy_color): continue
            pt = p[1]
            # Queen/Rook check (horizontal/vertical)
            if pt in ("Q", "R"):
                for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
                    for i in range(1, 8):
                        nc, nr = sc + dc*i, sr + dr*i
                        if (nc, nr) == king_pos: return True
                        if not board.is_on_board(nc, nr) or board.get_piece(nc, nr): break
            # Queen/Bishop check (diagonal)
            if pt in ("Q", "B"):
                for dc, dr in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                    for i in range(1, 8):
                        nc, nr = sc + dc*i, sr + dr*i
                        if (nc, nr) == king_pos: return True
                        if not board.is_on_board(nc, nr) or board.get_piece(nc, nr): break
            # Pawn check
            if pt == "P":
                direction = 1 if enemy_color == "W" else -1
                if sr + direction == king_pos[1] and abs(sc - king_pos[0]) == 1:
                    return True
        return False

    @staticmethod
    def get_black_moves(board):
        all_m, leg_m, ill_m = set(), set(), set()
        k_pos = next((pos for pos, p in board.pieces.items() if p == "BK"), None)
        if not k_pos: return [], [], []

        for dc, dr in [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]:
            nc, nr = k_pos[0] + dc, k_pos[1] + dr
            if board.is_on_board(nc, nr):
                m_str = f"K{board.FILES[nc]}{board.RANKS[nr]}"
                all_m.add(m_str)
                target = board.get_piece(nc, nr)
                if target and target.startswith("B"):
                    ill_m.add(m_str)
                else:
                    # Simulation
                    memo = board.pieces.copy()
                    del board.pieces[k_pos]
                    board.pieces[(nc, nr)] = "BK"
                    if not MoveGenerator.is_in_check(board, "B"):
                        leg_m.add(m_str)
                    board.pieces = memo
                    
        return sorted(list(all_m)), sorted(list(leg_m)), sorted(list(ill_m))