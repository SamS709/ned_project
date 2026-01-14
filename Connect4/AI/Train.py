from Connect4.AI.DQN import *
import numpy as np
import multiprocessing
from kivy.clock import mainthread

from global_vars import D_text_train

N_LEARNING = 0

class Train(Connect4):

    def __init__(self,model_name,info_label,scrollable_lablel,box,pb,reset=False,learning_rate=0.5e-3,discount_factor=0.98,softmax_=False,eps = 0.5):
        super().__init__()

        # loading two models that will play against each other (1: starts playing, 2: 2nd to play)
        self.dqnP1 = DQN(reset = reset, eps = eps, P1='1',learning_rate=learning_rate,gamma=discount_factor,model_name=model_name,softmax_=softmax_)
        self.dqnP2 = DQN(reset = reset, eps = eps, P1='2',learning_rate=learning_rate,gamma=discount_factor,model_name=model_name,softmax_=softmax_)

        self.info_label = info_label # informations displayed on the training menu
        self.model_name = model_name # the name of the model
        self.scrollable_lablel = scrollable_lablel # bottom right scollable label that displays the models in training
        self.box = box # the box that constains the informations of the training of the model
        self.pb = pb # the size of the training bar that displays the advencement of the training

    @mainthread
    def modif_label(self,i,N=1): # modifying ui of training menu
        if N==1:
            self.info_label.text = f"{D_text_train['model_name']} " + str(self.model_name) + f"\n{D_text_train['model_name']} " + str(i+1) + " / "+str(self.N)
            self.pb.value = (i+1)/self.N*self.pb.max
        if N==2:
            self.scrollable_lablel.layout.remove_widget(self.box)


    def P1vsP2(self,N): # simulating a game between the 2 DQN
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
                self.dqnP1.target.set_weights(self.dqnP1.model.get_weights()) # The target model updates every 10 games
                self.dqnP2.target.set_weights(self.dqnP2.model.get_weights())
                self.dqnP1.model.save(self.dqnP1.dir_path,overwrite=True) # For safety, we save the model every 10 gamee
                self.dqnP2.model.save(self.dqnP2.dir_path,overwrite=True)
        self.modif_label(i=N,N=2)


# as dqn1 and dqn2 both detect 1 as their pieces and 2 as opponent's, 
# dqn2 has to see the opposite of the grid seen by dqn1 :
# for dqn2: 1 is converted to 2, and 2 converted to 1
    def convert(self, grid): 
        GRID = grid.copy()
        GRID[GRID == 1] = 3
        GRID[GRID == 2] = 1
        GRID[GRID == 3] = 2
        return GRID


    def learn(self, P1, Dgrid, Dy): # learning from the game played in P1vsP2
        if P1 == '1':
            self.dqnP1.batch_learn(Dgrid, Dy)
        else:
            self.dqnP2.batch_learn(Dgrid, Dy)


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
    table = np.array([[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,0,1,1,0,0],
                      [0,1,1,2,1,0,0]])
    grid = play2.dqnP1.table_to_grid(table)
    print(play2.dqnP1.Q_value(grid))
