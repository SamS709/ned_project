from Morpion.AI.MorpionAI import *
from Morpion.AI.DQN import *

class AI(MorpionAI):

    def __init__(self):
        super().__init__()
        dim = [27,8,1]
        self.dqnP1 = DQN(reset=False, eps=0.95, P1='1', dim=dim, learning_rate=0.01)
        self.dqnP2 = DQN(reset=False, eps=0.95, P1='2', dim=dim, learning_rate=0.01)

    def convert(self, grid):
        GRID = grid.copy()
        GRID[GRID == 1] = 3
        GRID[GRID == 2] = 1
        GRID[GRID == 3] = 2
        return GRID

    def learn(self,P1,DX,Dy):
        if P1 =='1':
            self.dqnP1.batch_learn(DX,Dy)
        else:
            self.dqnP2.batch_learn(DX,Dy)

    def best_pos(self,table,P1):
        grid = super().table_to_grid(table)
        GRID = grid.copy()
        DX = np.array([[] for i in range(27)])  # store experiences (Experince Replay)
        Dy = np.array([])
        if P1 == '1':
            X = self.dqnP1.grid_to_X(GRID)
            GRID = self.dqnP1.next_grid(GRID).copy()
            y = self.dqnP1.output_y(GRID)
        else:
            GRID = self.convert(GRID)
            X = self.dqnP1.grid_to_X(GRID)
            GRID = self.dqnP2.next_grid(GRID).copy()
            y = self.dqnP2.output_y(GRID)
            GRID = self.convert(GRID)
        DX = np.concatenate((DX, X), axis=1)
        Dy = np.concatenate((Dy, y), axis=0)
        Dy = Dy.reshape((1, Dy.size))
        self.learn(P1,DX,Dy)
        pos = 0
        for i in range(len(grid)):
            if grid[i]!=GRID[i]:
                pos = i
        return super().posgrid_to_postable(pos)


