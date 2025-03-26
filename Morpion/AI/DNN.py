import numpy as np
from matplotlib import pyplot as plt
from numpy.ma.core import repeat
from select import select
from sklearn.datasets import make_circles
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import sqlite3

'''
DNN permet de créer un réseau de neurone
Pour créer plusieurs réseaux de neurones, il faut s'assurer que leur 'network_number' soit distinct
Il faudra faire une classe Creation_de_neurones dédié à la création de plusieurs neuronse qui empêche des erreurs liées à des bases de données déjà existantes
'''


class DNN:
    def __init__(self,dim,plot=True,learning_rate=0,network_number=1,reset = True):

        self.conn = sqlite3.connect('Morpion/AI/params.db')
        self.cur = self.conn.cursor()

        self.table_W = 'W'+str(network_number)
        self.table_b = 'b'+str(network_number)
        self.table_n_update = 'n_update'+str(network_number)

        self.dim = dim

        self.learning_rate = learning_rate
        self.plot = plot

        if reset == True:
            self.reset_data()
        else:
            self.init_params()


        self.n_couches = len(self.LW)

    def update_data(self): #met à jour la valeur des paramètres en base de donnée à partir de self.LW et self.Lb

        update_command = f"""UPDATE {self.table_W} SET value = ? WHERE id = ?"""
        L1W = [T.ravel() for T in self.LW]
        W = np.concatenate(L1W, axis=0)
        W = W.ravel()
        n = len(W)
        indW = np.array([i for i in range(n)])
        W = W.reshape((W.shape[0], 1))
        indW = indW.reshape((indW.shape[0], 1))
        LW = np.concatenate((W,indW), axis=1)
        self.cur.executemany(update_command,LW)

        update_command = f"""UPDATE {self.table_b} SET value = ? WHERE id = ?"""
        L1b = [T.ravel() for T in self.Lb]
        b = np.concatenate(L1b, axis=0)
        b = b.ravel()
        n = len(b)
        indb = np.array([i for i in range(n)])
        b = b.reshape((b.shape[0], 1))
        indb = indb.reshape((indb.shape[0], 1))
        Lb = np.concatenate((b,indb), axis=1)
        self.cur.executemany(update_command,Lb)

        n_update = self.get_n_update()
        n_update +=1
        L_n_update = [[n_update,0]]
        update_command = f"""UPDATE {self.table_n_update} SET value = ? WHERE id = ?"""
        self.cur.executemany(update_command,L_n_update)

        self.conn.commit()

    def get_n_update(self):
        select_command_W = f"SELECT value FROM {self.table_n_update} WHERE id = 0 "
        self.cur.execute(select_command_W)
        n_update = self.cur.fetchone()[0]
        return n_update

    def init_params(self):

        # On récupère les valeurs des poids W dans la liste des tableaux W self.LW
        select_command_W = f"SELECT value FROM {self.table_W} "
        self.cur.execute(select_command_W)
        LW = np.array(self.cur.fetchall())
        LW=LW.reshape(1,LW.shape[0]).ravel()
        s = 0
        Lind = []
        for i in range(1,len(self.dim)):
            p = self.dim[i-1]*self.dim[i]
            Lind.append(s+p)
            s += p
        self.LW = np.split(LW,Lind)
        self.LW.pop()
        for i in range(len(self.LW)):
            self.LW[i]=self.LW[i].reshape(self.dim[i+1],self.dim[i])

        # On récupère les valeurs des décalages b dans la liste des tableaux b self.Lb
        select_command_b = f"SELECT value FROM {self.table_b} "
        self.cur.execute(select_command_b)
        Lb = np.array(self.cur.fetchall())
        Lb = Lb.reshape(1, Lb.shape[0]).ravel()
        s = 0
        Lind = []
        for i in range(1, len(self.dim)):
            p = self.dim[i]
            Lind.append(s + p)
            s += p
        self.Lb = np.split(Lb, Lind)
        self.Lb.pop()
        for i in range(len(self.Lb)):
            self.Lb[i] = self.Lb[i].reshape(self.dim[i + 1], 1)


        return self.LW,self.Lb


    def reset_data(self):
        #création des commandes
        delete_command_W = f"DROP TABLE IF EXISTS {self.table_W}"
        delete_command_b = f"DROP TABLE IF EXISTS {self.table_b}"
        delete_command_n_update = f"DROP TABLE IF EXISTS {self.table_n_update}"
        create_command_W = f"""CREATE TABLE IF NOT EXISTS {self.table_W} (id INTEGER PRIMARY KEY,value REAL)"""
        create_command_b = f"""CREATE TABLE IF NOT EXISTS {self.table_b} (id INTEGER PRIMARY KEY,value REAL)"""
        create_command_n_update = f"""CREATE TABLE IF NOT EXISTS {self.table_n_update} (id INTEGER PRIMARY KEY,value REAL)"""
        insert_command_W = f"""INSERT INTO {self.table_W} (id, value) VALUES (:id, :value)"""
        insert_command_b = f"""INSERT INTO {self.table_b} (id, value) VALUES (:id, :value)"""
        insert_command_n_update = f"""INSERT INTO {self.table_n_update} (id, value) VALUES (0, 0)"""
        # exécution des commandes de suppression puis céation des tables de paramètres W et b
        self.cur.execute(delete_command_W)
        self.cur.execute(delete_command_b)
        self.cur.execute(delete_command_n_update)
        self.cur.execute(create_command_W)
        self.cur.execute(create_command_b)
        self.cur.execute(create_command_n_update)
        #création des listes des paramètres W et b
        self.LW = []
        self.Lb = []
        #création des listes de dictionnaires pour le remplissage des tables
        LW = []
        Lb = []
        # remplissage des listes des paramètres par les nombres générés aléatoirements (suivant une loi normale centrée en 0)
        for i in range(len(self.dim)-1):
            self.LW.append(np.random.randn(self.dim[i+1],self.dim[i]))
            self.Lb.append(np.random.randn(self.dim[i+1],1))
        # remplissage de LW
        s = 0
        for i in range(len(self.LW)):
            if i!=0:
                s = s + len(self.LW[i-1].ravel()) #longueur de tous les W précédents
            Wflat = self.LW[i].ravel()
            for j in range(len(Wflat)):
                LW.append({'id':j+s,'value':Wflat[j]})
        #remplissage de Lb
        s = 0
        for i in range(len(self.Lb)):
            if i !=0:
                s = s + len(self.Lb[i - 1].ravel())  # longueur de tous les b précédents
            bflat = self.Lb[i].ravel()
            for j in range(len(bflat)):
                Lb.append({'id':j+s,'value':bflat[j]})

        # On défini n_update le nombre de fois où on a update la table

        self.cur.executemany(insert_command_W, LW)
        self.cur.executemany(insert_command_b, Lb)
        self.cur.execute(insert_command_n_update)
        self.conn.commit()

    def model(self,X, W, b):
        Z = W.dot(X) +b
        A = 1 / (1 + np.exp(-Z))
        return A

    def log_loss(self,A, y):
        eps = 1e-15
        return 1 / len(y) * np.sum(-y * np.log(A+eps) - (1 - y) * np.log(1 - A+eps))

    def gradients(self,A,y): #A[0] = X et n est le nombre de couches du réseau de neurones
        m = y.shape[1]
        dW  = []
        db = []
        i = self.n_couches
        dZ = A[i]-y
        while i > 1:
            dW.append(1 / m * dZ.dot(A[i-1].T))
            db.append(1 / m * np.sum(dZ,axis = 1,keepdims=True))
            dZ = (self.LW[i-1].T).dot(dZ)*A[i-1]*(1-A[i-1])
            i = i-1
        dW.append(1 / m * dZ.dot(A[0].T))
        db.append(1 / m * np.sum(dZ, axis=1, keepdims=True))
        dW.reverse()
        db.reverse()
        return (dW, db)

    def update1(self,dW, db, learning_rate):
        for i in range(self.n_couches):
            self.LW[i] = self.LW[i] - learning_rate * dW[i]
            self.Lb[i] = self.Lb[i] - learning_rate * db[i]

    def forward_propagation(self,X):
        A = []
        A.append(X)
        for i in range(self.n_couches):
            A.append(self.model(A[i], self.LW[i], self.Lb[i]))
        return A

    def predict(self,X):
        A = self.forward_propagation(X)
        return A[-1] >= 0.5

    def artificial_neuron_stochastic(self,Xtrain,ytrain, Xtest=[], ytest=[], n_iter=1000,batch_size = 16):
        # initialisation W, Lb
        n_obs = Xtrain.shape[1]
        LZ = []
        if self.plot == True:
            res = 200
            x0 = np.linspace(Xtrain[0, :].min(), Xtrain[0, :].max(), res)
            x1 = np.linspace(Xtrain[1, :].min(), Xtrain[1, :].max(), res)
            X0, X1 = np.meshgrid(x0, x1)
            XX = np.vstack((X0.ravel(), X1.ravel()))
            train_loss = []
            test_loss = []
            train_accuracy = []
            test_accuracy = []
        for i in tqdm(range(n_iter)):
            XY = np.concatenate((Xtrain, ytrain), axis=0)
            rng = np.random.default_rng(seed=None)
            rng.shuffle(XY.T)
            for start in range(0, n_obs, batch_size):  # on fait des pas de la taille du batch
                stop = start + batch_size
                X_batch, Y_batch = XY[:-1, start:stop], XY[-1:, start:stop]
                A_batch = self.forward_propagation(X_batch)
                dW, db = self.gradients(A_batch, Y_batch)
                if self.learning_rate==0:
                    self.update1(dW, db, 1/(i+1)**(1/3))
                else:
                    self.update1(dW, db, self.learning_rate)
            if self.plot == True:
                if i % 10 == 0:
                    Atrain = self.forward_propagation(Xtrain)
                    Z = self.predict(XX)
                    Z = Z.reshape((res, res))
                    LZ.append(Z)
                    train_loss.append(self.log_loss(Atrain[-1], ytrain))
                    ytrain_pred = self.predict(Xtrain)
                    train_accuracy.append(accuracy_score(ytrain.flatten(), ytrain_pred.flatten()))
                    if len(Xtest) != 0:
                        Atest = self.forward_propagation(Xtest)
                        test_loss.append(self.log_loss(Atest[-1], ytest))
                        ytest_pred = self.predict(Xtest)
                        test_accuracy.append(accuracy_score(ytest.flatten(), ytest_pred.flatten()))

        if self.plot == True:
            plt.figure('Loss Function')
            plt.plot(train_loss, label='Train Loss')
            plt.plot(test_loss, label='Test Loss')
            plt.legend()
            plt.figure('Accuracy')
            plt.plot(train_accuracy, label='Train Accuracy')
            plt.plot(test_accuracy, label='Test Accuracy')
            plt.legend()
            plt.show()
        self.update_data()
        return LZ

if __name__=='__main__':
    '''
    Xtrain = np.array([[1,2,3],
                       [4,5,6]])/6
    ytrain = np.array([1,0,0])
    ytrain = ytrain.reshape(1,ytrain.shape[0])
    print('dimension de X:',Xtrain.shape)
    print('dimension de y:',ytrain.shape)
    dim = [2,4,5,6,1]
    '''
    X1, y1 = make_circles(n_samples=200, noise=0.1, factor=0.7, random_state=35)
    X2, y2 = make_circles(n_samples=200, noise=0.1, factor=0.7, random_state=15)
    X3, y3 = make_circles(n_samples=200, noise=0.1, factor=0.7, random_state=25)
    X2 = X2 + 3
    X3[:, 1] = X3[:, 1] + 4
    X = np.concatenate((X1, X2, X3))
    y = np.concatenate((y1, y2, y3))
    dim = [2, 32, 1]
    X = X.T
    y = y.reshape((1, y.shape[0]))
    dnn = DNN(2,1,dim,plot=True,reset=True,learning_rate=0.001)
    dnn.artificial_neuron_stochastic(X,y,n_iter=3000)

