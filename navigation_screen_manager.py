from kivy.uix.screenmanager import ScreenManager

# Allows us to navigate between the different windows

class NavigationScreenManager(ScreenManager):
    screen_stack = []

    def push(self,screen_name):
        self.screen_stack.append(self.current)
        self.transition.direction = 'left'
        self.current = screen_name

    def pop(self):
        if len(self.screen_stack)>0:
            self.transition.direction = 'right'
            self.current = self.screen_stack[-1]
            self.screen_stack.pop()
