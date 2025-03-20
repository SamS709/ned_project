from kivy.app import App
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget

from Minimax.MinMax import *




class Grille(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None,None #taille de la grille
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
            Color(0,0,0,1)
            for i in range(6): #création des cercles de couleur noir par dessus le rectangle bleu pour faire des 'trous' dans la grille
                for j in range(7):
                    self.LC[i].append(Ellipse(pos=(100,100),size=(50,50)))

class Game(BoxLayout):

    def __init__(self, gameMode='1P', **kwargs):
        super(Game, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.minimax = MinMax()
        self.depth = 3 #niveau de jeu
        self.P1 = '1' #joueur qui commence
        self.player = '1' # prend la valeur 'J' ou 'R' en fonction de la couleur du jeton
        self.grille = Grille() # on instancie une nouvelle grille de jeu
        self.add_widget(self.grille) #On affiche la grille
        self.table = np.array([[0 for j in range(7)] for i in range(6)]) # on créé une grille de jeu 'théorique' qui permet de gérer ce qui se passe en back
        self.init_C() #Initialisation des pions qui vont s'afficher dans la grille
        self.button() #initioalisation des boutons bindés
        self.wpionJ = Widget() #créarion du pion Jaune
        with self.wpionJ.canvas:
            Color(1,1,0,1)
            self.pionJ = Ellipse(pos=(100, 100), size=(50, 50)) #On associe un canva au pion Jaune
        self.add_widget(self.wpionJ)
        self.wpionR = Widget() #créarion du pion Rouge
        with self.wpionR.canvas:
            Color(1,0,0,1)
            self.pionR = Ellipse(pos=(100, 100), size=(50, 50)) #On associe un canva au pion Rouge
        if self.P1 == '1': #Le robot commence à jouer en mode solo
            self.robot()

    def button(self): # création des 7 boutons verticaux captant les clics
        for i in range(7):
            self.grille.Lbuttons[i].bind(on_press=self.press) #on bind ce qu'il se passe qd on relache
            self.grille.Lbuttons[i].bind(on_release=self.release)

    def robot(self):
        grid = self.minimax.table_to_grid(self.table)
        if not self.minimax.end(grid):
            a = -10000
            Lpos = self.minimax.avaible_pos_graphics(self.table)
            a = -10000
            POS = []
            for pos in Lpos:
                TABLE = self.table.copy()
                TABLE[pos[0], pos[1]] = 1
                val = self.minimax.minmax(TABLE, self.depth, -10000, 10000, 2)
                if val > a:
                    a = val
                    Lequalpos = [pos]
                if val == a:
                    Lequalpos.append(pos)
            POS = random.choice(Lequalpos)
            self.table[POS[0],POS[1]]=1
            self.add_widget(self.LwCR[POS[0]][POS[1]])
            self.remove_widget(self.wpionJ)
            self.add_widget(self.wpionJ)
            self.player = '2'


    def press(self,instance):
        Lpos = self.minimax.avaible_pos_graphics(self.table)
        grid = self.minimax.table_to_grid(self.table)
        if self.player == '2' and not self.minimax.end(grid):
            for i in range(6):
                for j in range(7):
                    if instance.text == str(j) and [i,j] in Lpos:
                        self.add_widget(self.LwCJ[i][j])
                        self.remove_widget(self.wpionJ)
                        self.player = '1'
                        self.table[i,j]=2

    def release(self,instance):
        self.robot()

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




class gameApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return Game()


if __name__ == "__main__":
    gameApp().run()
