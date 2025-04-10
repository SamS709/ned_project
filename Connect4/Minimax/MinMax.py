import random

from Connect4.Connect4 import *

# Minimax algorithm is a tree searching algorithm that determines the best move to play

# In the case of Connect4, this algorith is boosted with alpha-beta pruning that deletes decrease the number of nodes that are evaluated by the minimax algorithm in its search tree

class MinMax(Connect4):

    def __init__(self):
        super().__init__()

    def minmax(self,table,depth,alpha,beta,n): # returns the score of a board
        # either an end is detected
        # either the exploration's depth is reached and the table is evaluated according to the score function
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

    def best_pos(self,table,depth): # returns the best move to play among all possible moves
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



