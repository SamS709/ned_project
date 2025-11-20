from kivy.lang import Builder
from kivy.clock import mainthread
from pyniryo import *
import time
import os
from kivy.properties import StringProperty,ListProperty
from kivy.uix.boxlayout import BoxLayout
import threading


# The bar you see on the top of the UI to go back to the previous screen and test if the connection with the robot can be established

# Load the .kv file only once to prevent duplicates
if not hasattr(Builder, '_box_layout_with_action_bar_loaded'):
    Builder.load_file(os.path.join(os.path.dirname(__file__), 'box_layout_with_action_bar.kv'))
    Builder._box_layout_with_action_bar_loaded = True

class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty() # c'est une chaîne de caractère qu'on va pouvoir remplir après dans un fichier kv
    icon = StringProperty("images/wifi/wifi_w.png")
    button_color_wifi = ListProperty([1,1,1,0])

    def on_press(self):
        self.button_color_wifi = [1,1,1,0.3]
        print("Connexion en cours")
        self.t1 = threading.Thread(target=self.animate_wifi,args=("orange",))
        self.t1.start()
        self.t2 = threading.Thread(target=self.connect_robot)
        self.t2.start()

    def on_release(self):
        self.button_color_wifi = [1,1,1,0]

    @mainthread
    def set_wifi_o(self,i):
        self.icon = f"images/wifi/wifi_o{str(i)}.png"
    
    @mainthread
    def set_wifi_r(self,c):
        self.icon = f"images/wifi/wifi_{str(c)}.png"

    def animate_wifi(self,color):
        if color=="orange":
            for i in range(3):
                for i in range(1,5):
                    self.set_wifi_o(i)
                    time.sleep(0.5)
        if color == "red":
            for i in range(4):
                time.sleep(0.3)
                self.set_wifi_r("r")
                time.sleep(0.7)
                self.set_wifi_r("w")
            self.set_wifi_r("r")
        if color == "green":
            self.set_wifi_r("g")

    
    
    
    def connect_robot(self):
        try:
            robot_ip_address = "10.10.10.10"
            robot = NiryoRobot(robot_ip_address)
            robot.calibrate_auto()
            robot.update_tool()
            robot.set_arm_max_velocity(100)
            while self.t1.is_alive():
                a=0
            self.animate_wifi("green")
            robot.close_connection()
        except:
            print("eeeeeeeeeeee")
            while self.t1.is_alive():
                a=0
            self.animate_wifi("red")
    
  
        