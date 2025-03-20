import numpy as np

class Connect4:

    def __init__(self):
        pass

    def win(self,grid):
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


    def lose(self,grid):
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

    def tie(self,grid):
        a = True
        if self.win(grid) or self.lose(grid):
            a = False
        else:
            for i in range(len(grid)):
                if grid[i]==0:
                    a = False
        return a

    def end(self,grid):
        if self.win(grid):
            return True
        if self.lose(grid):
            return True
        if self.tie(grid):
            return True
        return False

    def grid_to_table(self,grid):
        return grid.reshape((7,6)).T

    def table_to_grid(self,table):
        table = table.T
        return np.array(table.reshape(1,table.size)).ravel()

    def free_pos(self, grid):
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
        L = []
        for j in range(len(table[0])):
            i = 5
            while table[i, j] != 0 and i >= 0:
                i = i - 1
            if table[i, j] == 0:
                L.append([i, j])
        return L

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
    print(connect4.free_pos(grid))
    print(connect4.lose(grid))
    print(connect4.posgrid_to_postable(20))
