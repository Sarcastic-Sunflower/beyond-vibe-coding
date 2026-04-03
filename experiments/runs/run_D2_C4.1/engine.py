import re
from constants import KING_OFFSETS, DIRECTIONS, FILES, RANKS

class ChessEngine:
    SAN_PATTERN = re.compile(r'([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(=[QRBN])?')

    @staticmethod
    def apply_san_move(board, san, color):
        match = ChessEngine.SAN_PATTERN.search(san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2)
        dest_str = match.group(4)
        target_pos = (board.FILES_INDEX[dest_str[0]], board.RANKS_INDEX[dest_str[1]])
        
        # Determine piece to move
        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                # Basic disambiguation for pawns/knights
                if spec_f and FILES[pos[0]] != spec_f: continue
                source_pos = pos
                break
        
        if source_pos:
            promo = f"{color}{match.group(5)[1]}" if match.group(5) else board.pieces[source_pos]
            del board.pieces[source_pos]
            board.pieces[target_pos] = promo

    @staticmethod
    def is_square_attacked(board, pos, attacker_color):
        # Check Knights
        for dc, dr in DIRECTIONS['knight']:
            tp = (pos[0] + dc, pos[1] + dr)
            if board.pieces.get(tp) == f"{attacker_color}N": return True
        
        # Check Sliders (Bishops, Rooks, Queens)
        scan_dirs = {
            'B': DIRECTIONS['diagonal'],
            'R': DIRECTIONS['orthogonal'],
            'Q': DIRECTIONS['diagonal'] + DIRECTIONS['orthogonal']
        }
        for p_char, dirs in scan_dirs.items():
            for dc, dr in dirs:
                curr = (pos[0] + dc, pos[1] + dr)
                while board.is_on_board(curr):
                    p = board.pieces.get(curr)
                    if p:
                        if p == f"{attacker_color}{p_char}": return True
                        break
                    curr = (curr[0] + dc, curr[1] + dr)
        
        # Check Pawns
        pawn_dir = 1 if attacker_color == "W" else -1
        for dc in [-1, 1]:
            if board.pieces.get((pos[0] + dc, pos[1] - pawn_dir)) == f"{attacker_color}P":
                return True
        return False

    @staticmethod
    def get_king_moves(board, color):
        opp_color = "B" if color == "W" else "W"
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        
        all_m, leg_m, ill_m = [], [], []
        
        for dc, dr in KING_OFFSETS:
            target = (k_pos[0] + dc, k_pos[1] + dr)
            if not board.is_on_board(target): continue
            
            m_str = f"K{FILES[target[0]]}{RANKS[target[1]]}"
            all_m.append(m_str)
            
            occupant = board.pieces.get(target)
            if (occupant and occupant[0] == color) or ChessEngine.is_square_attacked(board, target, opp_color):
                ill_m.append(m_str)
            else:
                leg_m.append(m_str)
                
        return sorted(all_m), sorted(leg_m), sorted(ill_m)