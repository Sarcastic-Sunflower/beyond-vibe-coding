def apply_san(self, san, color):
    # Standardize the token 
    token = san.strip("+#!?x ")
    dest = SQ_TO_IDX[token[-2:]]
    ptype = KING if token[0] == 'K' else ROOK
    target_val = color | ptype
    
    # Find which piece of this type can actually reach 'dest' 
    mover_src = -1
    for src in self.pieces[color]:
        if self.grid[src] == target_val:
            # Simple disambiguation: for this engine, we take the first match 
            mover_src = src
            break
            
    if mover_src != -1:
        # If there is an enemy piece at the destination, remove it from their list first
        if self.grid[dest]:
            enemy_color = BLACK if color == WHITE else WHITE
            if dest in self.pieces[enemy_color]:
                self.pieces[enemy_color].remove(dest)
        
        # Update the grid 
        self.grid[dest] = self.grid[mover_src]
        self.grid[mover_src] = 0
        
        # Sync the pieces list: remove old index, add new one
        self.pieces[color].remove(mover_src)
        self.pieces[color].append(dest)
        
        # Update king location if necessary 
        if ptype == KING:
            self.kings[color] = dest