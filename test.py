from kivy.app import App
from kivy.lang import Builder

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 40
    spacing: 20

    ThemedProgressBar:
        id: pb
        bar_color: 0.3, 0.7, 0.4, 0  # Example color
        border_color: 1, 1, 1, 0

    Button:
        text: "Increase"
        size_hint_y: None
        height: 40
        on_press: pb.value = min(pb.value + 10, pb.max)
'''

Builder.load_file('test.kv')

class DemoApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    DemoApp().run()