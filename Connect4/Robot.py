from pyniryo import *
import time
import os
import numpy as np
import cv2
from Connect4.model import Model, transform
import torch
from PIL import Image
import sys
import importlib
import importlib.util
import pygame

# Ensure torch.load can resolve pickled references to module 'model'.
# We reliably alias 'model' to the local Connect4/model.py using a file-based import,
# which works whether the package import path is available or not.
try:
    module_path = os.path.join(os.path.dirname(__file__), 'model.py')
    spec = importlib.util.spec_from_file_location('model', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules['model'] = module
except Exception:
    # Fallback: try regular package import alias if available
    try:
        sys.modules['model'] = importlib.import_module('Connect4.model')
    except Exception:
        pass

class Robot:

    def __init__(self):
        # connect to the robot when a new Robot object is created
        self.model = torch.load(os.path.join("Connect4", "AI", "models", "model3.pt"), weights_only= False, map_location=torch.device('cpu'))
        self.device = 'cpu'
        self.model.eval()
        robot_ip_address = "10.10.10.10"
        robot = NiryoRobot(robot_ip_address)
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(100)
        self.robot = robot
        self.stock = PoseObject(x = 0.2368, y = 0.0598, z = 0.1440,
                                roll = 0.777, pitch = 1.522, yaw = 0.769)  # position of the stock of circles (pieces played by the robot)
        self.middle_pos = PoseObject(x = 0.1041, y = 0.0009, z = 0.4700,
                                     roll = 0.077, pitch = 1.028, yaw = 0.042) # middle position when the robot plays in order to avoid collisions with the board
        self.home_pos = PoseObject(x = 0.1344, y = -0.0001, z = 0.1652,
                                   roll = 0.000, pitch = 1.011, yaw = -0.001)
        self.observationPose2 = PoseObject(x = 0.1448, y = 0.0048, z = 0.1768,
                                           roll = 0.045, pitch = 0.449, yaw = 0.036)
        self.observationPose = PoseObject(x = 0.1320, y = 0.0052, z = 0.2225,
                                            roll = -0.040, pitch = 0.273, yaw = 0.034)

    def cam_pos(self): # the robot moves towards a position from which it can analyse the board game
        self.robot.move_pose(self.observationPose2)


    def red_yellow_pos(self): # returns the image frame, a list of red pieces positions and a list of yellow pieces positions
        save_path = "current_game"
        os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
        self.cam_pos()
        mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
        img = self.robot.get_img_compressed() # getting image
        img_uncom = uncompress_image(img) # uncompressing image
        img_undis = undistort_image(img_uncom, mtx, dist) # undistort
        # Save with timestamp
        image_name = "current.png"
        cv2.imwrite(os.path.join(save_path, image_name), img_undis)
        image = Image.open(os.path.join(save_path, image_name)).convert('RGB')
        X = transform(image)
        with torch.no_grad():
            # cv2.imshow("coucou", X.numpy())
            X = X.unsqueeze(0).to(self.device)  # Add batch dimension and move to device
            pred_table = torch.argmax(self.model(X), dim = 1).reshape([6,7]).cpu().numpy()
        
        return img_undis, pred_table
    
    def check_table(self, table0: np.array, table: np.array):
        table0 = np.asarray(table0)
        table = np.asarray(table)
        
        if np.count_nonzero(table0) == table0.size and np.count_nonzero(table) == table0.size:
            return True

        old_values_mask = table0 != 0
        if not np.array_equal(table[old_values_mask], table0[old_values_mask]):
            return False

        diff_mask = table != table0
        if np.count_nonzero(diff_mask) != 1:
            return False

        i, j = np.argwhere(diff_mask)[0]
        return table0[i, j] == 0 and table[i, j] == 2





    def modif_table(self, table0: np.array): # returns the table detected by the robot
        pred_table = None
        while not self.check_table(table0, pred_table):        
            save_path = "current_game"
            os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
            self.cam_pos()
            mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
            img = self.robot.get_img_compressed() # getting image
            img_uncom = uncompress_image(img) # uncompressing image
            img_undis = undistort_image(img_uncom, mtx, dist) # undistort
            # Save with timestamp
            image_name = "current.png"
            cv2.imwrite(os.path.join(save_path, image_name), img_undis)
            image = Image.open(os.path.join(save_path, image_name)).convert('RGB')
            X = transform(image)
            with torch.no_grad():
                # cv2.imshow("coucou", X.numpy())
                X = X.unsqueeze(0).to(self.device)  # Add batch dimension and move to device
                pred_table = torch.argmax(self.model(X), dim = 1).reshape([6,7]).cpu().numpy()
            
        return pred_table

    def place(self, j): # robot moves to puta piece in the j-th column

        if j == 0:
            pos = [0.3864,0.1156, 0.3892, 0.007, 0.284, 0.222]
        if j == 1:
            pos = [0.3825,0.0815, 0.3982, -0.037,  0.388, 0.099]
        if j == 2:
            pos = [0.3828,0.0394, 0.3959, -0.073,  0.297, 0.045]
        if j == 3:
            pos = [0.3826,-0.0004, 0.3963, -0.081, 0.298, -0.062]
        if j == 4:
            pos = [0.3807,-0.0371, 0.3900, -0.098, 0.313, -0.164]
        if j == 5:
            pos = [0.3725,-0.0758, 0.3903, -0.059, 0.320, -0.213]
        if j == 6:
            pos = [0.3830,-0.1179, 0.3955, -0.051, 0.380, -0.294]

        pos1 = [0.1344, -0.0001, 0.1652, 0.000, 1.011, -0.001] # home positionn
        pos2 = [0.1041, 0.0009, 0.4700, 0.077, 1.028, 0.042] # middle position in order to avoid colisions with the physical board
        self.robot.pick_from_pose(self.stock)
        self.robot.execute_trajectory_from_poses([pos2, pos])
        self.robot.open_gripper()
        self.robot.execute_trajectory_from_poses([pos, pos2, pos1])

    def place2(self, j): # robot moves to puta piece in the j-th column

        if j == 0:
            pos = [0.3748, 0.1351, 0.4255,-0.055, 0.536, 0.344]
        if j == 1:
            pos = [0.3798, 0.0909, 0.4297,-0.077, 0.579, 0.215]
        if j == 2:
            pos = [0.3837, 0.0432, 0.4265,0.024, 0.657, 0.114]
        if j == 3:
            pos = [0.3882, 0.0004, 0.4238,0.005, 0.600, -0.013]
        if j == 4:
            pos = [0.3752, -0.0521, 0.4246,-0.205, 0.655, -0.142]
        if j == 5:
            pos = [0.3789,-0.1021,0.4141,-0.063,0.510,-0.237]
        if j == 6:
            pos = [0.3755,-0.1474,0.4072,-0.045,0.380,-0.343]

        pos1 = [0.1344, -0.0001, 0.1652, 0.000, 1.011, -0.001] # home positionn
        pos2 = [0.1041, 0.0009, 0.4700, 0.077, 1.028, 0.042] # middle position in order to avoid colisions with the physical board
        self.robot.pick_from_pose(self.stock)
        self.robot.execute_trajectory_from_poses([pos2, pos])
        self.robot.open_gripper()
        self.robot.execute_trajectory_from_poses([pos, pos2, pos1])


    def say_no(self): # to make the robot say no in real world 
        pos1 = [0.1271,-0.0404,0.2085,-0.122, 0.333,-0.305]
        pos2 = [0.1276, 0.0350,0.2117,-0.086,0.359,0.294]
        self.robot.set_arm_max_velocity(100)
        self.robot.execute_trajectory_from_poses([pos1, pos2,pos1,pos2])

    def take_picture(self):
        # Play sound to notify that picture is being taken
        
        save_path = "connect4_dataset"
        os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
        self.cam_pos()
        time.sleep(0.5)
        mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
        img = self.robot.get_img_compressed() # getting image
        img_uncom = uncompress_image(img) # uncompressing image
        img_undis = undistort_image(img_uncom, mtx, dist) # undistort
        # Save with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(os.path.join(save_path, f'img_undis_{timestamp}.png'), img_undis)
        pygame.mixer.init()
        pygame.mixer.music.load('Morpion/beep.wav')
        pygame.mixer.music.play()
        time.sleep(0.2)    

    def take_n_pictures(self, n):
        for i in range(n):
            time.sleep(3.0)
            self.take_picture()
            print("Picture taken || num of the pic: ", i)




if __name__=='__main__':

    robot1 = Robot()
    # #robot1.place(0)
    print(robot1.robot.get_pose())
    # print(robot1.modif_table())
    # robot1.take_picture()
    print(robot1.modif_table())
    # robot1.take_n_pictures(1)
    # """for j in range(7):
    #     robot1.place(j)"""
