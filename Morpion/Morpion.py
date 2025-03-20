import random

import numpy as np
import numpy.random as rd



class Morpion():

    def __init__(self):
        pass


    def win(self, table):

        a = table[0,0] == 1 and table[1,1] == 1 and table[2,2] == 1
        b = table[2,0] == 1 and table[1,1] == 1 and table[0,2] == 1
        c = table[0,0] == 1 and table[1,0] == 1 and table[2,0] == 1
        d = table[0,1] == 1 and table[1,1] == 1 and table[2,1] == 1
        e = table[0,2] == 1 and table[1,2] == 1 and table[2,2] == 1
        f = table[1,0] == 1 and table[1,1] == 1 and table[1,2] == 1
        g = table[2,0] == 1 and table[2,1] == 1 and table[2,2] == 1
        h = table[0,0] == 1 and table[0,1] == 1 and table[0,2] == 1
        if a or b or c or d or e or f or g or h:
            return True
        return False

    def lose(self,table):

        a = table[0,0] == 2 and table[1,1] == 2 and table[2,2] == 2
        b = table[2,0] == 2 and table[1,1] == 2 and table[0,2] == 2
        c = table[0,0] == 2 and table[1,0] == 2 and table[2,0] == 2
        d = table[0,1] == 2 and table[1,1] == 2 and table[2,1] == 2
        e = table[0,2] == 2 and table[1,2] == 2 and table[2,2] == 2
        f = table[1,0] == 2 and table[1,1] == 2 and table[1,2] == 2
        g = table[2,0] == 2 and table[2,1] == 2 and table[2,2] == 2
        h = table[0,0] == 2 and table[0,1] == 2 and table[0,2] == 2
        if a or b or c or d or e or f or g or h:
            return True
        return False


    def tie(self,table):
        a = True
        if self.win(table) or self.lose(table):
            return False
        else:
            for i in range(table.shape[0]):
                for j in range(table.shape[0]):
                    if table[i,j]==0:
                        a=False
        return a

    def end(self,table):
        if self.win(table) or self.lose(table) or self.tie(table):
            return True
        return False


