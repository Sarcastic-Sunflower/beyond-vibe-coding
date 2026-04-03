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

        # Find the specific piece that can move to the destination
        for (sc, sr), p_info in list(board.pieces.items()):
            if p_info == f"{color}{p_type}":
                # For pawns, ensure correct column for captures vs pushes
                if p_type == "P":
                    if abs(sc - dc) <= 1:
                        del board.pieces[(sc, sr)]
                        board.pieces[(dc, dr)] = f"{color}{promotion if promotion else 'P'}"
                        return
                # For King/Knight, direct jump logic
                else:
                    del board.pieces[(sc, sr)]
                    board.pieces[(dc, dr)] = f"{color}{p_type}"
                    return

class MoveGenerator:
    @staticmethod
    def is_in_check(board, color):
        king_pos = next((pos for pos, p in board.pieces.items() if p == f"{color}K"), None)
        if not king_pos: return False
        
        enemy_color = "W" if color == "B" else "B"
        # Check if any enemy piece can attack the King
        for (sc, sr), p in board.pieces.items():
            if not p.startswith(enemy_color): continue
            
            p_type = p[1]
            if p_type == "Q": # Queen moves (straight and diagonal)
                for dc, dr in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                    for i in range(1, 8):
                        nc, nr = sc + dc*i, sr + dr*i
                        if not board.is_on_board(nc, nr): break
                        if (nc, nr) == king_pos: return True
                        if board.get_piece(nc, nr): break
            # Simplified for current scope: Q and P check
            if p_type == "P":
                direction = -1 if enemy_color == "W" else 1
                if sr + direction == king_pos[1] and abs(sc - king_pos[0]) == 1:
                    return True
        return False

    @staticmethod
    def get_black_moves(board):
        all_m = set()
        leg_m = set()
        ill_m = set()
        
        # 1. Identify Black's King
        k_pos = next((pos for pos, p in board.pieces.items() if p == "BK"), None)
        if not k_pos: return [], [], []

        # King movement vectors
        offsets = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

        for dc, dr in offsets:
            nc, nr = k_pos[0] + dc, k_pos[1] + dr
            if board.is_on_board(nc, nr):
                m_str = f"K{board.FILES[nc]}{board.RANKS[nr]}"
                all_m.add(m_str)
                
                target = board.get_piece(nc, nr)
                # Illegal: Friendly fire
                if target and target.startswith("B"):
                    ill_m.add(m_str)
                    continue
                
                # Simulate move to check legality (escaping check)
                orig_pieces = board.pieces.copy()
                del board.pieces[k_pos]
                board.pieces[(nc, nr)] = "BK"
                
                if not MoveGenerator.is_in_check(board, "B"):
                    leg_m.add(m_str)
                
                board.pieces = orig_pieces # Restore board

        return sorted(list(all_m)), sorted(list(leg_m)), sorted(list(ill_m))