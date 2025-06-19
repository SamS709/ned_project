from kivy.app import App
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.properties import ListProperty
from Connect4.Minimax.MinMax import MinMax
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import random as rd
from Morpion.morpionInterface import var1
from kivy.lang import Builder
from Connect4.AI.Train import *
from kivy.core.window import Window
from ai_models_interface import TestButton

Builder.load_file('Connect4/connect4Interface.kv')

LIGHT_GREEN = [169 / 256, 221 / 256, 175 / 256, 1]
GREEN = [62 / 256, 182 / 256, 75 / 256, 1]
DARK_GREEN = [16 / 256, 118 / 256, 0, 1]
LIGHT_RED = [256/256,187/256,187/256,1]
RED = [237/256,79/256,79/256,1]
DARK_RED = [170/256,14/256,14/256,1]
LIGHT_BLUE = [182 / 256, 229 / 265, 246 / 256, 1]
BLUE = [112 / 256, 159 / 265, 256 / 256, 1]
DARK_BLUE = [82 / 256, 129 / 265, 256 / 256, 1]

class Mode(BoxLayout):  #Menu du choix de nombre de joueurs

    colors1 = ListProperty([1,0,0,1]) #couleur du bouton1
    colors2 = ListProperty([1, 0, 0, 1]) #couleur du bouton2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = 1, 1
        self.first = 'Start Playing'
        self.second = 'Let opponent Start'

    def pressB(self,instance): #on choisi le mode de jeu en cliquant sur B1 ou B2
        if instance.text == self.first:
            self.P1 = '1'
        if instance.text == self.second:
            self.P1 = '2'
        self.remove_widget(self.ids.B1) # on enlève tous les widgets du menu Mode
        self.remove_widget(self.ids.B2)
        self.remove_widget(self.ids.B3)
        self.game = Connect4GameNoRobot(gameMode=self.P1) # On charge une nouvelle partie avec le mode sélectionné
        self.add_widget(self.game) # On affiche la partie à l'écran

    def changeColor(self,instance): #on change la couleur du bouton quand on appuie dessus
        if instance.text == self.first:
            if self.colors1 == [1,0,0,1]:
                self.colors1 = [0,1,0,1]
            else:
                self.colors1 =[1,0,0,1]
            print(instance.state)
        if instance.text == self.second:
            self.colors2 = [0,1,0,1]



class Grille(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint =1,1 #taille de la grille
        self.pos_hint= {'x': 0, 'y': 0}
        #self.add_widget(Button(size_hint=(1,1)))
        self.Lbuttons = [] #liste des boutons répartis en colonne pour capter les clics
        for i in range(7): #création des boutons
            self.Lbuttons.append(Button(text=str(i),background_color=(0,0,0,0),color=(1,1,1,0)))
            self.add_widget(self.Lbuttons[i])
        #self.add_widget(Button(size_hint=(1, 1)))
        self.LR = []
        self.LC = [[]for j in range(7)]
        with self.canvas.before:
            Color(0, 0, 1, 0.9)
            for i in range(7): #création d'un fond blau pour chaque bouton => grand rectangle bleu qui fait toute la page
                self.LR.append(Rectangle(pos=self.Lbuttons[2].pos, size=self.Lbuttons[0].size))
            Color(LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], LIGHT_BLUE[3])
            for i in range(6): #création des cercles de couleur noir par dessus le rectangle bleu pour faire des 'trous' dans la grille
                for j in range(7):
                    self.LC[i].append(Ellipse(pos=(100,100),size=(50,50)))

