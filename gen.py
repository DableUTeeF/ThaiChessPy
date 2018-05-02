
def Generatemove():
    """
    firstmove[gameply] indicates where the moves of that gameply start in tree[]
    so, they are limited by firstmove[gameply+1] of course.
    """
    global firstmove, gameply, tomove
    firstmove[gameply + 1] = firstmove[gameply]

    # black tomove
    if tomove:
        Blackmove()
    else:
        Whitemove()


def Generatecapture():
    global firstmove, gameply, tomove
    firstmove[gameply + 1] = firstmove[gameply]
    if tomove:
        Bcapture()
    else:
        Wcapture()


def Wcapture():
    global board, WK, WR, WN, WC, WM, WP

    for i in range(64):
        if board[i] & 24:
            continue  # EMPTY=16  8+ are black pieces

        if board[i] == WK:
            Wkingcap(i)
        elif board[i] == WR:
            Wrookcap(i)
        elif board[i] == WN:
            Wknightcap(i)
        elif board[i] == WC:
            Wconecap(i)
        elif board[i] == WM:
            Wmedcap(i)
        elif board[i] == WP:
            Wpawncap(i)


def Whitemove():
    global board, WK, WR, WN, WC, WM, WP
    for i in range(64):
        if board[i] & 24:
            continue

        if board[i] == WK:
            Kingmove(i)
        elif board[i] == WR:
            Rookmove(i)
        elif board[i] == WN:
            Knightmove(i)
        elif board[i] == WC:
            Wconemove(i)
        elif board[i] == WM:
            Medmove(i)
        elif board[i] == WP:
            Wpawnmove(i)


def Bcapture():
    global board, BK, BR, BN, BC, BM, BP
    for i in range(64):
        if ~(board[i] & 8):
            continue  # white pieces are less than 8

        if board[i] == BK:
            Bkingcap(i)
        elif board[i] == BR:
            Brookcap(i)
        elif board[i] == BN:
            Bknightcap(i)
        elif board[i] == BC:
            Bconecap(i)
        elif board[i] == BM:
            Bmedcap(i)
        elif board[i] == BP:
            Bpawncap(i)


def Blackmove():
    for i in range(64):
        if ~(board[i] & 8):
            continue

        if board[i] == BK:
            Kingmove(i)
        elif board[i] == BR:
            Rookmove(i)
        elif board[i] == BN:
            Knightmove(i)
        elif board[i] == BC:
            Bconemove(i)
        elif board[i] == BM:
            Medmove(i)
        elif board[i] == BP:
            Bpawnmove(i)


def Linkmove(f, t, c, type):
    global firstmove, gameply, tree
    # each time we add a move shift the firstmove of next gameply too.
    m = tree[firstmove[gameply + 1]]
    m.f = f
    m.t = t
    m.c = c
    m.type = type
    m.s = 0  # let it be 0 at this stage
    tree[firstmove[gameply + 1]] = m
    firstmove[gameply + 1] += 1


def Kingmove(s):
    global RANK, FILE
    ABS = abs
    x = RANK(s)
    y = FILE(s)

    # # Similar to med
    Medmove(s)

    to = s - 8
    x1 = RANK(to)
    y1 = FILE(to)

    # Inboard indicates square>=0 and <64
    # and if board[to]== EMPTY or opponent pieces
    # and the distance from->to <=1
    # Notice in Linkmove() if it's capture move board[to]=captured piece
    # otherwise board[to]=EMPTY

    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s - 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Rookmove(s):
    global EM, board, FILE, ABS, tomove, RANK
    to = s
    # shift down one file for each iteration
    while FILE(to) > 0:
        to -= 1
        if board[to] == EM:
            Linkmove(s, to, EM, 0)
        else:  # a piece is found ,if it is opponent piece Linkmove
            if ((board[to] & 8) >> 3) != tomove:
                Linkmove(s, to, board[to], 0)
            break

    to = s
    while FILE(to) < 7:
        to += 1
        if board[to] == EM:
            Linkmove(s, to, EM, 0)
        else:
            if ((board[to] & 8) >> 3) != tomove:
                Linkmove(s, to, board[to], 0)
            break

    to = s
    while RANK(to) > 0:
        to -= 8
        if board[to] == EM:
            Linkmove(s, to, EM, 0)
        else:
            if ((board[to] & 8) >> 3) != tomove:
                Linkmove(s, to, board[to], 0)
            break

    to = s
    while RANK(to) < 7:
        to += 8
        if board[to] == EM:
            Linkmove(s, to, EM, 0)
        else:
            if ((board[to] & 8) >> 3) != tomove:
                Linkmove(s, to, board[to], 0)
            break


def Knightmove(s):
    global RANK, FILE, ABS, board
    x = RANK(s)
    y = FILE(s)

    # in 8 directions

    to = s - 17
    x1 = RANK(to)
    y1 = FILE(to)

    # The move is legal only the distance between from-to square <=2

    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 17
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 2) and ((ABS(y - y1)) <= 2):
        Linkmove(s, to, board[to], 0)


