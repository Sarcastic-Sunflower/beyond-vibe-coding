import re
from constants import KING_OFFSETS, DIRECTIONS, FILES, RANKS

class ChessEngine:
    # Captures: 1:Piece, 2:SourceFile, 3:SourceRank, 4:Capture, 5:Dest, 6:Promotion
    SAN_PATTERN = re.compile(r'([KQRBN])?([a-h])?([1-8])?(x)?([a-h][1-8])(=[QRBN])?')

    @staticmethod
    def apply_san_move(board, san, color):
        match = ChessEngine.SAN_PATTERN.search(san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2)
        dest_str = match.group(5)
        target_pos = (board.FILES_INDEX[dest_str[0]], board.RANKS_INDEX[dest_str[1]])
        
        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                # For pawns, if no source file is specified, they must be on the same file
                if p_type == "P" and not spec_f:
                    if pos[0] == target_pos[0]:
                        source_pos = pos
                        break
                # If source file IS specified (like 'd' in dxc8)
                elif spec_f and FILES[pos[0]] == spec_f:
                    source_pos = pos
                    break
                # For other pieces (like N in Nb6)
                elif p_type != "P":
                    source_pos = pos
                    break
        
        if source_pos:
            if target_pos in board.pieces:
                del board.pieces[target_pos]
            
            # Promotion logic
            new_piece = f"{color}{match.group(6)[1]}" if match.group(6) else board.pieces[source_pos]
            del board.pieces[source_pos]
            board.pieces[target_pos] = new_piece

    @staticmethod
    def is_square_attacked(board, pos, attacker_color):
        # Knight jumps
        for dc, dr in DIRECTIONS['knight']:
            tp = (pos[0] + dc, pos[1] + dr)
            if board.pieces.get(tp) == f"{attacker_color}N": return True
        
        # Sliders
        scan_dirs = {'B': DIRECTIONS['diagonal'], 'R': DIRECTIONS['orthogonal'], 'Q': KING_OFFSETS}
        for p_char, dirs in scan_dirs.items():
            for dc, dr in dirs:
                curr = (pos[0] + dc, pos[1] + dr)
                while board.is_on_board(curr):
                    p = board.pieces.get(curr)
                    if p:
                        if p == f"{attacker_color}{p_char}": return True
                        break
                    curr = (curr[0] + dc, curr[1] + dr)
        
        # Pawns (Attacking diagonally)
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