import random

import numpy as np

from Connect4.AI.DNN import *
from Connect4.AI.Connect4AI import *

class DQN(Connect4):

    def __init__(self,reset = True, eps = 0.8, P1='1',dim = [126,32,1],learning_rate = 0.05,alpha = 0.8,gamma=0.8):
        super().__init__()
        self.dnn1 = DNN(dim=dim,plot=False,reset=reset,network_number=P1+'1')
        self.dnn2 = DNN(dim=dim,plot=False,reset=reset,network_number=P1+'2')
        self.learning_rate = learning_rate
        self.eps = eps #epsilon greedy
        self.P1 = P1 # premier joueur
        self.alpha = alpha
        self.gamma=gamma


    def grad_desc(self,X_batch,y_batch): #batch_grid est de taille 9*m
        A_batch = self.dnn1.forward_propagation(X_batch)
        dW_batch,db_batch = self.dnn1.gradients(A_batch,y_batch)
        self.dnn1.update1(dW_batch,db_batch,self.learning_rate)
        self.dnn1.update_data()
        if self.dnn1.get_n_update()%100==0:
            self.dnn2.LW = self.dnn1.LW
            self.dnn2.Lb = self.dnn1.Lb
            self.dnn2.update_data()
            self.dnn2.init_params()

    def batch_learn(self, DX, Dy):
        n_obs = DX.shape[1]
        batch_size = 2
        XY = np.concatenate((DX, Dy), axis=0)
        rng = np.random.default_rng(seed=None)
        rng.shuffle(XY.T)
        for start in range(0, n_obs, batch_size):
            stop = start + batch_size
            X_batch, y_batch = XY[:-1, start:stop], XY[-1:, start:stop]
            self.grad_desc(X_batch,y_batch)


    def Q_value(self,grid):#prend en argument une grille et renvoie la valeur à partir du target network
        # reward
        if super().win(grid):
            val = 1
        elif super().lose(grid):
            val = 0
        elif super().tie(grid):
            val = 0.5
        # pas reward
        else:
            X = self.grid_to_X(grid)
            val = self.dnn2.forward_propagation(X)[-1]
            val = float(val)
        return val


    def output_y(self,grid): #prend en entrée l'état St+1 et renvoie la valeur de yt pour l'état St
        #reward
        if super().win(grid):
            y = 1
        elif super().lose(grid):
            y = 0
        elif super().tie(grid):
            y = 0.5
        #pas reward
        else:
            GRID = self.argmax(grid).copy()
            y = self.Q_value(GRID)
        return self.gamma*np.array([y])


    def grid_to_X(self, grid):
        X = np.array([])
        for num in grid:
            if num == 0:
                l = np.array([1,0,0])
            if num == 1:
                l = np.array([0,1,0])
            if num == 2:
                l = np.array([0,0,1])
            X=np.concatenate((X,l),axis = 0)
        return X.reshape((X.shape[0],1))

    def X_to_grid(self,X):
        grid = np.array([])
        for i in range(0,len(X),3):
            if X[i]==1 and X[i+1]==0 and X[i+2]==0:
                grid=np.concatenate((grid,np.array([0])),axis=0)
            elif X[i]==0 and X[i+1]==1 and X[i+2]==0:
                grid=np.concatenate((grid,np.array([1])),axis=0)
            else:
                grid=np.concatenate((grid,np.array([2])),axis=0)
        return grid


    def Q_value1(self,grid):
        X = self.grid_to_X(grid)
        val = self.dnn1.forward_propagation(X)[-1]
        return val


    def Q_value2(self,grid):
        X = self.grid_to_X(grid)
        val = self.dnn2.forward_propagation(X)[-1]
        return val


    def epsilon_greedy(self): #(1-eps) est la roba de jouer un coup random
        a = random.random() #appartient à [0,1[
        if a<self.eps:
            return False
        return True


    def argmax(self,grid): # détermine la grille maximale pour accessible à partir de grid en de basant sur le online network
        grid2 = grid.copy()
        if super().end(grid):
            return grid2
        n1 = np.count_nonzero(grid == 1)
        n2 = np.count_nonzero(grid == 2)
        L = super().free_pos(grid)
        A = -np.inf
        if self.P1 == '1':
            if n1<=n2:
                val = 1
            else:
                val = 2
        else:
            if n2<=n1:
                val = 2
            else:
                val = 1
        for pos in L:
            GRID = grid.copy()
            GRID[pos]=val
            if super().win(GRID):
                B=1
            elif super().lose(GRID):
                B=0
            elif super().tie(grid):
                B=0.5
            else:
                X = self.grid_to_X(GRID)
                B = float(self.dnn1.forward_propagation(X)[-1])
            if B>=A:
                A=B
                grid2 = GRID
        return grid2


    def next_grid(self,grid):
        n1 = np.count_nonzero(grid == 1)
        n2 = np.count_nonzero(grid == 2)
        GRID = grid.copy()
        if self.P1 == '1':
            if n1 <= n2:
                val = 1
            else:
                val = 2
        else:
            if n2 <= n1:
                val = 2
            else:
                val = 1
        if self.epsilon_greedy():
            L = super().free_pos(grid)
            if len(L)!=0:
                GRID[random.choice(L)]=val
        else:
            GRID = self.argmax(GRID).copy()
        return GRID


