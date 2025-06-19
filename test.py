from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.title = kwargs.get('title', 'Popup Title')
        self.content = kwargs.get('content', None)
        self.size_hint = kwargs.get('size_hint', (0.4, 0.4))
        self.auto_dismiss = kwargs.get('auto_dismiss', True)

class MainWidget(BoxLayout):
    def show_popup(self, *args):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Do you want to continue?"))

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_yes = Button(text="Yes")
        btn_no = Button(text="No")
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)

        popup = MyPopup(title="Confirmation", content=content)

        btn_yes.bind(on_release=lambda *a: (print("Yes pressed"), popup.dismiss()))
        btn_no.bind(on_release=lambda *a: (print("No pressed"), popup.dismiss()))

        popup.open()

class TestApp(App):
    def build(self):
        root = MainWidget(orientation='vertical', padding=40, spacing=20)
        btn = Button(text="Open Popup", size_hint=(None, None), size=(200, 50))
        btn.bind(on_release=root.show_popup)
        root.add_widget(btn)
        return root

if __name__ == '__main__':
    TestApp().run()