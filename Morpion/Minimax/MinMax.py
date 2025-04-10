from Morpion.Morpion import *

# Minimax algorithm is a tree searching algorithm that determines the best move to play

class MinMax(Morpion):

    def __init__(self):
        super().__init__()

    def minimax(self,table,player,depth): # returns the value of a table when a givenplayer (maximiser or minimiser) plays until the depth of the exploration has been reached
        # base case
        if self.win(table):
            return 1
        if self.lose(table):
            return -1
        if self.tie(table):
            return 0
        if depth == 0:
            return 0
        # recursion
        if player=="maximiser":
            a=-2
            for i in range(table.shape[0]):
                for j in range(table.shape[1]):
                    TABLE = table.copy()
                    pos = table[i,j]
                    if pos==0:
                        TABLE[i,j] = 1
                        val = self.minimax(TABLE,"minimiser",depth-1)
                        if val>= a:
                            a = val
            return a
        if player == "minimiser":
            b = 1000
            for i in range(table.shape[0]):
                for j in range(table.shape[1]):
                    TABLE = table.copy()
                    pos = table[i, j]
                    if pos == 0:
                        TABLE[i, j] = 2
                        val = self.minimax(TABLE,"maximiser",depth-1)
                        if val<=b:
                            b=val
            return b

    def best_pos(self,table,depth): # returns the best move to play among all possible moves
        a = -2
        Leqpos = []
        for i in range(table.shape[0]):
            for j in range(table.shape[1]):
                TABLE = table.copy()
                pos = table[i,j]
                if pos == 0:
                    TABLE[i, j] = 1
                    val = self.minimax(TABLE,depth=depth,player='minimiser')
                    if val == a:
                        Leqpos.append([i,j])
                    if val>a:
                        a=val
                        Leqpos = [[i,j]]
        print(Leqpos)
        POS = random.choice(Leqpos)
        return POS

