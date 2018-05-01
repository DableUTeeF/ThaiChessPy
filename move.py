

def Makemove(m):
    global BR, BN, BC, BM, BK, EM, BP
    global WP, WR, WN, WC, WK, WM
    global WHITE, board, blackconeattack, RANK, FILE, TRUE, FALSE
    global material, BLACK, piecevalue, positionvalue, evaltable
    global KVAL, RVAL, NVAL, CVAL, MVAL, PVAL, blackpawnattack
    global whiteconeattack, kingattack, medattack, whitepawnattack
    global knightattack, rookattack, kingsquare
    global gamemove, PROM, tomove, DIFF

    fr = m.f
    to = m.t
    ca = m.c
    ty = m.type
    p = board[fr]

    # Save the move in order to Unmake() later
    global gameply
    gamemove[gameply] = m
    gameply += 1

    # If it's king's move save the location,so we can use to test legality in Incheck.
    if (p | 8) == BK:
        kingsquare[tomove] = to

    # Capture move,reduce opponent material and position value
    if ca != EM:
        material[~tomove] -= piecevalue[ca]
        positionvalue[~tomove] -= evaltable[ca][to]

    # add the difference between evaluation table
    positionvalue[tomove] += evaltable[p][to] - evaltable[p][fr]

    # Promotion change the pawn to med,add material
    if ty & PROM:
        p += 1
        board[to] = ++p
        material[tomove] += DIFF
        positionvalue[tomove] += evaltable[p][to]  # evaltable of pawn at six rank=0

    else:
        board[to] = p

    board[fr] = EM

    tomove = ~tomove  # swap side


# Inversely similar to Makemove()

def Unmakemove():
    global BR, BN, BC, BM, BK, EM, BP
    global WP, WR, WN, WC, WK, WM
    global WHITE, board, blackconeattack, RANK, FILE, TRUE, FALSE
    global material, BLACK, piecevalue, positionvalue, evaltable
    global KVAL, RVAL, NVAL, CVAL, MVAL, PVAL, blackpawnattack
    global whiteconeattack, kingattack, medattack, whitepawnattack
    global knightattack, rookattack, kingsquare
    global gamemove, PROM, tomove, DIFF, gamemove, gameply

    gameply -= 1
    m = gamemove[gameply]
    tomove = ~tomove

    fr = m.f
    to = m.t
    ty = m.type
    cap = m.c
    p = board[to]

    if (p | 8) == BK:
        kingsquare[tomove] = fr

    if ty & PROM:
        positionvalue[tomove] -= evaltable[p][to]
        p -= 1
        material[tomove] -= DIFF

    board[fr] = p

    positionvalue[tomove] -= evaltable[p][to] - evaltable[p][fr]

    if cap != EM:
        material[~tomove] += piecevalue[cap]
        positionvalue[~tomove] += evaltable[cap][to]

    board[to] = cap
