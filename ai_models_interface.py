from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from Connect4.AI.DQN import DQN
from kivy.core.window import Window
from kivy.uix.textinput import TextInput


import shutil
import os
import time
import threading
import keras


from kivy.properties import ListProperty, NumericProperty, StringProperty

LIGHT_GREEN = [169 / 256, 221 / 256, 175 / 256, 1]
GREEN = [62 / 256, 182 / 256, 75 / 256, 1]
DARK_GREEN = [16 / 256, 118 / 256, 0, 1]
LIGHT_RED = [256/256,187/256,187/256,1]
RED = [237/256,79/256,79/256,1]
DARK_RED = [170/256,14/256,14/256,1]


class GetInfo:
     
     def __init__(self):
          pass
     
     def get_model_path(self,model_name):
         return os.path.join(os.getcwd()+"\Connect4\AI\models",model_name)
     
     def get_model_names(self): # returns a list of the name of the models we have
          return os.listdir(os.getcwd()+"\Connect4\AI\models")
     
     def get_info_model(self,model_name):
        print(os.getcwd())
        filepath=os.getcwd()+"\Connect4\AI\models"+f"\{str(model_name)}1"
        print(filepath)
        model = keras.models.load_model(filepath=filepath)
        cfg = model.get_config()
        print(cfg)
        layers = cfg['layers']
        n_layers = len(layers)
        n_dense = 0
        n_neurons_per_layer = 0
        for i in range(n_layers):
            if layers[i]['class_name'] == "Dense":
                if cfg['layers'][i]['config']['units']>1:
                    n_neurons_per_layer = cfg['layers'][i]['config']['units']
                    n_dense += 1
        n_neurons_tot = n_dense*n_neurons_per_layer
        info = f"  - Nom du modele: {str(model_name)}\n\n"
        info += f"  - Nombre total de couches: {str(n_layers)}\n\n  - Une couche d'entrée spécifiant la taille de la grille: ici 6x7 = 42.\n\n"
        info += f"  - Nombre de couches denses: {n_dense}.\n\n  - Nombre de neurones par couche dense: {str(n_neurons_per_layer)}.\n\n  - Nombre total de neurones: {str(n_neurons_tot)}\n\n"
        info += f"Les {n_layers-n_dense} couches restantes sont là pour assurer que le modèle ait un fonctionnement optimal. "
        return info

class InfoLabel(Label):
     
     line_width = NumericProperty(2)
     background_color = ListProperty([112 / 256, 159 / 265, 256 / 256, 1])
     line_button_color = ListProperty([1,1,1,1])
     
     def __init__(self, **kwargs):
          super().__init__(**kwargs)
        
    

class TestButton(Button):
    button_color = ListProperty([182 / 256, 229 / 265, 246 / 256, 1])
    line_button_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.getInfo = GetInfo()
    
    def on_press(self):
         print(1)





class ScrollableLabel(ScrollView):

    text = StringProperty('')
    color = ListProperty([1,0,0,1])


class ScrollingMenu(BoxLayout):

    # kivy properties you find in the graphics.kv file (TextArea class)
    text = StringProperty("coucou") # text displayed in the blue area
    title = StringProperty("Selectionne le modele d'IA de Ned") # title displayed in the brown area
    image_source = StringProperty('images/transparent.png') # source of the image displayed in the text area
    image_height = NumericProperty(30) # height of the image displayed
    TitleArea_color = ListProperty([219 / 256, 195 / 265, 151 / 256, 1]) # color of the title area
    Background_color = ListProperty([182 / 256, 229 / 265, 246 / 256, 1]) # color of the background of the text area
    TA_color = ListProperty([0, 0, 1, 1]) # color of the background of the text area
    Text_Color = ListProperty([1, 1, 1, 1]) # color of the text
    Line_color = ListProperty([1, 1, 1, 1]) # color of the line

    def __init__(self, **kwargs):
            super().__init__(**kwargs)

