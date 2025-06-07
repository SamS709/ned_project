import random
import os
from tensorflow import keras
import tensorflow.keras.backend as K
import tensorflow

from Connect4.Connect4 import *
import tensorflow as tf

#model = dnn1
#target = dnn2

class DQN(Connect4):

    def __init__(self,model_name,softmax_,learning_rate=1e-2,gamma=1e-1,eps = 0.9,P1="1",reset = False):

        super().__init__()
        self.eps = eps
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.P1 = P1
        self.model_name = model_name
        self.dir_path = os.getcwd()+'\Connect4\AI\models'+f'\{self.model_name}'+self.P1

        try:
            self.load_model()
        except:
            self.create_model()

        self.end_score = [1,-1,0]
        if softmax_:
            self.end_score = [1,0,0.5]

    def create_model(self,n_layers=2,n_neurons=32):
        input_ = keras.layers.Input(shape=(42))
        one_hot = keras.layers.Lambda(lambda x : K.one_hot(K.cast(x, 'int64'), 3))(input_)
        flatten = keras.layers.Flatten(input_shape=(42, 3))(one_hot)
        hidden1 = keras.layers.Dense(n_neurons,kernel_initializer="he_normal", use_bias=False)(flatten)
        BN1 = tf.keras.layers.BatchNormalization()(hidden1)
        relu1 = tf.keras.layers.Activation("relu")(BN1)
        dropout =keras.layers.Dropout(rate=0.2)(relu1)
        for i in range(n_layers-2):
            hidden = keras.layers.Dense(n_neurons,kernel_initializer="he_normal", use_bias=False)(dropout)
            BN = tf.keras.layers.BatchNormalization()(hidden)
            relu = tf.keras.layers.Activation("relu")(BN)
            dropout =keras.layers.Dropout(rate=0.2)(relu)
        hidden2 = keras.layers.Dense(n_neurons,kernel_initializer="he_normal", use_bias=False)(dropout)
        BN2 = tf.keras.layers.BatchNormalization()(hidden2)
        relu2 = tf.keras.layers.Activation("relu")(BN2)
        output_ = keras.layers.Dense(1, activation="linear")(relu2)
        self.model = keras.models.Model(inputs=[input_], outputs=[output_])
        self.model.save(self.dir_path,overwrite=True)
        self.target = keras.models.load_model(self.dir_path)

    def load_model(self):
        self.model = keras.models.load_model(self.dir_path)
        self.target = keras.models.load_model(self.dir_path)
        self.target.set_weights(self.model.get_weights())


    def epsilon_greedy(self): #(1-eps) est la roba de jouer un coup random
        a = np.random.rand() #appartient à [0,1[
        if a<self.eps:
            return False
        return True

    def argmax(self,grid,return_pos=False): # détermine la grille maximale pour accessible à partir de grid en de basant sur le online network, if return_pos==True: it returns the best position
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
                B=self.end_score[0]
            elif super().lose(GRID):
                B=self.end_score[1]
            elif super().tie(GRID):
                B=self.end_score[2]
            else:
                B = float(self.model((GRID.reshape(1,42))))
            if B>=A:
                A=B
                grid2 = GRID
                pos2 = pos
        if return_pos:
            return pos2
        return grid2

    def best_pos(self,table):
        grid = super().table_to_grid(table)
        pos_grid = self.argmax(grid,return_pos=True)
        pos_table = super().posgrid_to_postable(pos_grid)
        return pos_table

    def batch_learn(self, DX, Dy):
        n_obs = DX.shape[1]
        batch_size = 2
        Dy_ = np.reshape(Dy, (len(Dy), 1))
        Xy = np.concatenate((DX, Dy_), axis=1)
        rng = np.random.default_rng(seed=None)
        rng.shuffle(Xy)
        for start in range(0, n_obs, batch_size):
            stop = start + batch_size
            X_batch, y_batch = Xy[start:stop, :-1], Xy[start:stop, -1:]
            self.grad_desc(X_batch,y_batch)

    def grad_desc(self,X_batch,y_batch): #batch_grid est de taille 9*m
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        loss_fn = tf.keras.losses.mean_squared_error
        with tf.GradientTape() as tape:
            Q_val = self.model(X_batch)
            loss = tf.reduce_mean(loss_fn(Q_val,y_batch))
        grads = tape.gradient(loss,self.model.trainable_variables)
        optimizer.apply_gradients(zip(grads,self.model.trainable_variables))
        '''if self.dnn1.get_n_update()%100==0:
            self.dnn2.LW = self.dnn1.LW
            self.dnn2.Lb = self.dnn1.Lb
            self.dnn2.update_data()
            self.dnn2.init_params()'''

    def output_y(self,grid): #prend en entrée l'état St+1 et renvoie la valeur de yt pour l'état St
        #end of the game
        r = 0
        if super().win(grid):
            next_q = self.end_score[0]
        elif super().lose(grid):
            next_q = self.end_score[1]
        elif super().tie(grid):
            next_q = self.end_score[2]
        #else
        else:
            GRID = self.argmax(grid).copy()
            table = self.grid_to_table(grid)
            #r = self.reward(table)
            next_q = self.Q_value(GRID)
        return r + self.gamma*np.array([next_q])

    def Q_value(self,grid):#prend en argument une grille et renvoie la valeur à partir du target network
        # reward
        if super().win(grid):
            val = self.end_score[0]
        elif super().lose(grid):
            val = self.end_score[1]
        elif super().tie(grid):
            val = self.end_score[2]
        # pas reward
        else:
            val = self.target(grid.reshape(1,42))
            val = float(val)
        return val

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

    def Q_value2(self,grid):
        val = float(self.target(grid.reshape((1,42))))
        return val

    def Q_value1(self,grid):
        val = float(self.model(grid.reshape((1,42))))
        return val

    def count_lines(self,table,Nlines,n): # renvoie le nombre de lignes ayant Npions consécutifs pour le jour n

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

    def reward(self,table):
        S1N3 = self.count_lines(table,Nlines=3,n=1)
        S1N2 = self.count_lines(table,Nlines=2,n=1) - 2*S1N3
        S2N3 = self.count_lines(table,Nlines=3,n=2)
        S2N2 = self.count_lines(table,Nlines=2,n=2) - 2*S2N3
        S = S1N3 + 0.3*S1N2 - (S2N3 + 0.3*S2N2)
        reward = np.tanh(S/2)/2
        return reward

"""for i in range(10):
    DQN(reset=False,model_name="model"+str(i),softmax_=False,P1="1")
    DQN(reset=False,model_name="model"+str(i),softmax_=False,P1="2")"""

DQN(reset=True,model_name="Expert",softmax_=False,P1="1")

"""    table = np.array([[0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [2,1,1,2,1,0,0],
                        [2,1,1,2,1,0,0],
                        [2,1,1,2,1,0,0]])
    grid = dqn1.table_to_grid(table)
    print(dqn1.Q_value(grid))
    print(dqn1.reward(table))
    #dqn1.grad_desc(DX,Dy)"""
