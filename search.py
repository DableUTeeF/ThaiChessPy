import numpy as np
from time import clock
from move import *
from gen import *


def Showmove(m):
    global FILE, RANK
    print("%s%d%s%d" % (chr(ord('a') + FILE(m.f)), 8 - RANK(m.f), chr(ord('a') + FILE(m.t)), 8 - RANK(m.t)))


def Searchroot(depth):
    global zeromove, TRUE, firstmove, gameply, history, tree, INF
    global kingsquare, tomove, MATE, FALSE, LOSS, nodes
    temp, good = zeromove
    nomove = TRUE

    # reset these values each time before searching
    firstmove[gameply] = 0
    nodes = 0
    history = np.zeros((2, 64, 64), dtype='int32')

    # start clock
    t1 = clock()

    Generatemove()

    print("\n                ")
    print("\n           (Program Makruk 2.0 by Phoomchai Saihom.) ")
    print("\n                ")
    print("\n Computer say:=> I am thinking.Please wait a minutes. Depth= ")
    # Start iterative deepening

    for level in range(1, depth):
        best = -INF

        # Add sorting score to all move
        Scoreforsorting()

        print("\b%d", level)

        # loop all semilegal moves
        for i in range(firstmove[gameply + 1]):

            # sorting by history score

            bs = tree[i].s
            bi = i

            for j in range(i + 1, firstmove[gameply + 1]):
                if tree[j].s > bs:
                    bi = j
                    bs = tree[j].s

            # a better move found swap the moves
            if bi != i:
                temp = tree[i]
                tree[i] = tree[bi]
                tree[bi] = temp

            # /////////////////////////end sorting

            # //if the move leads to illegal position,don't go on.
            Makemove(tree[i])
            if Incheck(kingsquare[~tomove]):
                Unmakemove()
                continue

            nomove = FALSE
            value = -Search(-MATE, MATE, level - 1)
            Unmakemove()

            # //better move found Update history table
            if value > best:
                best = value
                good = tree[i]
                Updatehistory(tree[i], level)

    t2 = clock()

    # //No legal move at all
    if nomove:
        print("\n Game is ended")
        if Incheck(kingsquare[tomove]):
            print(". I am checkmated ")
        else:
            print(" by stalemate ")

    else:  # Show searching results
        print(" Move= ")
        Showmove(good)
        print(" Score=%d Time =%.2f N=%d", best, float((t2 - t1) / 1000., nodes))
    return good


def Search(alpha, beta, depth):
    global nodes, TRUE
    nodes += 1
    nomove = TRUE

    # //at leaf node depth==0 Qsearch() is called
    if depth == 0:
        return Qsearch(alpha, beta)

    Generatemove()

    # //Add score from history table to all moves
    Scoreforsorting()

    # //Loop all semilegal moves
    for i in range(firstmove[gameply], firstmove[gameply + 1]):

        # ///////////////////// sorting by history score

        bs = tree[i].s
        bi = i

        for j in range(i+1, firstmove[gameply + 1]):
            if tree[j].s > bs:
                bi = j
                bs = tree[j].s

        if bi != i:
            temp = tree[i]
            tree[i] = tree[bi]
            tree[bi] = temp
        # /////////////////////////end sorting

        # //Test legality after making the move
        Makemove(tree[i])
        if Incheck(kingsquare[~tomove]):
            Unmakemove()
            continue

        nomove = FALSE
        value = -Search(-beta, -alpha, depth - 1)
        Unmakemove()

        # //Update history table
        if value > alpha:
            Updatehistory(tree[i], depth)
            if value >= beta:
                return beta  # //value is too good to be true,so return beta
            alpha = value

    # //No legal move means a mate or stalemate
    if nomove:
        if Incheck(kingsquare[tomove]):
            return -LOSS + gameply  # //in order to discriminate shorter and longer mate
        else:
            return 0

    # //all moves have been searched return best score so far.
    return alpha


