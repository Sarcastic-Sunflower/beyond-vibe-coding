from typing import List, Set, Tuple

class ChessEngine:
    """
    A refactored chess engine focusing on efficiency and structure.
    Handles board state, move generation (pseudo-legal), and SAN processing.
    """
    FILES = "abcdefgh"
    RANKS = "12345678"

    def __init__(self):
        # 8x8 grid initialized to None
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "W"

    def setup_initial_position(self):
        """Sets up the specific initial position from the legacy code."""
        self.set_piece("b6", "WR")
        self.set_piece("g4", "WK")
        self.set_piece("g6", "BK")

    def set_piece(self, pos_str: str, piece: str):
        """Sets a piece at a given position string (e.g., 'a1')."""
        col, row = self._coords_from_str(pos_str)
        self.board[row][col] = piece

    def _coords_from_str(self, pos_str: str) -> Tuple[int, int]:
        col = self.FILES.index(pos_str[0])
        row = self.RANKS.index(pos_str[1])
        return col, row

    def _str_from_coords(self, col: int, row: int) -> str:
        return f"{self.FILES[col]}{self.RANKS[row]}"

    def apply_move(self, san: str, color: str):
        """
        Applies a move in SAN format. 
        Refactored to handle basic piece identification and movement.
        """
        # Clean SAN string
        clean_san = san.strip().translate(str.maketrans("", "", "+#!?x"))
        if not clean_san:
            return

        # Identify piece type and destination
        piece_type = clean_san[0] if clean_san[0] in "RKQBN" else "P"
        dest_str = clean_san[-2:]
        dest_col, dest_row = self._coords_from_str(dest_str)

        # Find the piece of the given color and type
        # Legacy logic: find the first matching piece
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == color and piece[1] == piece_type:
                    # Move the piece
                    self.board[r][c] = None
                    self.board[dest_row][dest_col] = piece
                    return

    def get_pseudo_legal_moves(self, color: str) -> List[str]:
        """
        Generates all pseudo-legal moves for the given color.
        Refactored for better performance and readability.
        """
        moves: Set[str] = set()
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == color:
                    moves.update(self._generate_piece_moves(piece, c, r))
        return sorted(list(moves))

    def _generate_piece_moves(self, piece: str, c: int, r: int) -> List[str]:
        piece_moves = []
        p_type = piece[1]
        color = piece[0]

        if p_type == "R":
            # Rook moves: horizontal and vertical
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dc, dr in directions:
                nc, nr = c + dc, r + dr
                while 0 <= nc < 8 and 0 <= nr < 8:
                    target = self.board[nr][nc]
                    if target:
                        if target[0] != color:
                            piece_moves.append(f"Rx{self._str_from_coords(nc, nr)}")
                        break
                    piece_moves.append(f"R{self._str_from_coords(nc, nr)}")
                    nc += dc
                    nr += dr
        elif p_type == "K":
            # King moves: 8 surrounding squares
            for dc in [-1, 0, 1]:
                for dr in [-1, 0, 1]:
                    if dc == 0 and dr == 0:
                        continue
                    nc, nr = c + dc, r + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        target = self.board[nr][nc]
                        if not target or target[0] != color:
                            prefix = "Kx" if target else "K"
                            piece_moves.append(f"{prefix}{self._str_from_coords(nc, nr)}")
        
        return piece_moves

    def get_position_string(self) -> str:
        """Returns the board state as a sorted semicolon-separated string."""
        parts = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece:
                    parts.append(f"{piece}{self._str_from_coords(c, r)}")
        
        # Sort criteria: White pieces first, then piece type, then position
        parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
        return ";".join(parts)
