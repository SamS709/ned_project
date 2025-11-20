import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from global_vars import *
from ai_models_interface import MyButton, InfoLabel, InfoBoxLayout


class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.title = kwargs.get('title', 'Popup Title')
        self.content = kwargs.get('content', None)
        self.size_hint = kwargs.get('size_hint', (0.4, 0.4))
        self.auto_dismiss = kwargs.get('auto_dismiss', True)


class MainPopup(BoxLayout):
        
    def show_popup(self, *args):
        content = InfoBoxLayout(orientation='vertical', spacing=10, padding=10, line_width = 1.5)
        lbl = InfoLabel(text="Do you want to play with ned2 or versus the computer ?", line_width = 1,halign='center',valign='middle')
        lbl.bind(
            size=lambda instance, value: setattr(instance, 'text_size', value)
        )        
        content.add_widget(lbl)
        btn_layout = InfoBoxLayout(orientation = "horizontal", size_hint_y=None, height=60, spacing=10, line_width = 1.5)
        btn_yes = MyButton(text="Robot", button_color=GREEN, line_width = 1.5)
        btn_no = MyButton(text="Computer", button_color=RED, line_width = 1.5)
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)

        popup = MyPopup(title="Choose your opponent", content=content, title_font='fonts/pixel.TTF',title_size = 0.12 * self.width,background = 'atlas://data/images/defaulttheme/button_pressed')

        def on_press_yes(instance):
            instance.button_color = DARK_GREEN # change button color to dark green when pressed

        def on_release_yes(instance):
            if var1.GAME == 'morpion':
                App.get_running_app().manager.push('MorpionGame')
            else:
                App.get_running_app().manager.push('Connect4Game')
            instance.button_color = GREEN # change button color to dark green when pressed
            popup.dismiss()
        
        def on_press_no(instance):
            instance.button_color = DARK_RED
        
        def on_release_no(instance):
            if var1.GAME == 'morpion':
                pass
            else:
                App.get_running_app().manager.push('Connect4GameNoRobot')
            instance.button_color = RED
            popup.dismiss()

        btn_yes.bind(on_press=on_press_yes) 
        btn_yes.bind(on_release=on_release_yes)
        btn_no.bind(on_release=on_release_no)
        btn_no.bind(on_press=on_press_no)
        popup.open()