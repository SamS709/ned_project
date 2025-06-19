import numpy as np

class Connect4:

    def __init__(self):
        pass

    def win(self,grid): # tells if the state of the table a win for the robot
        grid = self.grid_to_table(grid)
        # Horizontal positions
        for i in range(grid.shape[0]):
            for j in range(4):
                h = grid[i,j] == 1 and grid[i,j + 1] == 1 and grid[i,j + 2] == 1 and grid[i,j + 3] == 1
                if h:
                    return True

        # Vertical positions
        for j in range(grid.shape[1]):
            for i in range(3):
                v = grid[i,j] == 1 and grid[i + 1,j] == 1 and grid[i + 2,j] == 1 and grid[i + 3,j] == 1
                if v:
                    return True

        # Diagonal positions
        for i in range(3):
            for j in range(4):
                d1 = grid[i,j] == 1 and grid[i + 1,j + 1] == 1 and grid[i + 2,j + 2] == 1 and grid[i + 3,j + 3] == 1
                d2 = grid[i,j + 3] == 1 and grid[i + 1,j + 2] == 1 and grid[i + 2,j + 1] == 1 and grid[i + 3,j] == 1
                if d1 or d2:
                    return True
        #Autre
        return False


    def lose(self,grid): # tells if the state of the table a lose for the robot
        grid = self.grid_to_table(grid)
        # Horizontal positions
        for i in range(grid.shape[0]):
            for j in range(4):
                h = grid[i,j] == 2 and grid[i,j + 1] == 2 and grid[i,j + 2] == 2 and grid[i,j + 3] == 2
                if h:
                    return True

        # Vertical positions
        for j in range(grid.shape[1]):
            for i in range(3):
                v = grid[i,j] == 2 and grid[i + 1,j] == 2 and grid[i + 2,j] == 2 and grid[i + 3,j] == 2
                if v:
                    return True

        # Diagonal positions
        for i in range(3):
            for j in range(4):
                d1 = grid[i,j] == 2 and grid[i + 1,j + 1] == 2 and grid[i + 2,j + 2] == 2 and grid[i + 3,j + 3] == 2
                d2 = grid[i,j + 3] == 2 and grid[i + 1,j + 2] == 2 and grid[i + 2,j + 1] == 2 and grid[i + 3,j] == 2
                if d1 or d2:
                    return True
        #Autre
        return False

    def tie(self,grid): # tells if the state of the table a tie
        a = True
        if self.win(grid) or self.lose(grid):
            a = False
        else:
            for i in range(len(grid)):
                if grid[i]==0:
                    a = False
        return a

    def end(self,grid): # tells if the state of the table an end
        if self.win(grid):
            return True
        if self.lose(grid):
            return True
        if self.tie(grid):
            return True
        return False

    def grid_to_table(self,grid): # convert the grid representation (1d array) to the table representation (2d array) of the game
        return grid.reshape((7,6)).T

    def table_to_grid(self,table): # reverses the operation made by grid_t_table so that table_to_grid(grid_to_table(grid))=grid
        table = table.T
        return np.array(table.reshape(1,table.size)).ravel()

    def free_pos(self, grid): # tells authorized moves in a given grid
        table = self.grid_to_table(grid)
        L = []
        Lpos = []
        for j in range(len(table[0])):
            i = 5
            while table[i,j] != 0 and i >= 0:
                i = i - 1
            if table[i,j] == 0:
                L.append([i, j])
        for i in range(len(L)):
            Lpos.append(L[i][0]+6*L[i][1])

        return np.array(Lpos)
    

    def avaible_pos_graphics(self,grid):
        table = self.grid_to_table(grid)
        if grid.shape[0]==6:
            table = grid.copy()
        L = []
        for j in range(table.shape[1]):
            i = 5
            while table[i, j] != 0 and i >= 0:
                i = i - 1
            if table[i, j] == 0:
                L.append([i, j])
        return L

    def count_lines(self,table,Nlines,n): # returns the number of lines having N consecutive pieces for player n

        if Nlines == 2:

            S2 = 0 #nombre de lignes à 2 éléms

            # Horizontal positions
            for i in range(table.shape[0]):
                for j in range(6):
                    h = table[i,j] == n and table[i,j+1] == n
                    if h:
                        S2 = S2 + 1

            # Vertical positions
            for j in range(table.shape[1]):
                for i in range(5):
                    v = table[i,j] == n and table[i+1,j] == n
                    if v:
                        S2 = S2 + 1

            #Diagonal positions
            for i in range(table.shape[0]-1):
                for j in range(table.shape[1]-1):
                    d1 = table[i,j] == n and table[i+1,j+1] == n
                    d2 = table[i+1,j] == n and table[i,j+1] == n
                    if d1:
                        S2 = S2+1
                    if d2:
                        S2 = S2+1
            return S2

        if Nlines == 3:

            S3 = 0  # nombre de lignes à 3 éléms

            # Horizontal positions
            for i in range(table.shape[0]):
                for j in range(table.shape[1]-2):
                    h = table[i,j] == n and table[i,j+1] == n and table[i,j+2] == n
                    if h:
                        S3 = S3 + 1

            # Vertical positions
            for j in range(table.shape[1]):
                for i in range(table.shape[0]-2):
                    v = table[i,j] == n and table[i+1,j] == n and table[i+2,j] == n
                    if v:
                        S3 = S3 + 1

            # Diagonal positions
            for i in range(table.shape[0] - 2):
                for j in range(table.shape[1] - 2):
                    d1 = table[i,j] == n and table[i+1,j+1] == n and table[i+2,j+2]==n
                    d2 = table[i+2,j] == n and table[i+1,j+1] == n and table[i,j+2]==n
                    if d1:
                        S3 = S3 + 1
                    if d2:
                        S3 = S3 + 1
            return S3

    def score(self,table): # returns the score of a given board (this is just a proposal to evaluate the board, a better one can surely be found)
        S1N3 = self.count_lines(table,Nlines=3,n=1)
        S1N2 = self.count_lines(table,Nlines=2,n=1) - 2*S1N3
        S2N3 = self.count_lines(table,Nlines=3,n=2)
        S2N2 = self.count_lines(table,Nlines=2,n=2) - 2*S2N3
        S = S1N3 + 0.3*S1N2 - (S2N3 + 0.3*S2N2)
        return S
    
    def posgrid_to_postable(self,pos):
        j = pos//6
        i = pos-6*j
        return[i,j]

if __name__=='__main__':
    connect4 = Connect4()
    table = np.array([[0,0,0,1,0,0,0],
                      [0,1,0,2,0,0,0],
                      [0,1,0,1,0,2,0],
                      [0,2,0,1,0,2,0],
                      [0,1,1,1,0,2,1],
                      [0,1,1,2,1,2,1]])
    grid=connect4.table_to_grid(table)
    print(grid)
    print(connect4.grid_to_table(grid))
    print(connect4.avaible_pos_graphics(table))
    print(connect4.lose(table))