class ChooseAIModel(BoxLayout):

    Background_color = ListProperty([182 / 256, 229 / 265, 246 / 256, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_kv_post(self, base_widget):
        self.getInfo = GetInfo()
        self.scroll_menu = ScrollingMenu()
        self.scroll = self.scroll_menu.ids.scroll 
        self.info_label = self.ids.info_label
        self.scroll_box = self.ids.Scroll_box
        self.init_buttons()
        self.setup_title()


        
    
    def init_buttons(self):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None )
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.L_buttons = []
        self.load_button_list()
        self.validate_button = self.ids.validate_button
        self.validate_button.bind(on_press = self.on_press_validate, on_release = self.on_release_validate)
        self.validate_button.button_color = LIGHT_GREEN

    def load_button_list(self):
        self.layout.clear_widgets()
        self.scroll.clear_widgets()
        self.scroll_box.clear_widgets()
        self.model_list = self.getInfo.get_model_names()
        self.L_buttons = []
        for i in range(len(self.model_list)):
            btn = TestButton(text=str(self.model_list[i][:-1]), size_hint_y=None, height=40, on_press = self.on_press, on_release = self.on_release)
            if i % 2 == 0:
                self.L_buttons.append(btn)
                self.layout.add_widget(btn)
        self.scroll.add_widget(self.layout)
        self.scroll_box.add_widget(self.scroll_menu)

    def on_press_validate(self,instance):
        if self.validate_button.button_color == GREEN:
            self.validate_button.button_color = DARK_GREEN
    
    def on_release_validate(self,instance):
        self.validate_button.button_color = LIGHT_GREEN
        for btn in self.L_buttons:
             btn.button_color = [182 / 256, 229 / 265, 246 / 256, 1]

    def setup_title(self):
        self.ids.title_label.background_color = [1,1,1,1]
        self.ids.title_label.color = [0,0,0,1]
        self.ids.title_label.line_button_color = [0,0,0,1]
         

    def on_release(self,instance):
        instance.button_color = [112 / 256, 159 / 265, 256 / 256, 1]
        try:
            thread1 = threading.Thread(target=self.get_info, args=(instance, ))
            thread1.start()
        except BaseException:
            print('Error: unable to start thread')
    

    def on_press(self,instance):
        for btn in self.L_buttons:
             btn.button_color = [182 / 256, 229 / 265, 246 / 256, 1]
        instance.button_color = [82 / 256, 129 / 265, 256 / 256, 1]
        self.validate_button.button_color = [62 / 256, 182 / 256, 75 / 256, 1]
        

    def get_info(self,instance):
        try:
            info = self.getInfo.get_info_model(instance.text)
        except:
             info = "Erreur de chargement des informations"
        self.info_label.text = info
        print(info)

class CreateNewModel(ChooseAIModel):
    def __init__(self, **kwargs):
          super().__init__(**kwargs)
    

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.model_name = ""
        self.bottom_box =  self.ids.bottom_box
        self.info_input = MenuInput(self.on_release_cancel_new)
        self.update_texts_and_buttons()
    
    def on_release_cancel_new(self):
        print("3")
        self.scroll_box.clear_widgets()
        self.scroll_box.add_widget(self.scroll_menu)
        
    
    def update_texts_and_buttons(self):
        self.bottom_box.padding = [0,0,0,0]
        self.bottom_box.clear_widgets()
        self.log_label = ScrollableLabel()
        self.bottom_box.add_widget(self.log_label)
        self.left_title = self.scroll_menu.ids.left_title
        self.left_title.text = "Coucou"
        self.actions = BoxLayout(size_hint=(1,0.3),orientation="horizontal",padding = [0.1*self.width,0,0.1*self.width,0.1*self.height], spacing = 10)
        self.add = TestButton(text="New", on_press=self.add_on_press, on_release = self.add_on_release)
        self.delete = TestButton(text="Delete", on_press=self.delete_on_press, on_release = self.delete_on_release)
        self.add.button_color=GREEN
        self.delete.button_color=LIGHT_RED
        self.actions.add_widget(self.delete)
        self.actions.add_widget(self.add)
        self.scroll_menu.add_widget(self.actions)

    def log_error(self,i):
        if i == 1:
            self.bottom_box.padding = [0,0.05*self.bottom_box.height,0,0.05*self.bottom_box.height]
            self.log_label.text+="\n[ERREUR] Impossible de supprimer le modele "+str(self.model_name)
        if i == 2:
            self.bottom_box.padding = [0,0.05*self.bottom_box.height,0,0.05*self.bottom_box.height]
            self.log_label.text+="\n[ERREUR] Impossible de supprimer les modeles presents par defaut"


    def on_press(self, instance):
        for btn in self.L_buttons:
             btn.button_color = [182 / 256, 229 / 265, 246 / 256, 1]
        instance.button_color = [82 / 256, 129 / 265, 256 / 256, 1]
        self.model_name = instance.text
        self.delete.button_color = RED
    
    def delete_on_release(self,instance):
        instance.button_color = LIGHT_RED      

    def delete_on_press(self,instance):
        if instance.button_color==RED:
            instance.button_color=DARK_RED
            path = self.getInfo.get_model_path(self.model_name)
            print(path)
            print(self.model_name)
            cond = self.model_name == "Expert" or self.model_name == "Intermediaire" or self.model_name == "Debutant"
            if cond:
                self.log_error(2)
            else:
                try:
                    shutil.rmtree(path+"1")
                    print("Suppression de self.model_name réussie !")
                except:
                    self.log_error(1)
                    print("Le modèle n'a pas pu être supprimé")
                try:
                    shutil.rmtree(path+"2")
                    print("Suppression de self.model_name réussie !")
                except:
                    self.log_error(1)
                    print("Le modèle n'a pas pu être supprimé")
                self.load_button_list()

        

    def add_on_press(self,instance):
        if instance.button_color == GREEN:
            instance.button_color = DARK_GREEN


    def add_on_release(self,instance):
        if instance.button_color == DARK_GREEN:
            instance.button_color = GREEN
            self.scroll_box.clear_widgets()
            self.info_label.text = f"Nom du modèle: \n\n\n\nNombre de couches: \n\n\n\nNombre de neurones par couche: \n\n\n\nNombre total de neurones: \n\n"
            #self.scroll_box.padding = [0,0,0,0]
            self.scroll_box.add_widget(self.info_input)

class IBeamTextInput(TextInput):
    _instances = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        IBeamTextInput._instances.append(self)
        if len(IBeamTextInput._instances) == 1:
            Window.bind(mouse_pos=IBeamTextInput.on_mouse_pos_all)

    def on_parent(self, *args):
        if self.parent is None and self in IBeamTextInput._instances:
            IBeamTextInput._instances.remove(self)
            if not IBeamTextInput._instances:
                Window.unbind(mouse_pos=IBeamTextInput.on_mouse_pos_all)

    @staticmethod
    def on_mouse_pos_all(window, pos):
        for instance in IBeamTextInput._instances:
            if instance.get_root_window() and instance.collide_point(*instance.to_widget(*pos)):
                Window.set_system_cursor('ibeam')
                return
        Window.set_system_cursor('arrow')

class InfoInput(BoxLayout):

    button_set_color = ListProperty(GREEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MenuInput(BoxLayout):

    validate_color = ListProperty(GREEN)
    cancel_color = ListProperty(RED)



    def __init__(self, on_release_cancel, **kwargs):
        self.on_release_cancel_ = on_release_cancel
        super().__init__(**kwargs)

    def on_press_cancel(self,instance):
        if instance.button_color == RED:
            instance.button_color = DARK_RED
        print("COUCOU")

    
    def on_release_cancel(self,instance):
        if instance.button_color == DARK_RED:
            instance.button_color = RED
        print("4")
        self.on_release_cancel_()

    def on_press_validate(self,instance):
        if instance.button_color == GREEN:
            instance.button_color = DARK_GREEN
        print(99)

    def on_release_validate(self,instance):
        if instance.button_color == DARK_GREEN:
            instance.button_color = GREEN
        print(99)


class ai_models_interfaceApp(App):
      def build(self):
            return CreateNewModel()
      

if __name__!="__main__":
    Builder.load_file('ai_models_interface.kv')

if __name__=="__main__":
      #model = keras.models.load_model(filepath="C:\Dev\ned_project\Connect4\AI\models\my_linear_model1")
      ai_models_interfaceApp().run()
