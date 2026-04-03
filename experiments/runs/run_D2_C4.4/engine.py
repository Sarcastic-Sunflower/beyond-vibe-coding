import re
import copy
from constants import KING_OFFSETS, DIRECTIONS, FILES, RANKS

class ChessEngine:
    # Adjusted regex to handle '+' and '#' suffixes
    SAN_PATTERN = re.compile(r'([KQRBN])?([a-h])?([1-8])?(x)?([a-h][1-8])(=[QRBN])?[\+#]?')

    @staticmethod
    def apply_san_move(board, san, color):
        match = ChessEngine.SAN_PATTERN.match(san)
        if not match: return

        p_type = match.group(1) or "P"
        spec_f = match.group(2)
        dest_str = match.group(5)
        target_pos = (board.FILES_INDEX[dest_str[0]], board.RANKS_INDEX[dest_str[1]])
        
        source_pos = None
        for pos, piece in board.pieces.items():
            if piece == f"{color}{p_type}":
                if p_type == "P":
                    # Pawn move/capture logic
                    if spec_f: # Capture like 'dxc8'
                        if FILES[pos[0]] == spec_f and abs(pos[0] - target_pos[0]) == 1:
                            source_pos = pos
                            break
                    elif pos[0] == target_pos[0]: # Standard push
                        source_pos = pos
                        break
                else:
                    source_pos = pos
                    break
        
        if source_pos:
            if target_pos in board.pieces:
                del board.pieces[target_pos]
            new_piece = f"{color}{match.group(6)[1]}" if match.group(6) else board.pieces[source_pos]
            del board.pieces[source_pos]
            board.pieces[target_pos] = new_piece

    @staticmethod
    def is_square_attacked(board_pieces, pos, attacker_color):
        # Knight attacks
        for dc, dr in DIRECTIONS['knight']:
            if board_pieces.get((pos[0] + dc, pos[1] + dr)) == f"{attacker_color}N": return True
        
        # Slider attacks
        scan = {'B': DIRECTIONS['diagonal'], 'R': DIRECTIONS['orthogonal'], 'Q': KING_OFFSETS}
        for p_char, dirs in scan.items():
            for dc, dr in dirs:
                curr = (pos[0] + dc, pos[1] + dr)
                while 0 <= curr[0] < 8 and 0 <= curr[1] < 8:
                    p = board_pieces.get(curr)
                    if p:
                        if p == f"{attacker_color}{p_char}": return True
                        break
                    curr = (curr[0] + dc, curr[1] + dr)
        
        # Pawn attacks
        p_dir = 1 if attacker_color == "W" else -1
        for dc in [-1, 1]:
            if board_pieces.get((pos[0] + dc, pos[1] - p_dir)) == f"{attacker_color}P": return True
        
        # King attacks (to prevent Kings from touching)
        for dc, dr in KING_OFFSETS:
            if board_pieces.get((pos[0] + dc, pos[1] + dr)) == f"{attacker_color}K": return True
            
        return False

    @staticmethod
    def get_king_moves(board, color):
        opp_color = "W" if color == "B" else "B"
        k_pos = next(pos for pos, p in board.pieces.items() if p == f"{color}K")
        all_m, leg_m, ill_m = [], [], []

        for dc, dr in KING_OFFSETS:
            target = (k_pos[0] + dc, k_pos[1] + dr)
            if not board.is_on_board(target): continue
            
            m_str = f"K{FILES[target[0]]}{RANKS[target[1]]}"
            all_m.append(m_str)

            # Check if move is legal:
            # 1. Square isn't occupied by own piece
            # 2. Square isn't attacked by opponent
            occupant = board.pieces.get(target)
            if (occupant and occupant[0] == color) or ChessEngine.is_square_attacked(board.pieces, target, opp_color):
                ill_m.append(m_str)
            else:
                leg_m.append(m_str)
                
        return sorted(all_m), sorted(leg_m), sorted(ill_m)