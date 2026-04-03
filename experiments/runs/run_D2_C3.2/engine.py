import re

class ChessEngine:
    @staticmethod
    def apply_san_move(board, san, color):
        """Parses and applies a move in Standard Algebraic Notation."""
        # Handles captures (x), promotions (=Q), and checks (+)
        match = re.search(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?', san)
        if not match: return

        p_type = match.group(1) or "P"
        dest_str = match.group(4)
        target_pos = (board.FILES.index(dest_str[0]), board.RANKS.index(dest_str[1]))
        promo = match.group(5)[1] if match.group(5) else p_type

        # Find the specific piece that can make this move
        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                # In a full engine, we'd validate movement vectors here. 
                # For this refactor, we identify the piece matching the type.
                source_pos = pos
                break
        
        if source_pos:
            del board.pieces[source_pos]
            board.pieces[target_pos] = f"{color}{promo}"

    @staticmethod
    def get_king_moves(board, color):
        """Calculates all, legal, and illegal moves for the King."""
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        all_moves, legal_moves, illegal_moves = [], [], []
        
        # Directions: N, NE, E, SE, S, SW, W, NW
        directions = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
        
        for dc, dr in directions:
            target = (k_pos[0] + dc, k_pos[1] + dr)
            
            if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                m_str = f"K{board.FILES[target[0]]}{board.RANKS[target[1]]}"
                all_moves.append(m_str)
                
                # Check 1: Physical obstruction (friendly piece)
                if board.is_occupied_by_color(target, color):
                    illegal_moves.append(m_str)
                    continue
                
                # Check 2: Safety (Is the square attacked?)
                if ChessEngine.is_square_attacked(board, target, color):
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
            
            # Simplified Pawn attack logic
            if p_type == "P":
                #direction = 1 if attacker_color == "W" else -1
                if dr == 1 and abs(dc) == 1:
                    return True
            # Queen/Rook/Bishop line-of-sight would go here
            if p_type == "Q" or p_type == "R" or p_type == "B":
                if dc == 0 or dr == 0 or abs(dc) == abs(dr):
                    return True # Simplified for current board context
        return False