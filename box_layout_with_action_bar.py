from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

# The bar you seeon the top of the UI to go back to the previous screen

Builder.load_file('box_layout_with_action_bar.kv')

class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty() # c'est une chaîne de caractère qu'on va pouvoir remplir après dans un fichier kv
    pass