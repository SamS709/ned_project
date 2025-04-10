from kivy.app import App
from kivy.graphics import Line, Color
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget
from Morpion.AI.AI import *
from Connect4.connect4Interface import var1
from Morpion.Minimax.MinMax import *
import time
from Morpion.Robot import *

Builder.load_file('Morpion/morpionInterface.kv')




class MorpionGrille(GridLayout): # creates the grid
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 3
        self.size_hint = 1,1


class MorpionItems(Widget): # creates the circles and the squares that will be added to the UI

    R = NumericProperty(1)
    L = NumericProperty(1)

    def __init__(self, **kwargs,):
        super().__init__(**kwargs)
        self.size_hint=1,1
        self.init_circle()
        self.init_square()
        self.Grid= MorpionGrille()
        self.add_widget(self.Grid)


    def init_circle(self,*args):

        self.Lwcircle=[[] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.Lwcircle[i].append(Widget())


        self.Lcircle = [[] for i in range(3)]
        for i in range(3):
            for j in range(3):
                with self.Lwcircle[i][j].canvas:
                    Color(115/256,63/256,11/256,1)
                    self.Lcircle[i].append(Line(circle=(5, 5, 5), width=2.5))


    def init_square(self,*args):

        self.Lwsquare=[[] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.Lwsquare[i].append(Widget())

        self.Lsquare = [[] for i in range(3)]
        for i in range(3):
            for j in range(3):
                with self.Lwsquare[i][j].canvas:
                    Color(115/256,63/256,11/256,1)
                    self.Lsquare[i].append(Line(rectangle=(5, 5, 5,100), width=2.5))


    def on_size(self,*args):
        w,h = self.width,self.height

        #position de la grille et des boutons
        self.Grid.width,self.Grid.height = w,h
        a,b = 0.05*w,0.05*h
        x,y = (w-2*a)/3, (h-2*b)/3
        R = min((w-2*a) / 7.5, (h-2*b) / 7.5)
        L = 5*R/3
        for i in range(3):
            for j in range(3):
                self.Lcircle[-(i+1)][j].circle= (a+(2*j+1)*x/2, b+(2*i+1)*y/2 , R)
                self.Lsquare[-(i+1)][j].rectangle = (a+(2*j+1)*x/2-L/2, b+(2*i+1)*y/2-L/2, L, L)



class MorpionGame(BoxLayout):

    feu_image = StringProperty('Morpion/image/feu0.png')
    delay = NumericProperty(1/33)
    colors = ListProperty([219/256,195/265,151/256,1])
    color1 = ListProperty([219/256,195/265,151/256,1])
    color2 = ListProperty([0,0,1,1])
    colorsLine = ListProperty([168/256,114/256,60/256,1])
    colorLine1 = ListProperty([168/256,114/256,60/256,1])
    colorLine2 = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_end = False # tells if the robot has already detected the end of the game. If this is the case, first_end = True, else: first_end = False
        self.P1 = 'robot' # tells who plays first
        self.size_hint = 1,1
        self.table = np.array([[0 for j in range(3)] for i in range(3)]) # create a table of tic tac toe
        self.morpion = Morpion()
        self.minimax = MinMax()
        self.ai = AI()
        self.depth = 6 # exploratio's depth of minimax's algorithm
        self.robot1 = Robot() # useful toaccess to ned's actions
        self.robot1.robot.move_to_home_pose() # we want ned to go at its home position when we launch the application
        self.robot1.robot.close_connection() # we don't want the connectionto remain to long becauseofbugs and because we don't want to connect simunaetly with 2 Robot instancies
        self.pressText = ' Press when you \nfinished your move' # the text on the button before it is pressed
        self.restartText = 'Enleve les pieces\npour recommencer' # the text on the button when pieces should be removed
        self.releaseText = 'Ned is playing...' # the text on the button when ned is playing


    def on_kv_post(self, base_widget): # wait until kv file is executed before running this function
        self.game =self.ids.G

    def animationFire(self, state): # animate the traffic lights
        self.ids.feuLose.source = "Morpion/image/feu%d.png" % int(self.ids.feuLose.image_num)
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



    def fire(self,color): # change the color of the traffic light
            if color == "green":
                self.ids.feuLose.source = "Morpion/image/feuLose/feu1.png"
            if color == "red":
                self.ids.feuLose.source = "Morpion/image/feuLose/feu3.png"


    def pressB(self,instance): # when the button ispressed
        if instance.text == self.pressText or instance.text == self.restartText:
            instance.text = self.releaseText # change text's button
            self.robot1 = Robot() # create a new robot
            self.table = self.robot1.modif_table() # the robot look at the game and change the table according to the detected piece
            self.fire("red") # change traffic light to red
            self.first_end = False # if a game is restarted we want first_end to be false
            instance.text = "Ned is playing..."
            self.colors = self.color2 # change the color of the button
            self.colorsLine = self.colorLine2 # change the color of the line
            instance.color = [1, 1, 1, 1] # change the color of the text
            self.modifUI(instance,0)# update the displayed game according to the table


    def firstPlayer(self,table): # tells who played the first move
        n1 = np.count_nonzero(table == 1)
        n2 = np.count_nonzero(table == 2)
        if n1 >= n2:
            P1 = '1'
        else:
            P1 = '2'
        return P1

    def detPos(self, mode, level): # returns the pos calculated by the selected mode (AI or Minimax)
        if mode == 'minimax':
            if level == 'novice':
                self.depth = 1
            if level == 'debutant':
                self.depth = 2
            if level == 'intermediaire':
                self.depth = 4
            if level == 'expert':
                self.depth = 7
            return self.minimax.best_pos(self.table,self.depth)
        else:
            return self.ai.best_pos(self.table,self.P1)

    def modifUI(self,instance,i,p=0,q=0): # change the UI according to the parameter
        if i == 0:
            for h in range(self.table.shape[0]):
                for j in range(self.table.shape[1]):
                    self.game.remove_widget(self.game.Lwsquare[2 - h][2 - j])
                    self.game.remove_widget(self.game.Lwcircle[2 - h][2 - j])
                    if self.table[h, j] == 1:
                        self.game.add_widget(self.game.Lwcircle[2 - h][2 - j])
                    if self.table[h, j] == 2:
                        self.game.add_widget(self.game.Lwsquare[2 - h][2 - j])
        if i == 1:
            self.game.add_widget(self.game.Lwcircle[2 - p][2 - q])
            instance.text = ' Press when you \nfinished your move'
            instance.color = [115 / 256, 63 / 256, 11 / 256, 1]
            self.colors = self.color1
            self.colorsLine = self.colorLine1
        if i == 2:
            self.animationFire('end')
            instance.text = 'Enleve les pieces\npour recommencer'
            self.ids.G1.anim_loop = 1
            instance.color = [1, 1, 1, 1]
            self.colorsLine = [1, 1, 1, 1]
            self.colors = [240 / 256, 0, 0, 1]
            self.first_end = True  # indicates that the end game has already been signaled to te user
        if i == 3:
            self.ids.G1._coreimage.anim_reset(True)
            self.ids.G1.anim_loop = 1
            self.ids.G1.source = 'Morpion/gifs/Stop_arm.gif'
            self.delay = 1 / 40
            self.animationFire('redFire')
            instance.color = [1,1,1,1]
            self.colors = [1,0,0,1]



    def releaseB(self,instance): # when the button is released
        self.feu_image = 'Morpion/image/feuLose/feu1.png'
        mode = var1.MODE # mode selected in the menu (see graphics.py)
        level = var1.LEVEL # level selected in the menu (see graphics.py)
        if not self.morpion.end(self.table): # if the game is not finished after the user played
            self.P1 = self.firstPlayer(self.table) # determines who started to play
            pos = self.detPos(mode, level) # determines the position of the piece that the robot should play
            p,q = pos[0],pos[1]
            self.table[p,q]=1 # change the current table to the one modified by the robot
            self.robot1.place(p,q) # robot pick and place the piece to the position determined above
            self.modifUI(instance,1,p,q)  # add the piece on UI and change text / color ....
            if self.morpion.end(self.table): # if the robot won after its play
                instance.text= self.releaseText
                self.modifUI(instance,2) # animation to tell the user the robot won
            else:
                instance.text = self.pressText # then, the user will be able to play
                self.fire("green")
        else: # if the user won after he played (or he tries to play after an end has been detected)
            instance.text = self.restartText
            if self.first_end==False:
                # self.robot1.say_no()
                self.modifUI(instance,3) # traffic light blinks red
            else:
                self.modifiUI(instance,2)
        self.robot1.robot.move_pose(self.robot1.home_pos)
        self.robot1.robot.close_connection() # close the connection of the robot in order not to connect multiple times to the robot.
        # Morever, we don't want the robot to be connected too long because it creates bugs


class morpionInterfaceApp(App):

    def build(self):
        return MorpionGame()

if __name__ == "__main__":
    A = morpionInterfaceApp()
    A.run()