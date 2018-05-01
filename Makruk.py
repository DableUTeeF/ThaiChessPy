from __future__ import print_function
import numpy as np


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


MAXPLY = 600

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
    cmove = movetype(1)[0]
    Initgame()
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


if __name__ == '__main__':
    main()
