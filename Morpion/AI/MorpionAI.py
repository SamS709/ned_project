import numpy as np

class MorpionAI:

    def __init__(self):
        pass

    def posgrid_to_postable(self,posgrid):
        if posgrid == 0:
            i,j=0,0
        if posgrid == 1:
            i,j=0,1
        if posgrid == 2:
            i,j=0,2
        if posgrid == 3:
            i,j=1,0
        if posgrid == 4:
            i,j=1,1
        if posgrid == 5:
            i,j=1,2
        if posgrid == 6:
            i,j=2,0
        if posgrid == 7:
            i,j=2,1
        if posgrid == 8:
            i,j=2,2
        return [i,j]


    def grid_to_table(self,grid):
        return grid.reshape((3,3))

    def table_to_grid(self,table):
        return np.array(table.reshape(1,table.size).ravel())

    def win(self,grid):
        if grid.shape == (3,3):
            grid = self.table_to_grid(grid)

        a = grid[0] == 1 and grid[1] == 1 and grid[2] == 1
        b = grid[3] == 1 and grid[4] == 1 and grid[5] == 1
        c = grid[6] == 1 and grid[7] == 1 and grid[8] == 1
        d = grid[0] == 1 and grid[3] == 1 and grid[6] == 1
        e = grid[1] == 1 and grid[4] == 1 and grid[7] == 1
        f = grid[2] == 1 and grid[5] == 1 and grid[8] == 1
        g = grid[0] == 1 and grid[4] == 1 and grid[8] == 1
        h = grid[2] == 1 and grid[4] == 1 and grid[6] == 1

        if a or b or c or d or e or f or g or h:
            return True

        return False

    def lose(self,grid):
        if grid.shape == (3,3):
            grid = self.table_to_grid(grid)

        a = grid[0] == 2 and grid[1] == 2 and grid[2] == 2
        b = grid[3] == 2 and grid[4] == 2 and grid[5] == 2
        c = grid[6] == 2 and grid[7] == 2 and grid[8] == 2
        d = grid[0] == 2 and grid[3] == 2 and grid[6] == 2
        e = grid[1] == 2 and grid[4] == 2 and grid[7] == 2
        f = grid[2] == 2 and grid[5] == 2 and grid[8] == 2
        g = grid[0] == 2 and grid[4] == 2 and grid[8] == 2
        h = grid[2] == 2 and grid[4] == 2 and grid[6] == 2

        if a or b or c or d or e or f or g or h:
            return True

        return False

    def tie(self,grid):

        if grid.shape == (3,3):
            grid = self.table_to_grid(grid)

        a = True

        if self.win(grid) or self.lose(grid):
            a = False
        else:
            for i in range(len(grid)):
                if grid[i]==0:
                    a = False

        return a

    def end(self,grid):
        if grid.shape == (3,3):
            self.table_to_grid(grid)
        if self.tie(grid) or self.win(grid) or self.lose(grid):
            return True
        return False

    def free_pos(self,grid):
        if grid.shape == (3,3):
            grid = self.table_to_grid(grid)
        return np.where(grid == 0)[0]



if __name__=='__main__':
    morpion = MorpionAI()
    table = morpion.grid_to_table(np.array([2,0,1,0,0,2,2,0,1]))
    print(table)
    grid = morpion.table_to_grid(table)
    print(grid)
    print(morpion.free_pos(table))