# WARNING : only works with pyniryo==1.1.2 (pip install pyniryo==1.1.2)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from global_vars import *
from Connect4.AI.connect4InterfaceNoRobot import *
from Morpion.morpionInterface import *
from Connect4.connect4Interface import *
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from navigation_screen_manager import NavigationScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from popup import *





class TextArea(BoxLayout): # the text area giving informations that you see on the UI

    # kivy properties you find in the graphics.kv file (TextArea class)
    text = StringProperty("") # text displayed in the blue area
    title = StringProperty("") # title displayed in the brown area
    image_source = StringProperty('images/transparent.png') # source of the image displayed in the text area
    image_height = NumericProperty(30) # height of the image displayed
    TitleArea_color = ListProperty(SAND) # color of the title area
    Background_color = ListProperty(LIGHT_BLUE) # color of the background of the text area
    TA_color = ListProperty(BLUE) # color of the background of the text area
    Text_Color = ListProperty(WHITE) # color of the text
    Line_color = ListProperty(WHITE) # color of the line

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
    source_settings = StringProperty("images/setting2.png")

    colors1 = ListProperty(BLUE)
    colors2 = ListProperty(BLUE)
    colors5 = ListProperty(LIGHT_GREEN)

    color_line1 = ListProperty(WHITE)
    color_line2 = ListProperty(WHITE)

    def __init__(self, text='a', **kwargs):
        super().__init__(**kwargs)

    def pressB(self, instance):

        # Responsive design

        if instance.text == self.B1text:
            self.colors1 = WHITE
            self.colors2 = BLUE
            self.color_line1 = BLACK
            self.color_line2 = WHITE
            instance.color = BLACK
            self.ids.B2.color = WHITE
            self.colors5 = GREEN
            var1.GAME = 'morpion'
            self.screen = 'ChoiceModeMorpion'
            self.image_morpion = 'images/morpionWhite.png'
            self.image_connect4 = 'images/puissance4.png'

        if instance.text == self.B2text:
            self.colors2 = WHITE
            self.colors1 = BLUE
            self.color_line1 = WHITE
            self.color_line2 = BLACK
            instance.color = BLACK
            self.ids.B1.color = WHITE
            self.colors5 = GREEN
            var1.GAME = 'connect4'
            self.screen = 'ChoiceModePuissance4'
            self.image_morpion = 'images/morpion.png'
            self.image_connect4 = 'images/puissance4White.png'
        
        if instance.text == "":
            self.screen = 'MySettings'
            self.source_settings = "images/setting1.png"


        if instance.text == self.B5text and self.colors5 == GREEN:
            self.colors5 = DARK_GREEN

    def releaseB(self, instance):
        if instance.text == self.B5text and self.colors5 == DARK_GREEN or self.ids.Bsettings.background_color==SEMI_TRANSPARENT or instance.text == "":
            self.color_line1 = WHITE
            self.color_line2 = WHITE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.source_settings = "images/setting2.png"
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors5 = LIGHT_GREEN
            self.image_morpion = 'images/morpion.png'
            self.image_connect4 = 'images/puissance4.png'
            self.ids.Bsettings.background_color = TRANSPARENT
            #self.screen = "ChooseAIModel"
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
    colors1 = ListProperty(BLUE)
    colors2 = ListProperty(BLUE)
    colors5 = ListProperty(LIGHT_GREEN)
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
            self.colors1 = SAND
            self.ZdT.text = "Attention, il est impossible de gagner face à un adversaire qui connaît une stratégie gagnante !"
            self.Ntrain = 0
            self.colors2 = BLUE
            self.ids.B2.color = WHITE
            self.colors5 = GREEN
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
            self.colors2 = SAND
            self.ZdT.text = "Face à l'IA, tu as toutes tes chances de gagner.\n\n "
            self.Ntrain = 1000
            self.colors1 = BLUE
            self.ids.B1.color = WHITE
            self.colors5 = GREEN
            var1.MODE = 'IA'
            self.ZdT.image_source='images/brain.png'
            if var1.GAME == 'morpion':
                self.image_source = 'images/morpionIA.png'
            else:
                self.image_source='images/puissance4IA.png'
            self.ZdT.image_height = 50
            self.screen += var1.MODE
        if instance.text != self.B5text:
            instance.color = MAROON
        if instance.text == self.B5text and self.colors5 == GREEN:
            self.colors5 = DARK_GREEN

    def releaseB(self, instance):
        if instance.text == self.B5text and self.colors5 == DARK_GREEN:
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.colors5 = LIGHT_GREEN
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

    colors1 = ListProperty(BLUE)
    colors2 = ListProperty(BLUE)
    colors3 = ListProperty(BLUE)
    colors4 = ListProperty(BLUE)
    colors5 = ListProperty(LIGHT_GREEN)
    Ntrain = NumericProperty(0)

    titre = StringProperty("Choisis le niveau d'entrainement de ton adversaire !")

    def __init__(self,mode = 'IA',**kwargs):
        self.mode = mode
        super().__init__(**kwargs)
    
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ZdT = TextArea(text='coucou')
        self.ZdT.title = "[u]Quel niveau choisir ?[/u]"
        if self.mode == 'IA':
            self.B1text = 'Debutant'
            self.B2text = 'Intermediaire'
            self.B3text = 'Expert'
            self.B4text = 'Personnalise'
            self.titre = "Choisis le niveau d'entrainement de l'IA !"
            self.ZdT.text = "Plus le niveau sélectionné est élevé plus l'IA est forte.\n\nPour être plus forte, l'IA s'est entraînée en jouant plus de partie, tout simplement !"
        else:
            self.titre = "Choisis le niveau de l'algorithme Minimax !"
            self.ZdT.text = "Plus le niveau sélectionné est élevé plus l'algorithme est puissant.\n\nPour être plus performant, l'algorithme Minimax va explorer plein de parties possibles pour déterminer le coup qui lui est leplus favorable !"
        self.ids.zdt.add_widget(self.ZdT)


    def pressB(self, instance):
        if instance.text == self.B1text:
            var1.LEVEL = self.B1text.lower()
            self.colors1 = SAND
            self.Ntrain = 0
            self.colors2 = BLUE
            self.colors3 = BLUE
            self.colors4 = BLUE
            self.ids.B2.color = WHITE
            self.ids.B3.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/level1.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA n'a jamais été entraînée : elle découvre le jeu ! "
            else:
                self.ZdT.text = "Dans ce mode, l'algorithme n'explore pas de parties: il joue aléatoirement "


        if instance.text == self.B2text:
            var1.LEVEL = self.B2text.lower()
            self.colors2 = SAND
            self.Ntrain = 1000
            self.colors1 = BLUE
            self.colors3 = BLUE
            self.colors4 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B3.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/level2.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA n'a joué que 1000 parties : son apprentissage a été très court ! "
            else:
                self.ZdT.text = "Dans ce mode, l'algorithme ne prévoit qu'un coup à l'avance... pas très performant. "


        if instance.text == self.B3text:
            var1.LEVEL = self.B3text.lower()
            self.colors3 = SAND
            self.Ntrain = 5000
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors4 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/level3.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Dans ce mode, l'IA a joué 5000 parties : 5 fois plus d'expérience qu'au mode débutant.\nA toi de découvrir son évolution ! "
            else:
                self.ZdT.text = "Dans ce mode, l'Algorithme explore 3 coups à l'avance : il commence à voit ton coup venir ! "


        if instance.text == self.B4text:
            var1.LEVEL = self.B4text.lower()
            self.colors4 = SAND
            self.Ntrain = 10000
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors3 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.ids.B3.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/level4.png'
            if var1.MODE == 'IA':
                self.ZdT.text = "Tu peux choisir le modèle d'IA que tu souhaites utiliser. Pour en créer de nouveaux, tu peux aller sur la page d'accueil"
            else:
                self.ZdT.text = "Attention... dans ce mode, l'algorithme joue toutes les parties possibles avec 5 coups d'avance, il lit très clair dans ton jeu..."


        if instance.text != self.B5text:
            instance.color = MAROON # change button text color to maroon
        if instance.text == self.B5text and self.colors5 == GREEN:
            self.colors5 = DARK_GREEN


    def releaseB(self,instance):
        if instance.text == self.B5text and self.colors5 == DARK_GREEN:
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors3 = BLUE
            self.colors4 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.ids.B3.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = LIGHT_GREEN
            self.image_source = 'images/level0.png'
            self.popup = MainPopup()
            if var1.LEVEL=='personnalise':
                if var1.GAME == 'connect4':
                    App.get_running_app().manager.push('ChooseAIModelConnect4')
                else:
                    App.get_running_app().manager.push('ChooseAIModelMorpion')
            else:
                self.popup.show_popup()




