from table import Inittable
from gen import Inboard

global BR, BN, BC, BM, BK, EM, BP
global WP, WR, WN, WC, WK, WM
global WHITE, board, blackconeattack, RANK, FILE, TRUE, FALSE
global material, BLACK, piecevalue, positionvalue, evaltable
global KVAL, RVAL, NVAL, CVAL, MVAL, PVAL, blackpawnattack
global whiteconeattack, kingattack, medattack, whitepawnattack
global knightattack, rookattack


def Initgame():
    Initvalue()
    Inittable()  # in table.c
    Initboard()
    Initattacktable()
    global gameply
    gameply = 0
    global tomove
    tomove = WHITE


def Initboard():
    # Starting board
    b = [BR, BN, BC, BM, BK, BC, BN, BR,
        EM, EM, EM, EM, EM, EM, EM, EM,
        BP, BP, BP, BP, BP, BP, BP, BP,
        EM, EM, EM, EM, EM, EM, EM, EM,
        EM, EM, EM, EM, EM, EM, EM, EM,
        WP, WP, WP, WP, WP, WP, WP, WP,
        EM, EM, EM, EM, EM, EM, EM, EM,
        WR, WN, WC, WK, WM, WC, WN, WR]

    # Calculate material and position value for both sides.
    # and mark king locations.

    for i in range(64):
        board[i] = b[i]
        if b[i] != EM:
            if b[i] & 8:
                material[BLACK] += piecevalue[b[i]]
                positionvalue[BLACK] += evaltable[b[i]][i]

            else:
                material[WHITE] += piecevalue[b[i]]
                positionvalue[WHITE] += evaltable[b[i]][i]
        global kingsquare
        if b[i] == WK:
            kingsquare[WHITE] = i
        if b[i] == BK:
            kingsquare[BLACK] = i


def Initvalue():
    piecevalue[WK] = KVAL
    piecevalue[WR] = RVAL
    piecevalue[WN] = NVAL
    piecevalue[WC] = CVAL
    piecevalue[WM] = MVAL
    piecevalue[WP] = PVAL

    piecevalue[BK] = KVAL
    piecevalue[BR] = RVAL
    piecevalue[BN] = NVAL
    piecevalue[BC] = CVAL
    piecevalue[BM] = MVAL
    piecevalue[BP] = PVAL

# All attack[f][t] are used mainly in Incheck().The idea is if the piece at
# from square can attack to square then attack[from][to]=TRUE except rookattack.
# The residual were initialized to 0 already.


def Initattacktable():
    """ attack[from][to]"""
    dirs = [-17, -15, -10, -6, 6, 10, 15, 17]

    for i in range(64):
        x = RANK(i)
        y = FILE(i)

        if (y != 7) and (x != 7):
            blackpawnattack[i][i + 9] = TRUE
            blackconeattack[i][i + 9] = TRUE
            whiteconeattack[i][i + 9] = TRUE

            kingattack[i][i + 9] = TRUE
            medattack[i][i + 9] = TRUE

        if (y != 0) and (x != 7):
            blackpawnattack[i][i + 7] = TRUE
            blackconeattack[i][i + 7] = TRUE
            whiteconeattack[i][i + 7] = TRUE
            medattack[i][i + 7] = TRUE
            kingattack[i][i + 7] = TRUE

        if (x != 0) and (y != 0):
            blackconeattack[i][i - 9] = TRUE
            whiteconeattack[i][i - 9] = TRUE
            whitepawnattack[i][i - 9] = TRUE
            medattack[i][i - 9] = TRUE
            kingattack[i][i - 9] = TRUE

        if (x != 0) and (y != 7):
            blackconeattack[i][i - 7] = TRUE
            whiteconeattack[i][i - 7] = TRUE
            whitepawnattack[i][i - 7] = TRUE
            medattack[i][i - 7] = TRUE
            kingattack[i][i - 7] = TRUE

        if x != 0:
            whiteconeattack[i][i - 8] = TRUE
            kingattack[i][i - 8] = TRUE

        if x != 7:
            blackconeattack[i][i + 8] = TRUE
            kingattack[i][i + 8] = TRUE

        if y != 0:
            kingattack[i][i - 1] = TRUE

        if y != 7:
            kingattack[i][i + 1] = TRUE

        for j in range(8):
            k = i + dirs[j]
            x1 = RANK(k)
            y1 = FILE(k)
            if (Inboard(k)) and (abs(x - x1) <= 2) and (abs(y - y1) <= 2):
                knightattack[i][k] = TRUE

        # For the rook we assign the direction from rook to attacked piece instead.
        # see Incheck()

        for j in range(64):
            if j == i:
                continue

            x1 = RANK(j)
            y1 = FILE(j)

            if (x == x1) and (y1 > y):
                rookattack[j][i] = -1
            if (x == x1) and (y1 < y):
                rookattack[j][i] = 1
            if (y == y1) and (x1 > x):
                rookattack[j][i] = -8
            if (y == y1) and (x1 < x):
                rookattack[j][i] = 8
