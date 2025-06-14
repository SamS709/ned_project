from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder

class test(Button):
      
        def __init__(self, **kwargs):
                super(test, self).__init__(**kwargs)
                self.text = "Test Button"
                self.size_hint = (None, None)
                self.size = (200, 50)
        
        def on_press(self):
            print(self.state)

        def on_release(self):
            print(self.state)
            


class testApp(App):
      def build(self):
            return test()
      

if __name__!="__main__":
    Builder.load_file('ai_models_interface.kv')

if __name__=="__main__":
      #model = keras.models.load_model(filepath="C:\Dev\ned_project\Connect4\AI\models\my_linear_model1")
      testApp().run()