class MySettings(ChoiceLevel): # Settings menu

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ZdT.text = "Choisis le paramètre que tu veux modifier"
        self.titre = 'Paramètres'
        self.B1text = 'Langue'
        self.B2text = 'Morpion'
        self.B3text = 'Puissance 4'
        self.B4text = 'Echecs'
        self.image_source = 'images/setting1.png'
        self.children[0].children[1].size_hint = 1,0.18 # reduce the "parameters" text area
        #self.ids.get('B4').parent.remove_widget(self.ids.get('B4')) # remove the button B4 (AI Model) from the settings screen

    def pressB(self, instance):
        if instance.text == self.B1text:
            self.colors1 = SAND
            self.colors2 = BLUE
            self.colors3 = BLUE
            self.colors4 = BLUE
            self.ids.B2.color = WHITE
            self.ids.B3.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = LIGHT_GREEN
            self.image_source = 'images/developpement.png'
            self.ZdT.text = "Pour le moment, seul le français est disponible"


        if instance.text == self.B2text:
            self.colors2 = SAND
            self.colors1 = BLUE
            self.colors3 = BLUE
            self.colors4 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B3.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/morpion.png'
            self.ZdT.text = "Modifier les paramètres du Morpion "
            self.screen = "EditModelsMorpion"


        if instance.text == self.B3text:
            self.colors3 = SAND
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors4 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.ids.B4.color = WHITE
            self.colors5 = GREEN
            self.image_source = 'images/puissance4.png'
            self.ZdT.text = "Modifier les paramètres du Puissance 4 ! "
            self.screen = "EditModelsConnect4"



        if instance.text == self.B4text:
            self.colors4 = SAND
            self.colors1 = BLUE
            self.colors2 = BLUE
            self.colors3 = BLUE
            self.ids.B1.color = WHITE
            self.ids.B2.color = WHITE
            self.ids.B3.color = WHITE
            self.colors5 = LIGHT_GREEN
            self.image_source = 'images/developpement.png'
            self.ZdT.text = "En cours de développement..."


        if instance.text != self.B5text:
            instance.color = MAROON
        if instance.text == self.B5text and self.colors5 == GREEN:
            self.colors5 = DARK_GREEN
            App.get_running_app().manager.push(self.screen) # pushes to the self.screen screen


    
    

class ChoiceLevelIA(BoxLayout):

    def on_kv_post(self, base_widget):
        self.add_widget(ChoiceLevel(mode='IA'))


class ChoiceLevelMinimax(BoxLayout):

    def on_kv_post(self, base_widget):
        self.add_widget(ChoiceLevel(mode='Minimax'))



class MyScreenManager(NavigationScreenManager): 
    pass


class graphicsApp(App):
    manager = ObjectProperty(None)
    
    def get_application_config(self):
        return super(graphicsApp, self).get_application_config()
    
    def get_kv_path(self):
        return os.path.join(os.path.dirname(__file__), 'graphics.kv')
    
    def load_kv(self, filename=None):
        return Builder.load_file(os.path.join(os.path.dirname(__file__), 'graphics.kv'))
    
    def build(self):
        self.width = Window.width
        self.height = Window.height
        self.manager = MyScreenManager() # We access the functions of MyScreenManager which inherits from NavigationSScreenManager and its methods
        return self.manager # we return the instantiated object and call a method via app.manager.method() where method is defined in MyScreenManager or inherited by MyScreenManager



if __name__=='__main__':
    graphicsApp().run()




