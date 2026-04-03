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
                offsets = []
                
                if piece_type == "N":
                    offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
                elif piece_type == "K":
                    offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                elif piece_type == "Q": # Added logic for the promoted Queen
                    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
                    for dc, dr in directions:
                        for step in range(1, 8):
                            nc, nr = c + dc * step, r + dr * step
                            if 0 <= nc < 8 and 0 <= nr < 8:
                                offsets.append((dc * step, dr * step))
                                if grid[nr][nc]: break # Stop at first piece
                            else: break

                for dc, dr in offsets:
                    nc, nr = c + dc, r + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        move_str = f"{piece_type}{board_obj.FILES[nc]}{board_obj.RANKS[nr]}"
                        all_moves.append(move_str)
                        target = grid[nr][nc]
                        if target and target.startswith("B"):
                            illegal.append(move_str)
                        else:
                            legal.append(move_str)
        
        return sorted(list(set(all_moves))), sorted(list(set(legal))), sorted(list(set(illegal)))