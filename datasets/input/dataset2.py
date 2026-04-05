#!/usr/bin/env python3
import os
import sys

FILES = "abcdefgh"
RANKS = "12345678"

board = [["" for _ in range(8)] for _ in range(8)]

# Apply starting position
board[6][1] = "BK"  # Black King on b7
board[3][2] = "BN"  # Black Knight on c4
board[5][3] = "WP"  # White Pawn on d6
board[4][4] = "WP"  # White Pawn on e5
board[4][0] = "WK"  # White King on a5

def do_move(san, color):
    """Blindly teleports the first piece matching the requested type."""
    if not san: return
    s = san.strip().replace("+", "").replace("#", "").replace("x", "")
    pt = s[0] if s[0] in "RKQBN" else "P"
    dest = s[-2:]
    
    if len(dest) != 2 or dest[0] not in FILES or dest[1] not in RANKS:
        return
        
    dc = FILES.index(dest[0])
    dr = RANKS.index(dest[1])
    
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p[0] == color and p[1] == pt:
                board[r][c] = ""
                board[dr][dc] = p
                return

def get_black_moves():
    all_moves = []
    legal_moves = []
    illegal_moves = []
    
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p or p[0] != "B":
                continue
            
            offsets = []
            if p[1] == "N":
                offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), 
                           (1, 2), (1, -2), (-1, 2), (-1, -2)]
            elif p[1] == "K":
                offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), 
                           (-1, 0), (-1, -1), (0, -1), (1, -1)]
                
            for dc, dr in offsets:
                nc, nr = c + dc, r + dr
                # Only evaluate moves that stay on the 8x8 grid
                if 0 <= nc <= 7 and 0 <= nr <= 7:
                    t = FILES[nc] + RANKS[nr]
                    move_str = f"{p[1]}{t}"
                    all_moves.append(move_str)
                    
                    if board[nr][nc].startswith("B"):
                        illegal_moves.append(move_str)
                    else:
                        legal_moves.append(move_str)
                        
    return all_moves, legal_moves, illegal_moves

def pos_string():
    parts = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                parts.append(p + FILES[c] + RANKS[r])
    parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
    return ";".join(parts)

def format_move_line(mvs):
    if not mvs:
        return "0 :"
    return f"{len(mvs)} : " + ";".join(mvs)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = os.path.join(script_dir, "moves2.txt")
    
    if os.path.isfile(moves_path):
        with open(moves_path, "r", encoding="utf-8") as f:
            content = f.read().split()
            moves_list = [m for m in content if not m.endswith(".")]
            
        turn = "W"
        for m in moves_list:
            do_move(m, turn)
            turn = "B" if turn == "W" else "W"

    # Generate data strings
    pos = pos_string()
    all_m, leg_m, ill_m = get_black_moves()
    
    all_line = format_move_line(all_m)
    leg_line = format_move_line(leg_m)
    ill_line = format_move_line(ill_m)

    out_path = os.path.join(script_dir, "output2.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pos + "\n")
        f.write(all_line + "\n")
        f.write(leg_line + "\n")
        f.write(ill_line + "\n")

if __name__ == "__main__":
    main()