class Connect4GameNoRobot(FloatLayout): #Classe principale du jeu Connect4 sans robot

    def __init__(self, P1='1P',TF=True, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.depth = 3 #niveau de jeu
        self.minimax = MinMax() #on instancie l'algorithme Minimax
        self.TF = TF
        self.first_player = 'computer' #joueur qui commence
        self.P1 = P1 #choix du mode de jeu (fait à partir de Mode : prend la valeur donnée à Mode)
        self.player = 'J' # prend la valeur 'J' ou 'R' en fonction de la couleur du jeton
        
        self.reset() #on initialise la partie

    def on_press_reset(self, instance):
        instance.button_color = DARK_BLUE
    
    def on_release_reset(self, instance):
        instance.button_color = BLUE
        self.reset()

    def reset(self):
        self.clear_widgets() # on enlève tous les widgets de la fenêtre
        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.grille = Grille() # on instancie une nouvelle grille de jeu
        self.main_layout.add_widget(self.grille) #On affiche la grille
        self.grid = np.array([0 for j in range(42)]) # on créé une grille de jeu 'théorique' qui permet de gérer ce qui se passe en back
        self.init_C() #Initialisation des pions qui vont s'afficher dans la grille
        self.button() #initioalisation des boutons bindés
        self.wpionJ = Widget() #créarion du pion Jaune
        with self.canvas.before:
            Color(0.68, 0.85, 0.90, 1)  # light blue (RGB: 173, 216, 230)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        with self.wpionJ.canvas:
            Color(1,1,0,1)
            self.pionJ = Ellipse(pos=(100, 100), size=(50, 50)) #On associe un canva au pion Jaune
        self.add_widget(self.wpionJ)
        self.wpionR = Widget() #créarion du pion Rouge
        with self.wpionR.canvas:
            Color(1,0,0,1)
            self.pionR = Ellipse(pos=(100, 100), size=(50, 50)) #On associe un canva au pion Rouge
        if self.P1 == '1': #Le robot commence à jouer en mode solo
            self.play()
        self.top_right_btn = TestButton(
            text='Play Again',
            size_hint=(0.18, 0.08),
            #size=(0.1, 0.1),
            pos_hint={'right': 0.98, 'top': 0.98},
            button_color = BLUE,
            on_press = self.on_press_reset,
            on_release = self.on_release_reset
        )
        self.add_widget(self.main_layout) #On ajoute la grille à la fenêtre
        self.main_layout.size = self.size
        self.main_layout.pos = self.pos
        self.bind(size=self._update_main_layout, pos=self._update_main_layout)
        self.add_widget(self.top_right_btn)
        self.grille.size_hint = (1, 1) #On fixe la taille de la grille
        self.wwidth,self.wheight = Window.size[0], Window.size[1] #On fixe la taille de la fenêtre
        Window.size = 0.9*self.wwidth,0.9*self.wheight
        Window.size = (self.wwidth, self.wheight) #On remet la taille de la fenêtre à sa taille d'origine
    def _update_main_layout(self, *args):
            self.main_layout.size = self.size
            self.main_layout.pos = self.pos
    

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    def button(self): # création des 7 boutons verticaux captant les clics
        for i in range(7):
            self.grille.Lbuttons[i].bind(on_release = self.release) #on bind ce qu'il se passe qd on press
            self.grille.Lbuttons[i].bind(on_press=self.press) #on bind ce qu'il se passe qd on relache

    def firstPlayer(self,table): # tells who played the first move
            n1 = np.count_nonzero(table == 1)
            n2 = np.count_nonzero(table == 2)
            if n1 >= n2:
                P1 = '1'
            else:
                P1 = '2'
            return P1

    def detPos(self):
        mode = var1.MODE
        level = var1.LEVEL
        print(var1.MODE)
        if mode == 'minimax':
            if level == 'novice':
                self.depth = 1
            if level == 'debutant':
                self.depth = 2
            if level == 'intermediaire':
                self.depth = 3
            if level == 'expert':
                self.depth = 4
            pos = self.minimax.best_pos(self.table,self.depth)
            print('MINIMAX')
        else:
            self.ai = DQN(model_name=var1.model_name,softmax_=False,P1=self.P1)
            #return pos = self.ai.best_pos(self.table,self.P1) not ready for the moment
            pos = self.ai.best_pos(self.table)
            print('AI')
        return pos
    
    def play(self):
        if self.first_player == 'computer':
            P1 ='1'
        else:
            P1 = '2'
        self.P1 = self.firstPlayer(self.table)
        pos = self.detPos()
        p,q = pos[0],pos[1]
        self.table = self.minimax.grid_to_table(self.grid)
        self.table[p,q] = 1
        self.grid = self.minimax.table_to_grid(self.table)
        for i in range(self.table.shape[0]):
            for j in range(self.table.shape[1]):
                self.remove_widget(self.LwCR[i][j])
                self.remove_widget(self.LwCJ[i][j])
        for i in range(self.table.shape[0]):
            for j in range(self.table.shape[1]):
                if self.table[i,j] == 1:
                    self.add_widget(self.LwCR[i][j])
                if self.table[i,j] == 2:
                    self.add_widget(self.LwCJ[i][j])
        if not self.minimax.end(grid=self.grid):
            self.player = 'J'

    def press(self,instance):
        PP = self.minimax.avaible_pos_graphics(self.grid)
        if self.player == 'J' and not self.minimax.end(self.grid):
            for i in range(6):
                for j in range(7):
                    if instance.text == str(j) and [i,j] in PP:
                        self.add_widget(self.LwCJ[i][j])
                        self.remove_widget(self.wpionJ)
    

    def release(self,instance):
        PP = self.minimax.avaible_pos_graphics(self.grid)
        self.table = self.minimax.grid_to_table(self.grid)
        if self.player == 'J' and not self.minimax.end(self.grid):
            for i in range(6):
                for j in range(7):
                    if instance.text == str(j) and [i,j] in PP:
                        self.table[i,j]=2
                        self.grid = self.minimax.table_to_grid(self.table)
                        self.add_widget(self.wpionJ)
                        self.player = 'R'
                        self.play()



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
        w,h = W/7, 6*H/8
        hh = h/6
        R = min(2 * w / 3, h / 7)

        self.grille.width, self.grille.height =W,H
        self.pionJ.size = R,R
        self.pionR.size = R, R

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

    def mouse_pos(self, window, pos):
        self.mousepos = pos
        self.pionJ.pos = pos[0] - self.pionJ.size[0] / 2, self.height - self.pionJ.size[1]
        self.pionR.pos = pos[0] - self.pionJ.size[0] / 2, self.height - self.pionJ.size[1]




class graphicsApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return Mode()


if __name__ == "__main__":
    graphicsApp().run()