def Medmove(s):
    global RANK, FILE, ABS, board
    x = RANK(s)
    y = FILE(s)

    # The same idea as Kingmove()

    to = s - 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s - 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (((board[to] & 24) >> 3) != tomove) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Wconemove(s):
    global RANK, FILE, ABS, board
    x = RANK(s)
    y = FILE(s)

    Medmove(s)

    # add one more direction to Medmove()
    to = s - 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (board[to] & 24) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Wpawnmove(s):
    global PROM, board
    if board[s - 8] == EM:
        if s < 32:
            Linkmove(s, s - 8, EM, PROM)
        else:
            Linkmove(s, s - 8, EM, 0)
    Wpawncap(s)


def Bconemove(s):
    global RANK, FILE, ABS, board
    x = RANK(s)
    y = FILE(s)

    Medmove(s)

    to = s + 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (Inboard(to)) and (~(board[to] & 8)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Bpawnmove(s):
    global RANK, FILE, ABS, board, EM
    if board[s + 8] == EM:
        if s > 31:
            Linkmove(s, s + 8, EM, PROM)
        else:
            Linkmove(s, s + 8, EM, 0)

    Bpawncap(s)


def Wkingcap(s):
    global RANK, FILE, ABS, board

    x = RANK(s)
    y = FILE(s)

    Wconecap(s)

    to = s - 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Wrookcap(s):
    global EM, board, FILE, ABS, tomove, RANK
    to = s
    while FILE(to) > 0:
        to -= 1
        if board[to] == EM:
            continue
        if board[to] & 8:
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while FILE(to) < 7:
        to += 1
        if board[to] == EM:
            continue
        if board[to] & 8:
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while RANK(to) > 0:
        to -= 8
        if board[to] == EM:
            continue
        if board[to] & 8:
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while RANK(to) < 7:
        to += 8
        if board[to] == EM:
            continue
        if board[to] & 8:
            Linkmove(s, to, board[to], 0)
        break


def Wknightcap(s):

    global EM, board, FILE, ABS, tomove, RANK
    x = RANK(s)
    y = FILE(s)

    to = s - 17
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 17
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)


def Wconecap(s):
    global RANK, FILE, board, ABS
    x = RANK(s)
    y = FILE(s)

    Wmedcap(s)

    to = s - 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Wmedcap(s):
    global EM, board, FILE, ABS, tomove, RANK
    x = RANK(s)
    y = FILE(s)

    to = s - 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s - 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (board[to] & 8) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Wpawncap(s):
    global board, FILE, PROM
    f = FILE(s)
    if (f > 0) and (board[s - 9] & 8):
        if s < 32:
            Linkmove(s, s - 9, board[s - 9], PROM)
        else:
            Linkmove(s, s - 9, board[s - 9], 0)

    if (f < 7) and (board[s - 7] & 8):
        if s < 32:
            Linkmove(s, s - 7, board[s - 7], PROM)
        else:
            Linkmove(s, s - 7, board[s - 7], 0)


def Bkingcap(s):
    global EM, board, FILE, ABS, tomove, RANK
    x = RANK(s)
    y = FILE(s)

    Bconecap(s)

    to = s - 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 1
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s - 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Brookcap(s):
    global EM, board, FILE, ABS, tomove, RANK
    to = s
    while FILE(to) > 0:
        to -= 1
        if board[to] == EM:
            continue
        if ~(board[to] & 24):
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while FILE(to) < 7:
        to += 1
        if board[to] == EM:
            continue
        if ~(board[to] & 24):
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while RANK(to) > 0:
        to -= 8
        if board[to] == EM:
            continue
        if ~(board[to] & 24):
            Linkmove(s, to, board[to], 0)
        break

    to = s
    while RANK(to) < 7:
        to += 8
        if board[to] == EM:
            continue
        if ~(board[to] & 24):
            Linkmove(s, to, board[to], 0)
        break


def Bknightcap(s):

    x = RANK(s)
    y = FILE(s)

    to = s - 17
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s - 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 17
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 15
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 10
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)

    to = s + 6
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 2) and (ABS(y - y1) <= 2):
        Linkmove(s, to, board[to], 0)


def Bconecap(s):
    x = RANK(s)
    y = FILE(s)

    Bmedcap(s)

    to = s + 8
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Bmedcap(s):
    x = RANK(s)
    y = FILE(s)

    to = s - 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s - 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 9
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)

    to = s + 7
    x1 = RANK(to)
    y1 = FILE(to)
    if (~(board[to] & 24)) and (Inboard(to)) and (ABS(x - x1) <= 1) and (ABS(y - y1) <= 1):
        Linkmove(s, to, board[to], 0)


def Bpawncap(s):
    f = FILE(s)

    if (f > 0) and (~(board[s + 7] & 24)):
        if s > 31:
            Linkmove(s, s + 7, board[s + 7], PROM)
        else:
            Linkmove(s, s + 7, board[s + 7], 0)

    if (f < 7) and (~(board[s + 9] & 24)):
        if s > 31:
            Linkmove(s, s + 9, board[s + 9], PROM)
        else:
            Linkmove(s, s + 9, board[s + 9], 0)


def Inboard(s):
    if (s < 0) or (s > 63):
        return False
    return True