def eval():  # static evaluation quite simple
    global material, WHITE, BLACK, kingend, positionvalue
    wm = material[WHITE]
    bm = material[BLACK]

    # if any side has less than 1000 use king end game table instead

    if (wm <= 1000) or (bm <= 1000):
        ke = kingend[WHITE][kingsquare[WHITE]] - kingend[BLACK][kingsquare[BLACK]]

        if tomove:
            return bm - wm + positionvalue[BLACK] - positionvalue[WHITE] - ke
        else:
            return wm - bm + positionvalue[WHITE] - positionvalue[BLACK] + ke

    if tomove:
        return bm - wm + positionvalue[BLACK] - positionvalue[WHITE]
    else:
        return wm - bm + positionvalue[WHITE] - positionvalue[BLACK]


def Qsearch(alpha, beta):
    global nodes, tree
    nodes += 1

    # //Calculate standpat value
    x = eval()
    if x >= beta:
        return beta
    if x > alpha:
        alpha = x

    # //Only capture moves are considered in Qsearch()
    Generatecapture()

    # //add MVV/LVA score
    Scoreforsorting()

    # ///loop through all capture moves

    for i in range(firstmove[gameply], firstmove[gameply+1]):
        # ///////////////////// sorting by MVV/LVA
        bs = tree[i].s
        bi = i

        for j in range(i+1, firstmove[gameply+1]):
            if tree[j].s > bs:
                bi = j
                bs = tree[j].s

        if bi != i:
            temp = tree[i]
            tree[i] = tree[bi]
            tree[bi] = temp
        # /////////////////////////end sorting

        Makemove(tree[i])
        if Incheck(kingsquare[~tomove]):
            Unmakemove()
            continue
        x = -Qsearch(-beta, -alpha)
        Unmakemove()
        if x > alpha:
            if x >= beta:
                return beta
            alpha = x
    return alpha


def Incheck(sq):
    global board, BK, whitepawnattack, medattack, whiteconeattack, knightattack
    global kingattack, rookattack, WP, WM, WC, WN, WK, WR, EM, blackpawnattack
    global BP, BM, BC, BN, blackconeattack, BR

    # black king is in check ?
    if board[sq] == BK:
        for i in range(64):
            if board[i] & 24:
                continue
            if board[i] == WP:
                if whitepawnattack[i][sq]:
                    return TRUE
            elif board[i] == WM:
                if medattack[i][sq]:
                    return TRUE
            elif board[i] == WC:
                if whiteconeattack[i][sq]:
                    return TRUE
            elif board[i] == WN:
                if knightattack[i][sq]:
                    return TRUE
            elif board[i] == WK:
                if kingattack[i][sq]:
                    return TRUE
            elif board[i] == WR:
                if rookattack[i][sq]:
                    dir = rookattack[i][sq] # //direction of rook to the king
                    r = i  # //the rook is originally at square i

                    while board[r] == EM:
                        r += dir  # //shift that rook toward the king until a piece is found.
                    if sq == r:
                        return TRUE  # //No blocking piece between rook and the king

        return FALSE

    else:  # //white king
        for i in range(64):
            if ~(board[i] & 8):
                continue
            # switch (board[i]) {
            if board[i] == BP:
                if blackpawnattack[i][sq]:
                    return TRUE
            elif board[i] == BM:
                if medattack[i][sq]:
                    return TRUE
            elif board[i] == BC:
                if blackconeattack[i][sq]:
                    return TRUE
            elif board[i] == BN:
                if knightattack[i][sq]:
                    return TRUE
            elif board[i] == BK:
                if kingattack[i][sq]:
                    return TRUE
            elif board[i] == BR:
                if rookattack[i][sq]:
                    dir = rookattack[i][sq]
                    r = i
                    while board[r] == EM:
                        r += dir
                    if sq == r:
                        return TRUE
        return FALSE


def Updatehistory(m, d):
    """
    We already have capture moves above in the list.
    So,only non-capture move is record on the table.
    And the move that leads to cut off in higher depth is more promising.
    """
    global EM, tomove, history
    if m.c != EM:
        return
    history[tomove][m.f][m.t] += d * d


def Scoreforsorting():
    """
    Capture moves are first.
    //MVV/LVA (most valuable victim/least valuable attacker) method is used.
    //The rests are sorted by history score
    //With 16 bit compiler these figures can overflow.
    """
    for i in range(firstmove[gameply], firstmove[gameply]+1):
        if tree[i].c != EM:
            tree[i].s = (1000000 + tree[i].c - board[tree[i].f])
        else:
            tree[i].s = history[tomove][tree[i].f][tree[i].t]
