from Connect4.AI.DQN import *
from tqdm import tqdm
import numpy as np
import multiprocessing
from kivy.clock import mainthread

N_LEARNING = 0

class Train(Connect4):

    def __init__(self,model_name,info_label,scrollable_lablel,box,reset=False,learning_rate=0.5e-3,discount_factor=0.98,softmax_=False,eps = 0.5):
        super().__init__()
        self.dqnP1 = DQN(reset = reset, eps = eps, P1='1',learning_rate=learning_rate,gamma=discount_factor,model_name=model_name,softmax_=softmax_)
        self.dqnP2 = DQN(reset = reset, eps = eps, P1='2',learning_rate=learning_rate,gamma=discount_factor,model_name=model_name,softmax_=softmax_)
        self.info_label = info_label
        self.model_name = model_name
        self.scrollable_lablel = scrollable_lablel
        self.box = box

    @mainthread
    def modif_label(self,i,N=1):
        if N==1:
            self.info_label.text = "Nom du modèle: " + str(self.model_name) + "\n\nNombre d'epoques: " + str(i+1) + " / "+str(self.N)
        if N==2:
            self.scrollable_lablel.layout.remove_widget(self.box)


    def P1vsP2(self,N):
        self.N=N
        for i in range(N):
            self.modif_label(i,N=1)
            grid = np.array([0 for i in range(42)])
            new_grid = grid.copy()
            DX1 = np.array([])
            Dy1 = np.array([])
            DX2 = DX1.copy()
            Dy2 = Dy1.copy()
            while not super().end(grid):
                grid = new_grid.copy()
                DX1 = np.concatenate((DX1,grid),axis = 0)
                new_grid = self.dqnP1.next_grid(grid).copy()
                y1 = self.dqnP1.output_y(new_grid)
                Dy1 = np.concatenate((Dy1,y1),axis = 0)
                grid = self.convert(grid)
                new_grid = self.convert(new_grid)
                DX2 = np.concatenate((DX2,grid),axis = 0)
                y2 = self.dqnP2.output_y(new_grid)
                Dy2 = np.concatenate((Dy2,y2),axis = 0)
                if not super().end(grid):
                    grid = new_grid.copy()
                    DX2 = np.concatenate((DX2, grid), axis=0)
                    new_grid = self.dqnP2.next_grid(grid).copy()
                    y2 = self.dqnP2.output_y(new_grid)
                    Dy2 = np.concatenate((Dy2, y2), axis=0)
                    grid = self.convert(grid)
                    new_grid = self.convert(new_grid)
                    #print('grid\n',super().grid_to_table(grid))
                    #print('NEWgrid\n', super().grid_to_table(new_grid))
                    DX1 = np.concatenate((DX1, grid), axis=0)
                    y1 = self.dqnP1.output_y(new_grid)
                    Dy1 = np.concatenate((Dy1, y1), axis=0)
            DX1 = DX1.reshape(int(len(DX1)/42),42)
            DX2 = DX2.reshape(int(len(DX2)/42),42)
            self.learn('1', DX1, Dy1)
            self.learn('2', DX2, Dy2)
            if i % 10 == 0:
                print(1)
                self.dqnP1.target.set_weights(self.dqnP1.model.get_weights()) # Le model target s'acualise seulement tous les 10 parties
                self.dqnP2.target.set_weights(self.dqnP2.model.get_weights())
                self.dqnP1.model.save(self.dqnP1.model_name+"1",overwrite=True) # par sécurité, on enregistre lemodel une fois toutes les 10 paries
                self.dqnP2.model.save(self.dqnP2.model_name+"2",overwrite=True)
        self.modif_label(i=N,N=2)



    def convert(self, grid):
        GRID = grid.copy()
        GRID[GRID == 1] = 3
        GRID[GRID == 2] = 1
        GRID[GRID == 3] = 2
        return GRID


    def learn(self, P1, Dgrid, Dy):
        if P1 == '1':
            self.dqnP1.batch_learn(Dgrid, Dy)
        else:
            self.dqnP2.batch_learn(Dgrid, Dy)

    def play(self,grid,P1):
        if P1=='1':
            grid = self.dqnP1.next_grid(grid)
            y = self.dqnP1.output_y(grid)
        else:
            self.convert(grid)
            grid = self.dqnP2.next_grid(grid)
            y = self.dqnP2.output_y(grid)
            self.convert(grid)
        return grid,y


if __name__=='__main__':
    #play1 = TF_Play(reset = False, eps=0.5, model_name="my_simple_model",softmax_=True)
    play2 = Train(reset = False, eps=0.5, model_name="my_linear_model",softmax_=False)
    play = play2
    """for i in range(1):
        play.learn_multiple(10)"""
    play.P1vsP2(11)
    play.dqnP1.model.summary()
    grid = np.array([0 for i in range(42)])
    L = play.free_pos(grid)
    D = {}
    for i in range(len(L)):
        new_grid = grid.copy()
        new_grid[L[i]] = 1
        val = play.dqnP1.Q_value1(new_grid)
        table = play.grid_to_table(new_grid)
        D[float(val)] = table
    ind = max(D.keys())
    print(D)
    print(D[ind], ind)
    next_grid = play.dqnP1.next_grid(grid)
    print(play.grid_to_table(next_grid))
    next_grid2,y = play.play(grid,'1')
    print(play.grid_to_table(next_grid2),y)
    table = np.array([[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,0,1,1,0,0],
                      [0,1,1,2,1,0,0]])
    grid = play2.dqnP1.table_to_grid(table)
    print(play2.dqnP1.Q_value(grid))
