from Morpion.Morpion import *

class MinMax(Morpion):

    def __init__(self):
        super().__init__()

    def minimax(self,table,player,depth):

        #cas de base
        if self.win(table):
            return 1
        if self.lose(table):
            return -1
        if self.tie(table):
            return 0
        if depth == 0:
            return 0
        #récursion
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

    def best_pos(self,table,depth):
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

if __name__=='__main__':
    table = np.array([[2,0,2],[0,1,0],[0,0,0]])
    minmax = MinMax()
    minmax.best_pos(table,7)