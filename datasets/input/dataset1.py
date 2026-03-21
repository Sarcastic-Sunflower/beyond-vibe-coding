#!/usr/bin/env python3
import sys, os

FILES = "abcdefgh"
RANKS = "12345678"

board = [["" for _ in range(8)] for _ in range(8)]
turn = "W"

board[5][1] = "WR"
board[3][6] = "WK"
board[5][6] = "BK"


def get_moves(color):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p or p[0] != color:
                continue
            if p[1] == "R":
                for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nc, nr = c + dc, r + dr
                    while 0 <= nc <= 7 and 0 <= nr <= 7:
                        tp = board[nr][nc]
                        if tp and tp[0] == color:
                            break
                        t = FILES[nc] + RANKS[nr]
                        moves.append("R" + ("x" if tp else "") + t)
                        if tp:
                            break
                        nc += dc
                        nr += dr
            elif p[1] == "K":
                for dc in [-1, 0, 1]:
                    for dr in [-1, 0, 1]:
                        if dc == 0 and dr == 0:
                            continue
                        nc, nr = c + dc, r + dr
                        if 0 <= nc <= 7 and 0 <= nr <= 7:
                            tp = board[nr][nc]
                            if not tp or tp[0] != color:
                                t = FILES[nc] + RANKS[nr]
                                moves.append("K" + ("x" if tp else "") + t)
    return sorted(set(moves))


def pos_string():
    parts = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                parts.append(p + FILES[c] + RANKS[r])
    parts.sort(key=lambda x: (0 if x[0] == "W" else 1, x[1], x[2:]))
    return ";".join(parts)


def do_move(san, color):
    s = san.strip()
    for ch in "+#!?":
        s = s.replace(ch, "")
    s = s.replace("x", "")
    pt = s[0] if s[0] in "RKQBN" else "P"
    dest = s[-2:]
    dr = RANKS.index(dest[1])
    dc = FILES.index(dest[0])
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p[0] == color and p[1] == pt:
                board[r][c] = ""
                board[dr][dc] = p
                return


def main():
    global turn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    moves_path = (
        sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "moves1.txt")
    )

    if os.path.isfile(moves_path):
        for line in open(moves_path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            do_move(line, turn)
            turn = "B" if turn == "W" else "W"

    mvs = get_moves(turn)
    mv_str = ";".join(mvs)
    pos = pos_string()
    move_line = f"{len(mvs)} :" + (f" {mv_str}" if mvs else "")

    out_path = os.path.join(script_dir, "output1.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pos + "\n")
        f.write(move_line + "\n")
        f.write(move_line + "\n")
        f.write("0 :\n")


if __name__ == "__main__":
    main()
