from kivy.lang import Builder
from Connect4.Minimax.MinMax import *
from kivy.app import App
from graphics import var1
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.widget import Widget
from Connect4.AI.DQN import *
import threading
from Connect4.Robot import *
from kivy.clock import mainthread



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

    delay = NumericProperty(1000)
    anim_loop = NumericProperty(0)
    colors = ListProperty([100/256,100/256,100/256,1])
    color1 = ListProperty([100/256,100/256,100/256,1])
    color2 = ListProperty([0,0,1,1])
    colorsLine = ListProperty([0,0,0,1])
    colorLine1 = ListProperty([0,0,0,1])
    colorLine2 = ListProperty([1,1,1,1])


    def __init__(self,depth=3, **kwargs):
        self.first_end = False #indique si le robot détecte la fin ou pas: utile pour le feu de fin : si self.end == True et self.first_end == False alors on célèbre le fin. Si self.end == False : on indique q'il faut retirer les pieces
        super().__init__(**kwargs)
        self.minimax = MinMax()
        self.connect4 = Connect4()
        self.t1 : threading.Thread = threading.Thread() # thread that will be used to run the robot's actions
        self.table = np.array([[0 for j in range(7)] for i in range(6)])
        self.pressText = ' Press when you \nfinished your move' # the text on the button before it is pressed
        self.restartText = 'Enleve les pieces\npour recommencer' # the text on the button when pieces should be removed
        self.releaseText = 'Ned is playing...' # the text on the button when ned is playing
        self.depth = depth


    def on_kv_post(self, base_widget):
        self.game = self.ids.G
        self.action_bar = self.ids.action_bar



    @mainthread
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

    @mainthread
    def fire(self,color): # change the color of the traffic light
            if color == "green":
                self.ids.feuLose.source = "Morpion/image/feuLose/feu1.png"
            if color == "red":
                self.ids.feuLose.source = "Morpion/image/feuLose/feu3.png"

    def firstPlayer(self,table): # tells who played the first move
        n1 = np.count_nonzero(table == 1)
        n2 = np.count_nonzero(table == 2)
        if n1 >= n2:
            P1 = '1'
        else:
            P1 = '2'
        return P1

    def thread_robot(self,instance):
        try:
            self.robot1 = Robot() # useful toaccess to ned's actions
            self.action_bar.animate_wifi("green")
            self.table = self.robot1.modif_table() # the robot look at the game and change the table according to the detected piece
            self.fire("red") # change traffic light to red
            self.first_end = False # if a game is restarted we want first_end to be false
            self.modifUI(instance,0)# update the displayed game according to the table
            self.robot_connected = True # True if the robot is connected
        except:
            self.robot_connected = False
            t = threading.Thread(target=self.action_bar.animate_wifi,args=("red",))
            t.start()
        mode = var1.MODE # mode selected in the menu (see graphics.py)
        level = var1.LEVEL # level selected in the menu (see graphics.py)
        self.grid = self.connect4.table_to_grid(self.table)
        if self.robot_connected:
            if not self.connect4.end(self.grid): # if the game is not finished after the user played
                self.P1 = self.firstPlayer(self.table) # determines who started to play
                pos = self.detPos(mode, level) # determines the position of the piece that the robot should play
                p,q = pos[0],pos[1]
                self.table[p,q]=1 # change the current table to the one modified by the robot
                self.robot1.place(q) # robot pick and place the piece to the position determined above
                self.modifUI(instance,1,p,q)  # add the piece on UI and change text / color ....
                if self.connect4.end(self.grid): # if the robot won after its play
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
                    self.modifUI(instance,2)
            self.robot1.robot.move_pose(self.robot1.home_pos)
            self.robot1.robot.close_connection() # close the connection of the robot in order not to connect multiple times to the robot.
            self.robot_connected = False
            # Morever, we don't want the robot to be connected too long because it creates bugs
        else :
            pass
        self.anim_loop = 1 # the animation of the robot is not looping
        self.delay = 1/1000
        time.sleep(0.5)
        self.modifUI(instance,5) # update the displayed game according to the table
        self.modifUI(instance,6) # change the text of the button to indicate that the user can play again

    @mainthread
    def modifUI(self,instance,i,p=0,q=0): # change the UI according to the parameter
        if i == 0:
            for h in range(self.table.shape[0]):
                for j in range(self.table.shape[1]):
                    self.game.remove_widget(self.game.LwCJ[h][j])
                    self.game.remove_widget(self.game.LwCR[h][j])
                    if self.table[h, j] == 1:
                        self.game.add_widget(self.game.LwCR[h][j])
                    if self.table[h, j] == 2:
                        self.game.add_widget(self.game.LwCJ[h][j])
        if i == 1:
            self.game.add_widget(self.game.LwCR[p][q])
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
        if i==4:
            instance.text = self.releaseText # change text's button
            instance.text = "Ned is playing..."
            self.colors = self.color2 # change the color of the button
            self.colorsLine = self.colorLine2 # change the color of the line
            instance.color = [1, 1, 1, 1] # change the color of the text
            self.delay = 1/33
            self.anim_loop = 0
        if i ==5:
            self.ids.G1.source = 'Morpion/gifs/bras-robotique-gros.gif'
            self.ids.G1.reload()
            self.delay = 10000
        if i == 6:
            instance.text = ' Press when you \nfinished your move'
            instance.color = [1,1,1, 1]
            self.colors = self.color1
            self.colorsLine = self.colorLine1


    def pressB(self,instance): # when the button ispressed
        cond = instance.text == self.pressText or instance.text == self.restartText
        if cond and self.t1.is_alive() == False: # if the button is pressed when the user has finished his move or if the game is restarted
            self.modifUI(instance,4)


    def detPos(self,mode,level):
        self.ai = DQN(model_name=var1.model_name,softmax_=False,P1=self.P1)
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
            #return pos = self.ai.best_pos(self.table,self.P1) not ready for the moment
            pos = self.ai.best_pos(self.table)
        print(pos)
        return pos



    def releaseB(self,instance):
        if instance.text == self.releaseText and self.t1.is_alive() == False: # if the button is released when the robot is playing
            self.t1 = threading.Thread(target=self.thread_robot, args=(instance,))
            self.feu_image = 'Morpion/image/feuLose/feu1.png'
            self.t1.start()                  




class connect4InterfaceApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return Connect4Game()


if __name__ == "__main__":
    connect4InterfaceApp().run()
