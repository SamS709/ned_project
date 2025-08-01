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
from kivy.uix.switch import Switch
import random as rd
from Morpion.morpionInterface import var1
from kivy.lang import Builder
from Connect4.AI.Train import *
from kivy.core.window import Window
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'GUI'))
from ai_models_interface import MyButton

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



class Grille(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #self.add_widget(Button(size_hint=(1,1)))
        self.Lbuttons = [] # list of buttons distributed in columns to capture clicks
        for i in range(7): # button creation
            self.Lbuttons.append(Button(text=str(i),background_color=(0,0,0,0),color=(1,1,1,0)))
            self.add_widget(self.Lbuttons[i])
        #self.add_widget(Button(size_hint=(1, 1)))
        self.LR = []
        self.LC = [[]for j in range(7)]
        with self.canvas.before:
            Color(0, 0, 1, 0.9)
            for i in range(7): # creating a blue background for each button => big blue rectangle that covers the whole page
                self.LR.append(Rectangle(pos=self.Lbuttons[2].pos, size=self.Lbuttons[0].size))
            Color(LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], LIGHT_BLUE[3])
            for i in range(6): # creating black circles on top of the blue rectangle to make 'holes' in the grid
                for j in range(7):
                    self.LC[i].append(Ellipse(pos=(100,100),size=(50,50)))
        

class Connect4GameNoRobot(FloatLayout): # Main class for Connect4 game without robot

    def __init__(self, P1='1P', **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.depth = 3 # game level
        self.minimax = MinMax() # instantiate the Minimax algorithm
        self.P1 = P1 # game mode choice (made from Mode: takes the value given to Mode)
        self.reset() # initialize the game

    def on_press_reset(self, instance):
        instance.button_color = DARK_BLUE
    
    def on_release_reset(self, instance):
        instance.button_color = BLUE
        self.reset()

    def reset(self):
        self.clear_widgets() # remove all widgets from the window
        self.P1 = '2' # by default, the AI plays after
        self.player = 'J' # by default, the user starts (user = yellow player)
        self.grille = Grille() # instantiate a new game grid
        self.add_widget(self.grille) # Display the grid
        self.grid = np.array([0 for j in range(42)]) # create a 'theoretical' game grid that manages what happens in the back
        self.table = self.minimax.grid_to_table(self.grid) # convert the grid to table for Minimax algorithm
        self.init_C() # Initialize the pieces that will be displayed in the grid
        self.button() # initialize the bound buttons
        self.wpionJ = Widget() # we create the piece of user
        with self.canvas.before:
            Color(0.68, 0.85, 0.90, 1)  # light blue (RGB: 173, 216, 230)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        with self.wpionJ.canvas:
            Color(1,1,0,1)
            self.pionJ = Ellipse(pos=(100, 100), size=(50, 50)) # Associate a canvas to the Yellow piece
        self.add_widget(self.wpionJ) 
        self.player_one_button = MyButton(
            text='Play 2nd',
            size_hint=(0.2, 0.08),
            #size=(0.1, 0.1),
            pos_hint={'right': 0.22, 'top': 0.98},
            button_color = RED,
            on_press = self.on_press_player_one,
            on_release = self.on_release_player_one
        )
        self.reset_button = MyButton(
            text='Play again',
            size_hint=(0.2, 0.08),
            #size=(0.1, 0.1),
            pos_hint={'right': 0.98, 'top': 0.98},
            button_color = BLUE,
            on_press = self.on_press_reset,
            on_release = self.on_release_reset
        )
        self.add_widget(self.player_one_button) # Add the button to let the opponent start
        self.add_widget(self.reset_button)        
        self.on_size() # updateing the size of the elements

    
    def on_press_player_one(self, instance):
        if instance.button_color == RED :
            instance.button_color = DARK_RED

    def on_release_player_one(self, instance):
        if instance.button_color == DARK_RED :
            instance.button_color = LIGHT_RED
            self.first_shot = True
            self.player = 'R' #the red player starts
            self.P1 = '1'
            self.play() #we play the first move of the red player


    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def button(self): # creation of 7 vertical buttons capturing clicks
        for i in range(7):
            self.grille.Lbuttons[i].bind(on_release = self.release) # bind what happens when button is pressed
            self.grille.Lbuttons[i].bind(on_press=self.press) # bind what happens when button is released

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
        else:
            self.ai = DQN(model_name=var1.model_name,softmax_=False,P1=self.P1)
            #return pos = self.ai.best_pos(self.table,self.P1) not ready for the moment
            print(var1.MODE)
            pos = self.ai.best_pos(self.table)
        return pos
    
    def play(self):
        self.player_one_button.button_color = LIGHT_RED
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



    def init_C(self,*args): # init the circles
        self.LwCJ = [[] for j in range(7)] # yellow widgets
        self.LwCR = [[] for j in range(7)] # red widgets
        self.LCJ = [[] for j in range(7)] # yellow canvas
        self.LCR = [[] for j in range(7)] # red canvas
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



    def on_size(self, *args): # keeps proportions

        W,H= self.width, self.height
        w,h = W/7, 6*H/8
        hh = h/6
        R = min(2 * w / 3, h / 7)

        self.grille.width, self.grille.height =W,H
        self.pionJ.size = R,R

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

    def mouse_pos(self, window, pos): # detects mouse pos, and changes the yellow piece position thanks to it
        self.mousepos = pos
        self.pionJ.pos = pos[0] - self.pionJ.size[0] / 2, self.height - self.pionJ.size[1]




class graphicsApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return Connect4GameNoRobot()


if __name__ == "__main__":
    graphicsApp().run()