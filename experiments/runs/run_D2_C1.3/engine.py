class MoveGenerator:
    @staticmethod
    def get_black_moves(board_obj):
        all_moves, legal, illegal = [], [], []
        grid = board_obj.grid

        for r in range(8):
            for c in range(8):
                p = grid[r][c]
                if not p or p[0] != "B":
                    continue

                piece_type = p[1]
                # Offsets for King (and others if needed)
                offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

                for dc, dr in offsets:
                    nc, nr = c + dc, r + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        move_str = f"{piece_type}{board_obj.FILES[nc]}{board_obj.RANKS[nr]}"
                        all_moves.append(move_str)
                        
                        target = grid[nr][nc]
                        # A move is illegal if it lands on a piece of the same color
                        if target and target.startswith("B"):
                            illegal.append(move_str)
                        else:
                            legal.append(move_str)
        
        return (sorted(list(set(all_moves))), 
                sorted(list(set(legal))), 
                sorted(list(set(illegal))))