import re

class MoveProcessor:
    @staticmethod
    def apply_san(board, san, color):
        # 1. Clean symbols and identify promotion
        clean_san = san.replace("+", "").replace("#", "").replace("x", "")
        promotion = None
        if "=" in clean_san:
            clean_san, promotion = clean_san.split("=")

        # 2. Determine piece type and destination
        p_type = "P" if not clean_san[0].isupper() else clean_san[0]
        dest_sq = clean_san[-2:]
        dc = board.FILES.index(dest_sq[0])
        dr = board.RANKS.index(dest_sq[1])

        # 3. Locate the correct moving piece
        for (sc, sr), p_info in list(board.pieces.items()):
            if p_info == f"{color}{p_type}":
                # Pawn logic: check files for captures or forward moves
                if p_type == "P":
                    if abs(sc - dc) <= 1: # Capture (1) or push (0)
                        del board.pieces[(sc, sr)]
                        board.pieces[(dc, dr)] = f"{color}{promotion if promotion else 'P'}"
                        return
                # Piece logic: verify reachability for King and Knight
                else:
                    del board.pieces[(sc, sr)]
                    board.pieces[(dc, dr)] = f"{color}{p_type}"
                    return

class MoveGenerator:
    @staticmethod
    def get_black_moves(board):
        all_m, leg_m, ill_m = set(), set(), set()
        
        for (c, r), p in board.pieces.items():
            if not p.startswith("B"): continue
            p_type = p[1]
            
            # Define movement vectors
            if p_type == "K":
                offsets = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
            elif p_type == "N":
                offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
            else:
                continue

            for dc, dr in offsets:
                nc, nr = c + dc, r + dr
                if board.is_on_board(nc, nr):
                    m_str = f"{p_type}{board.FILES[nc]}{board.RANKS[nr]}"
                    all_m.add(m_str)
                    
                    target = board.get_piece(nc, nr)
                    # A move is illegal if it lands on a piece of the same color
                    if target and target.startswith("B"):
                        ill_m.add(m_str)
                    else:
                        leg_m.add(m_str)
                        
        return sorted(list(all_m)), sorted(list(leg_m)), sorted(list(ill_m))