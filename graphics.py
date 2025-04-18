from Morpion.morpionInterface import *
from Connect4.connect4Interface import *
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from navigation_screen_manager import NavigationScreenManager
from kivy.core.window import Window


# WARNING : only works with pyniryo==1.1.2 (pip install pyniryo==1.1.2)

# global variables that we can access in other files

class var:
    def __init__(self):
        self.MODE = ""
        self.LEVEL = ""
        self.GAME = ""

var1 = var()
# creates a variable that we will access in other files


class TextArea(BoxLayout): # the text area giving informations that you see on the UI

    # kivy properties you find in the graphics.kv file (TextArea class)
    text = StringProperty("") # text displayed in the blue area
    title = StringProperty("") # title displayed in the brown area
    image_source = StringProperty('images/transparent.png') # source of the image displayed in the text area
    image_height = NumericProperty(30) # height of the image displayed
    TitleArea_color = ListProperty([219 / 256, 195 / 265, 151 / 256, 1]) # color of the title area
    Background_color = ListProperty([182 / 256, 229 / 265, 246 / 256, 1]) # color of the background of the text area
    TA_color = ListProperty([0, 0, 1, 1]) # color of the background of the text area
    Text_Color = ListProperty([1, 1, 1, 1]) # color of the text
    Line_color = ListProperty([1, 1, 1, 1]) # color of the line

    def __init__(self,text='Insérer texte',titre = 'insérer titre',**kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.title = titre

class ChoiceGame(BoxLayout): # First menu to choose the game you want to play

    # kivy properties you find in the graphics.kv file (ChoiceGame class)
    screen = StringProperty('ChoiceMode')
    B1text = StringProperty('Morpion')
    B2text = StringProperty('Puissance 4')
    B5text = StringProperty('Valider')
    image_morpion = StringProperty('images/morpion.png')
    image_connect4 = StringProperty('images/puissance4.png')

    colors1 = ListProperty([0, 0, 1, 1])
    colors2 = ListProperty([0, 0, 1, 1])
    colors5 = ListProperty([169 / 256, 221 / 256, 175 / 256, 1])

    color_line1 = ListProperty([1, 1, 1, 1])
    color_line2 = ListProperty([1, 1, 1, 1])

    def __init__(self, text='a', **kwargs):
        super().__init__(**kwargs)

    def pressB(self, instance):

        # Responsive design

        if instance.text == self.B1text:
            self.screen = 'ChoiceMode'
            self.colors1 = [1,1,1,1]
            self.colors2 = [0, 0, 1, 1]
            self.color_line1 = [0, 0, 0, 1]
            self.color_line2 = [1, 1, 1, 1]
            instance.color = [0,0,0,1]
            self.ids.B2.color = [1,1,1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            var1.GAME = 'morpion'
            self.screen = 'ChoiceModeMorpion'
            self.image_morpion = 'images/morpionWhite.png'
            self.image_connect4 = 'images/puissance4.png'

        if instance.text == self.B2text:
            self.screen = 'ChoiceMode'
            self.colors2 = [1,1,1, 1]
            self.colors1 = [0, 0, 1, 1]
            self.color_line1 = [1, 1, 1, 1]
            self.color_line2 = [0, 0, 0, 1]
            instance.color = [0,0,0,1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            var1.GAME = 'connect4'
            self.screen = 'ChoiceModePuissance4'
            self.image_morpion = 'images/morpion.png'
            self.image_connect4 = 'images/puissance4White.png'

        if instance.text == self.B5text and self.colors5 == [62 / 256, 182 / 256, 75 / 256, 1]:
            self.colors5 = [16 / 256, 118 / 256, 0, 1]

    def releaseB(self, instance):
        if instance.text == self.B5text and self.colors5 == [16 / 256, 118 / 256, 0, 1]:
            self.color_line1 = [1, 1, 1, 1]
            self.color_line2 = [1, 1, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.colors1 = [0, 0, 1, 1]
            self.colors2 = [0, 0, 1, 1]
            self.colors5 = [169 / 256, 221 / 256, 175 / 256, 1]
            self.image_morpion = 'images/morpion.png'
            self.image_connect4 = 'images/puissance4.png'
            App.get_running_app().manager.push(self.screen) # pushes the selected screen

class ChoiceModeMorpion(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(ChoiceMode(game='morpion'))

class ChoiceModePuissance4(BoxLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(ChoiceMode(game='puissance4'))


class ChoiceMode(BoxLayout): # Makes the user choose between AI and Minimax Algorithm

    # kivy properties you find in the graphics.kv file (ChoiceGame class)
    B1text = StringProperty('MiniMax')
    B2text = StringProperty('IA')
    B5text = StringProperty('Valider')
    screen = StringProperty('ChoiceLevel')
    image_source = StringProperty('images/morpion.png')
    colors1 = ListProperty([0, 0, 1, 1])
    colors2 = ListProperty([0, 0, 1, 1])
    colors5 = ListProperty([169 / 256, 221 / 256, 175 / 256, 1])
    Ntrain = NumericProperty(0)

    def __init__(self,game='morpion',**kwargs):
        super().__init__(**kwargs)
        if game!= 'morpion':
            self.image_source='images/puissance4.png'

    def on_kv_post(self, text='a'):
        self.ZdT = TextArea(text='coucou')
        self.ids.zdt.add_widget(self.ZdT)
        self.ZdT.text = "L'algorithme Minimax a été pensé par des humains pour donner une stratégie gagnante à l'ordinateur\n\nL'IA a joué des milliers de parties pour apprendre, sans avoir besoin de l'aide d'un humain !"
        self.ZdT.title = '[u]Comment choisir ton adversaire ?[/u]'

    # displays information according to the level selected, to help the user to make his choice
    def pressB(self, instance):
        if instance.text == self.B1text:
            self.screen = 'ChoiceLevel'
            self.colors1 = [219 / 256, 195 / 265, 151 / 256, 1]
            self.ZdT.text = "Attention, il est impossible de gagner face à un adversaire qui connaît une stratégie gagnante !"
            self.Ntrain = 0
            self.colors2 = [0, 0, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            var1.MODE = 'minimax'
            self.ZdT.image_source='images/graph.png'
            if var1.GAME == 'morpion':
                self.image_source = 'images/morpionM.png'
            else:
                self.image_source='images/puissance4M.png'
            self.ZdT.image_height = 30
            self.screen ='ChoiceLevelMinimax'
        if instance.text == self.B2text:
            self.screen = 'ChoiceLevel'
            self.colors2 = [219 / 256, 195 / 265, 151 / 256, 1]
            self.ZdT.text = "Face à l'IA, tu as toutes tes chances de gagner.\n\n "
            self.Ntrain = 1000
            self.colors1 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            var1.MODE = 'IA'
            self.ZdT.image_source='images/brain.png'
            if var1.GAME == 'morpion':
                self.image_source = 'images/morpionIA.png'
            else:
                self.image_source='images/puissance4IA.png'
            self.ZdT.image_height = 50
            self.screen += var1.MODE
        if instance.text != self.B5text:
            instance.color = [115 / 256, 63 / 256, 11 / 256, 1]
        if instance.text == self.B5text and self.colors5 == [62 / 256, 182 / 256, 75 / 256, 1]:
            self.colors5 = [16 / 256, 118 / 256, 0, 1]

    def releaseB(self, instance):
        if instance.text == self.B5text and self.colors5 == [16 / 256, 118 / 256, 0, 1]:
            self.colors1 = [0, 0, 1, 1]
            self.colors2 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.colors5 = [169 / 256, 221 / 256, 175 / 256, 1]
            self.ZdT.image_source='images/transparent.png'
            self.ZdT.text = "L'algorithme Minimax a été pensé par des humains pour donner une stratégie gagnante à l'ordinateur\n\nL'IA a joué des milliers de parties pour apprendre, sans avoir besoin de l'aide d'un humain !"
            if var1.GAME == 'morpion':
                self.image_source = 'images/morpion.png'
            else:
                self.image_source='images/puissance4.png'
            App.get_running_app().manager.push(self.screen) # pushes to the selected screen


class ChoiceLevel(BoxLayout): # Makes the user choose the level (number of trains for AI and depth exploration for minimax algorithm)

    # kivy properties you find in the graphics.kv file (ChoiceGame class)
    B1text = StringProperty('Novice')
    B2text = StringProperty('Debutant')
    B3text = StringProperty('Intermediaire')
    B4text = StringProperty('Expert')
    B5text = StringProperty('Valider')

    image_source = StringProperty('images/level0.png')

    colors1 = ListProperty([0,0,1,1])
    colors2 = ListProperty([0,0,1,1])
    colors3 = ListProperty([0,0,1,1])
    colors4 = ListProperty([0,0,1,1])
    colors5 = ListProperty([169/256, 221/256, 175/256 ,1])
    Ntrain = NumericProperty(0)

    titre = StringProperty("Choisis le niveau d'entrainement de ton adversaire !")

    def __init__(self,mode = 'IA',**kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.ZdT = TextArea(text='coucou')
        self.ZdT.title = "[u]Quel niveau choisir ?[/u]"
        if self.mode == 'IA':
            self.titre = "Choisis le niveau d'entrainement de l'IA !"
            self.ZdT.text = "Plus le niveau sélectionné est élevé plus l'IA est forte.\n\nPour être plus forte, l'IA s'est entraînée en jouant plus de partie, tout simplement !"
        else:
            self.titre = "Choisis le niveau de l'algorithme Minimax !"
            self.ZdT.text = "Plus le niveau sélectionné est élevé plus l'algorithme est puissant.\n\nPour être plus performant, l'algorithme Minimax va explorer plein de parties possibles pour déterminer le coup qui lui est leplus favorable !"
        self.ids.zdt.add_widget(self.ZdT)


    def pressB(self, instance):
        if instance.text == self.B1text:
            var1.LEVEL = self.B1text.lower()
            self.colors1 = [219/256,195/265,151/256,1]
            self.Ntrain = 0
            self.colors2 = [0, 0, 1, 1]
            self.colors3 = [0, 0, 1, 1]
            self.colors4 = [0, 0, 1, 1]
            self.ids.B2.color = [1,1,1,1]
            self.ids.B3.color = [1,1,1,1]
            self.ids.B4.color = [1,1,1,1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            self.image_source = 'images/level1.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA n'a jamais été entraînée : elle découvre le jeu ! "
            else:
                self.ZdT.text = "Dans ce mode, l'algorithme n'explore pas de parties: il joue aléatoirement "


        if instance.text == self.B2text:
            var1.LEVEL = self.B2text.lower()
            self.colors2 = [219/256,195/265,151/256,1]
            self.Ntrain = 1000
            self.colors1 = [0, 0, 1, 1]
            self.colors3 = [0, 0, 1, 1]
            self.colors4 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B3.color = [1, 1, 1, 1]
            self.ids.B4.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            self.image_source = 'images/level2.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA n'a joué que 1000 parties : son apprentissage a été très court ! "
            else:
                self.ZdT.text = "Dans ce mode, l'algorithme ne prévoit qu'un coup à l'avance... pas très performant. "


        if instance.text == self.B3text:
            var1.LEVEL = self.B3text.lower()
            self.colors3 = [219/256,195/265,151/256,1]
            self.Ntrain = 5000
            self.colors1 = [0, 0, 1, 1]
            self.colors2 = [0, 0, 1, 1]
            self.colors4 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.ids.B4.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            self.image_source = 'images/level3.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA a joué 5000 parties : 5 fois plus d'expérience qu'au mode débutant.\nA toi de découvrir son évolution ! "
            else:
                self.ZdT.text = "Dans ce mode, l'Algorithme explore 3 coups à l'avance : il commence à voit ton coup venir ! "


        if instance.text == self.B4text:
            var1.LEVEL = self.B4text.lower()
            self.colors4 = [219/256,195/265,151/256,1]
            self.Ntrain = 10000
            self.colors1 = [0, 0, 1, 1]
            self.colors2 = [0, 0, 1, 1]
            self.colors3 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.ids.B3.color = [1, 1, 1, 1]
            self.colors5 = [62 / 256, 182 / 256, 75 / 256, 1]
            self.image_source = 'images/level4.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Attention... dans ce mode, l'IA s'est entraînée 10000 fois, elle est très puissante."
            else:
                self.ZdT.text = "Attention... dans ce mode, l'algorithme joue toutes les parties possibles avec 5 coups d'avance, il lit très clair dans ton jeu..."


        if instance.text != self.B5text:
            instance.color = [115/256,63/256,11/256,1]
        if instance.text == self.B5text and self.colors5 == [62/256, 182/256, 75/256, 1]:
            self.colors5 = [16/256,118/256,0,1]


    def releaseB(self,instance):
        if instance.text == self.B5text and self.colors5 == [16/256,118/256,0,1]:
            self.colors1 = [0, 0, 1, 1]
            self.colors2 = [0, 0, 1, 1]
            self.colors3 = [0, 0, 1, 1]
            self.colors4 = [0, 0, 1, 1]
            self.ids.B1.color = [1, 1, 1, 1]
            self.ids.B2.color = [1, 1, 1, 1]
            self.ids.B3.color = [1, 1, 1, 1]
            self.ids.B4.color = [1, 1, 1, 1]
            self.colors5 = [169 / 256, 221 / 256, 175 / 256, 1]
            self.image_source = 'images/level0.png'
            if var1.GAME == 'morpion':
                App.get_running_app().manager.push('MorpionGame')
            else:
                App.get_running_app().manager.push('Connect4Game')



class ChoiceLevelIA(BoxLayout):

    def on_kv_post(self, base_widget):
        self.add_widget(ChoiceLevel(mode='IA'))


class ChoiceLevelMinimax(BoxLayout):

    def on_kv_post(self, base_widget):
        self.add_widget(ChoiceLevel(mode='Minimax'))


class MyScreenManager(NavigationScreenManager): #hérite du screen manager qu'on a créé
    pass


class graphicsApp(App):
    manager = ObjectProperty(None)
    def build(self):
        self.width = Window.width
        self.height = Window.height
        self.manager = MyScreenManager() # We access the functions of MyScreenManager which inherits from NavigationSScreenManager and its methods
        return self.manager # we return the instantiated object and call a method via app.manager.method() where method is defined in MyScreenManager or inherited by MyScreenManager



if __name__=='__main__':
    graphicsApp().run()




