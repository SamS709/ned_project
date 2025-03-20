import random

from Connect4.Connect4 import *

class MinMax(Connect4):

    def __init__(self):
        super().__init__()

    def minmax(self,table,depth,alpha,beta,n):

        grid = super().table_to_grid(table)
        if super().win(grid):
            return 1000
        if super().lose(grid):
            return -1000
        if super().tie(grid):
            return 0
        if depth == 0:
            return super().score(table)

        if n == 1:
            a = -10000
            Lpos = super().avaible_pos_graphics(table)
            for pos in Lpos:
                TABLE = table.copy()
                TABLE[pos[0],pos[1]]=1
                val = self.minmax(TABLE,depth-1,alpha,beta,2)
                if val>=a:
                    a=val
                if a > beta:
                    return a
                alpha = max(alpha,val)
            return a

        if n == 2:
            b = 10000
            Lpos = super().avaible_pos_graphics(table)
            for pos in Lpos:
                TABLE = table.copy()
                TABLE[pos[0], pos[1]] = 2
                val = self.minmax(TABLE, depth - 1, alpha, beta, 1)
                if val <= b:
                    b = val
                if b < alpha:
                    return b
            return b

    def best_pos(self,table,depth): # renvoie la meilleure position selon l'algo minmax pour la table donnée
        Lpos = self.avaible_pos_graphics(table)
        a = -10000
        Leqpos = []
        for pos in Lpos:
            TABLE = table.copy()
            TABLE[pos[0],pos[1]]=1
            val= self.minmax(TABLE,depth,-10000,10000,2)
            if val>a:
                a=val
                Leqpos = [pos]
            elif val == a:
                Leqpos.append(pos)
        POS = random.choice(Leqpos)
        return POS

if __name__=='__main__':
    minmax = MinMax()
    table = np.array([[0 for j in range(7)] for i in range(6)])
    table[5,0]=1
    table[4, 0] = 1
    table[3, 0] = 1
    print(table)
    POS = minmax.best_pos(table,2)
    table[POS[0],POS[1]]=1
    print(table)

