from __future__ import print_function
import numpy as np
from init import Initgame


class movetype:
    def __init__(self, lens):
        self.f = np.zeros(lens, dtype='int32')
        self.t = np.zeros(lens, dtype='int32')
        self.c = np.zeros(lens, dtype='int32')
        self.type = np.zeros(lens, dtype='int32')
        self.s = np.zeros(lens, dtype='int32')

    def __getitem__(self, idx):
        return self.m(self.f[idx], self.t[idx], self.c[idx], self.type[idx], self.s[idx])

    class m:
        def __init__(self, f, t, c, types, s):
            self.f = f
            self.t = t
            self.c = c
            self.type = types
            self.s = s


def strcmp(str1, str2):
    lens = len(str1) if len(str1) < len(str2) else len(str2)
    for i in range(lens):
        if str1[i] != str2[i]:
            return ord(str1) - ord(str2)


# white pieces are less than 8
# global WP, WM, WC, WN, WR, WK
WP = 1
WM = 2
WC = 3
WN = 4
WR = 5
WK = 6

# black pieces are above 8 less than 16
# global BP, BM, BC, BN, BR, BK
BP = 9
BM = 10
BC = 11
BN = 12
BR = 13
BK = 14

# EMPTY square
# global EM
EM = 16

# global WHITE, BLACK, TRUE, FALSE
WHITE = 0
BLACK = 1
TRUE = 1
FALSE = 0

# global KVAL, RVAL, NVAL, CVAL, MVAL, PVAL, DIFF
KVAL = 0
RVAL = 500
NVAL = 350
CVAL = 250
MVAL = 150
PVAL = 118
DIFF = 60  # p 118 m 150

INF = 6500
MATE = 6000
LOSS = 5500

PROM = 1

MAXPLY = 600
RANK = lambda x: (x >> 3)
FILE = lambda x: (x & 7)
ABS = abs

# ------------------------------------------------------- #
board = np.zeros(64, dtype='int32')
tomove = 0
tree = movetype(MAXPLY)
gamemove = movetype(MAXPLY)
firstmove = np.zeros(MAXPLY, dtype='int32')
gameply = 0
material = np.zeros(2, dtype='int32')
positionvalue = np.zeros(2, dtype='int32')
evaltable = np.zeros((15, 64), dtype='int32')
piecevalue = np.zeros(15, dtype='int32')
zeromove = movetype(1)[0]
nodes = 0
kingsquare = np.zeros(2, dtype='int32')
kingend = np.zeros((2, 64), dtype='int32')

whitepawnattack = np.zeros((64, 64), dtype='int32')
whiteconeattack = np.zeros((64, 64), dtype='int32')

blackpawnattack = np.zeros((64, 64), dtype='int32')
blackconeattack = np.zeros((64, 64), dtype='int32')

medattack = np.zeros((64, 64), dtype='int32')
knightattack = np.zeros((64, 64), dtype='int32')
rookattack = np.zeros((64, 64), dtype='int32')
kingattack = np.zeros((64, 64), dtype='int32')
history = np.zeros((2, 64, 64), dtype='int32')


def main():
    global gameply, tomove
    gameply, tomove = Initgame()
    computer = ~tomove
    while 1:
        Printboard()
        if computer == tomove:
            # Search at 8 plys level. If the move is not zeromove then make it.
            cmove = Searchroot(8)
            if cmove.c != 0:
                Makemove(cmove)
            else:
                computer = ~tomove
            continue
        # firstmove[gameply] indicates the point that the moves start in tree[]
        firstmove[gameply] = 0
        Generatemove()
        n = firstmove[gameply + 1]
        j = 0
        m = 0
        for i in range(n):
            Makemove(tree[i])
            if Incheck(kingsquare[~tomove]):
                m += 1
            Unmakemove()

            # If all moves lead to illegal positions,it must be a mate or stalemate.
            if n == m:
                if Incheck(kingsquare[tomove]):
                    print("\n You are checkmated! ")
                else:
                    print("\n Stalemate")
                break
            j += 1
            if j % 9 == 0:
                print("\n %d.", j)
            else:
                print(" %d.", j)
            Showmove(tree[i])
        print("\n Enter Number of move (n,t,c,x=New game,Takeback,Computer to move,exit) => ")
        try:
            enter = raw_input()  # for python2
        except NameError:
            enter = input()  # python >= 3
        print("\n                ")
        print("\n           (Program Makruk 2.0 by Phoomchai Saihom.) ")
        print("\n                ")
        if ~strcmp(enter, "x"):
            break
        if ~strcmp(enter, "c"):
            computer = tomove
            continue

        if ~strcmp(enter, "n"):
            Initgame()

        if ~strcmp(enter, "t"):
            if gameply > 0:
                Unmakemove()
                computer = ~tomove
            continue

        k = atoi(enter)
        if (k <= 0) or (k > n):
            continue

        # Test legality after making the move
        Makemove(tree[k - 1])
        if Incheck(kingsquare[~tomove]):
            Unmakemove()
            print("Illegal move")
            continue


def Printboard():
    s = "                |---|---|---|---|---|---|---|---| "

    j = 8
    for i in range(64):
        if i % 8 == 0:
            print("\n%s\n             %d  |", s, j)
            j -= 1

        if board[i] == EM:
            print("   |")
        elif board[i] == WP:
            print("BIA|")
        elif board[i] == WM:
            print("MED|")
        elif board[i] == WC:
            print("CON|")
        elif board[i] == WN:
            print("MHA|")
        elif board[i] == WR:
            print("RUA|")
        elif board[i] == WK:
            print("KUN|")
        elif board[i] == BP:
            print("bia|")
        elif board[i] == BM:
            print("med|")
        elif board[i] == BC:
            print("con|")
        elif board[i] == BN:
            print("mha|")
        elif board[i] == BR:
            print("rua|")
        elif board[i] == BK:
            print("kun|")
        else:
            print(" %d,%d Strange piece", board[i], i)
            exit(0)
    print("\n%s\n                  a   b   c   d   e   f   g   h", s)


# To show the move in string

def Showmove(m):
    print("%s%d%s%d" % (chr(ord('a') + FILE(m.f)), 8 - RANK(m.f), chr(ord('a') + FILE(m.t)), 8 - RANK(m.t)))


if __name__ == '__main__':
    main()
