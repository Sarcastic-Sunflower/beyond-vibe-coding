class MoveGenerator:
    # Pre-defined movement vectors for the King
    K_OFFSETS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

    @staticmethod
    def get_black_moves(board_obj):
        all_m, leg_m, ill_m = set(), set(), set()
        files, ranks = board_obj.FILES, board_obj.RANKS
        
        # Iterate only over active Black pieces
        for (c, r), p in board_obj.pieces.items():
            if p[0] != "B": continue
            
            p_type = p[1]
            if p_type == "K":
                for dc, dr in MoveGenerator.K_OFFSETS:
                    nc, nr = c + dc, r + dr
                    if 0 <= nc < 8 and 0 <= nr < 8:
                        m_str = f"{p_type}{files[nc]}{ranks[nr]}"
                        all_m.add(m_str)
                        
                        target = board_obj.pieces.get((nc, nr))
                        if target and target.startswith("B"):
                            ill_m.add(m_str)
                        else:
                            leg_m.add(m_str)
        
        return sorted(all_m), sorted(leg_m), sorted(ill_m)