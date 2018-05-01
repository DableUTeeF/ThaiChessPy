
global BR, BN, BC, BM, BK, EM, BP
global WP, WR, WN, WC, WK, WM
global WHITE, board
global material, BLACK, piecevalue, positionvalue, evaltable
global KVAL, RVAL, NVAL, CVAL, MVAL, PVAL


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


