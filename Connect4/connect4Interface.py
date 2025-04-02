from kivy.lang import Builder
from Connect4.Minimax.MinMax import *
from kivy.app import App
from graphics import var1
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget
from Connect4.AI.AI import *

from Connect4.Robot import *



Builder.load_file('Connect4/connect4Interface.kv')



class Connect4Grille(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None,None #taille de la grille
        self.LR = []
        self.LC = [[]for j in range(7)]
        with self.canvas.before:
            Color(0, 0, 1, 0.9)
            for i in range(7): #création d'un fond blau pour chaque bouton => grand rectangle bleu qui fait toute la page
                self.LR.append(Rectangle())
            Color(182/256,229/265,246/256,1)
            for i in range(6): #création des cercles de couleur noir par dessus le rectangle bleu pour faire des 'trous' dans la grille
                for j in range(7):
                    self.LC[i].append(Ellipse(pos=(100,100),size=(50,50)))




class Connect4Items(BoxLayout):

    def __init__(self, gameMode='1P', **kwargs):
        super(Connect4Items, self).__init__(**kwargs)
        self.minimax = MinMax()
        self.depth = 3 #niveau de jeu
        self.P1 = '1' #joueur qui commence
        self.player = '1' # prend la valeur 'J' ou 'R' en fonction de la couleur du jeton
        self.grille = Connect4Grille() # on instancie une nouvelle grille de jeu
        self.add_widget(self.grille) #On affiche la grille
        self.table = np.array([[0 for j in range(7)] for i in range(6)]) # on créé une grille de jeu 'théorique' qui permet de gérer ce qui se passe en back
        self.init_C() #Initialisation des pions qui vont s'afficher dans la grille
        ''' self.label = Label(text='coucou', pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.label)'''

    def init_C(self,*args):
        self.LwCJ = [[] for j in range(7)]
        self.LwCR = [[] for j in range(7)]
        self.LCJ = [[] for j in range(7)]
        self.LCR = [[] for j in range(7)]
        for i in range(6):
            for j in range(7):
                self.LwCJ[i].append(Widget())
                self.LwCR[i].append(Widget())
        for i in range(6):
            for j in range(7):
                with self.LwCJ[i][j].canvas:
                    Color(1, 1, 0,1)
                    self.LCJ[i].append(Ellipse(pos=(100,100),size=(50,50)))
                with self.LwCR[i][j].canvas:
                    Color(1, 0, 0, 1)
                    self.LCR[i].append(Ellipse(pos=(100, 100), size=(50, 50)))


    def on_size(self, *args):

        W,H= self.width, self.height
        w,h = W/7, 7.5*H/8
        hh = h/6
        R = min(2 * w / 3, h / 7)

        #self.label.pos = W/2,H/2

        self.grille.width, self.grille.height =W,H

        for i in range(7):
            self.grille.LR[i].pos = i * w,0
            self.grille.LR[i].size = w,h

        for i in range(6):
            for j in range(7):
                self.grille.LC[i][j].size = R,R
                self.LCJ[i][j].size = R, R
                self.LCR[i][j].size = R, R
                self.grille.LC[i][j].pos = j * w + w / 2 - R / 2, i * hh + hh / 2 - R / 2
                self.LCJ[5-i][j].pos = j * w + w / 2 - R / 2, i * hh + hh / 2 - R / 2
                self.LCR[5-i][j].pos = j * w + w / 2 - R / 2, i * hh + hh / 2 - R / 2

class Connect4Game(BoxLayout):

    delay = NumericProperty(1/33)
    colors = ListProperty([100/256,100/256,100/256,1])
    color1 = ListProperty([100/256,100/256,100/256,1])
    color2 = ListProperty([0,0,1,1])
    colorsLine = ListProperty([0,0,0,1])
    colorLine1 = ListProperty([0,0,0,1])
    colorLine2 = ListProperty([1,1,1,1])


    def __init__(self,depth=3, **kwargs):
        self.first_end = False #indique si le robot détecte la fin ou pas: utile pour le feu de fin : si self.end == True et self.first_end == False alors on célèbre le fin. Si self.end == False : on indique q'il faut retirer les pieces
        super().__init__(**kwargs)
        self.minmax = MinMax()
        self.connect4 = Connect4()
        self.table = np.array([[0 for j in range(7)] for i in range(6)])
        self.depth = depth
        self.ai = AI()


    def on_kv_post(self, base_widget):
        self.game = self.ids.G

    def animationFire(self, state):
        if state == 'end':
            animate = Animation(image_num=3, duration=0)
            for i in range(3):
                animate += Animation(image_num=3,duration=0)
                animate += Animation(image_num=3,duration=0.15)
                animate += Animation(image_num=2,duration=0)
                animate += Animation(image_num=2,duration=0.15)
                animate += Animation(image_num=1,duration=0)
                animate += Animation(image_num=1, duration=0.7)
            for i in range(3):
                animate += Animation(image_num=0, duration=0)
                animate += Animation(image_num=0, duration=0.2)
                animate += Animation(image_num=4, duration=0)
                animate += Animation(image_num=4, duration=0.7)
            animate.start(self.ids.feuLose)
        if state == 'redFire':
            animate = Animation(image_num=0, duration=0)
            for i in range(3):
                animate += Animation(image_num=3, duration=0)
                animate += Animation(image_num=3, duration=0.8)
                animate += Animation(image_num=0, duration=0)
                animate += Animation(image_num=0, duration=0.2)
            animate.start(self.ids.feuLose)

    def feu(self,i):
            animate = Animation(image_num=i,d=0)
            animate.start(self.ids.feuLose)

    def robot_animation(self,i):
        n_images = 161
        if i == 1:
            animate = Animation(image_num=0, duration=0)
            animate.start(self.ids.robot)
        if i == 2:
            animate = Animation(image_num=1, duration=0)
            animate.start(self.ids.robot)

    def pressB(self,instance):
        self.robot1 = Robot()
        self.table = self.robot1.modif_table()
        grid = self.connect4.table_to_grid(self.table)
        if instance.text == ' Press when you \nfinished your move' or instance.text == 'Enleve les pieces\npour recommencer':
            if not self.connect4.end(grid):
                self.ids.G1.source = 'Morpion/gifs/bras-robotique-gros.gif'
                self.delay = 1/33
                self.first_end = False
                instance.text = "Ned is playing..."
                self.colors = self.color2
                self.colorsLine = self.colorLine2
                instance.color = [1, 1, 1, 1]
                self.delay = 1 / 30
                for i in range(self.table.shape[0]):
                    for j in range(self.table.shape[1]):
                        self.game.remove_widget(self.game.LwCR[i][j])
                        self.game.remove_widget(self.game.LwCJ[i][j])
                        if self.table[i, j] == 1:
                            self.game.add_widget(self.game.LwCR[i][j])
                        if self.table[i, j] == 2:
                            self.game.add_widget(self.game.LwCJ[i][j])
                self.ids.feuLose.source = "Connect4/image/feu3.png"
            else:
                for i in range(self.table.shape[0]):
                    for j in range(self.table.shape[1]):
                        self.game.remove_widget(self.game.LwCR[i][j])
                        self.game.remove_widget(self.game.LwCJ[i][j])
                        if self.table[i, j] == 1:
                            self.game.add_widget(self.game.LwCR[i][j])
                        if self.table[i, j] == 2:
                            self.game.add_widget(self.game.LwCJ[i][j])
                print('AAAA')
                self.colors = [185/256,0,0,1]
                self.ids.G1.anim_loop = 1
                instance.text = 'Enleve les pieces\npour recommencer'
                instance.color = [1,1,1,1]
                self.colorsLine = [1,1,1,1]



    def releaseB(self,instance):
        self.ids.feuLose.source = "Connect4/image/feu%d.png" % int(self.ids.feuLose.image_num)
        mode = var1.MODE
        level = var1.LEVEL
        grid = self.connect4.table_to_grid(self.table)
        n1 = np.count_nonzero(self.table == 1)
        n2 = np.count_nonzero(self.table == 2)
        if n1>= n2: # On détermine quel réseau de neurone utiliser
            self.P1 = '1'
        else:
            self.P1 = '2'
        if instance.text == 'Ned is playing...':
            if not self.connect4.end(grid):
                if mode == 'minimax':
                    if level == 'novice':
                        self.depth = 1
                    if level == 'debutant':
                        self.depth = 2
                    if level == 'intermediaire':
                        self.depth = 3
                    if level == 'expert':
                        self.depth = 4
                    pos = self.minmax.best_pos(self.table,self.depth)
                else:
                    pos = self.ai.best_pos(self.table,self.P1)
                    pass
                p,q = pos[0],pos[1]
                self.table[p,q]=1
                self.robot1.place(pos[1])
                self.game.add_widget(self.game.LwCR[p][q])
                instance.text = ' Press when you \nfinished your move'
                self.colors = self.color1
                self.colorsLine = self.colorLine1
                instance.color = [1,1,1,1]
                grid = self.connect4.table_to_grid(self.table)
                if self.connect4.end(grid):
                    self.animationFire('end')
                    instance.text = 'Enleve les pieces\npour recommencer'
                    self.ids.G1.anim_loop = 1
                    instance.color = [1, 1, 1, 1]
                    self.colorsLine = [1, 1, 1, 1]
                    self.colors = [240 / 256, 0, 0, 1]
                    self.first_end = True
                    if self.connect4.win(grid):
                        #self.robot1.celebrate(1)
                        pass
                    if self.connect4.lose(grid):
                        #self.robot1.celebrate(2)
                        pass
                else:
                    self.feu(1)
            '''    if self.connect4.win(grid):
                    self.robot1.celebrate(1)
                if self.connect4.lose(grid):
                    self.robot1.celebrate(2)
            else:
                if self.connect4.lose(grid):
                    self.robot.celebration(2)
                else:
                    self.robot.celebration(1)'''
        else: # si la fin de la partie est détectée après le coup du joeur
            print('ok')
            self.colors = [240/256,0,0,1]
            if self.first_end==False: # s'il appuie pour la première fois sur le bouton après avoir gagné
                print('firstend')
                self.animationFire('end')
                if self.connect4.win(grid):
                    #self.robot1.celebration(1)
                    pass
                if self.connect4.lose(grid):
                    #self.robot1.celebration(2)
                    pass
                if self.connect4.tie(grid):
                    # self.robot1.celebration(3)
                    pass
            else:
                self.animationFire('redFire')
                self.ids.G1._coreimage.anim_reset(True)
                self.ids.G1.anim_loop = 1
                self.ids.G1.source = 'Morpion/gifs/Stop_arm.gif'
                self.delay = 1/40
                self.robot1.say_no() #le robot dit non de la tête
            self.first_end = True
        self.robot1.robot.close_connection()




class connect4InterfaceApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return Connect4Game()


if __name__ == "__main__":
    connect4InterfaceApp().run()
