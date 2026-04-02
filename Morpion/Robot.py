from pyniryo import *
import numpy as np
import time
import cv2 as cv
import pygame
import os
from Morpion.model import Model, transform
import torch
from PIL import Image
import sys
import importlib
import importlib.util
import pygame
# WARNING : only works with pyniryo==1.1.2

try:
    module_path = os.path.join(os.path.dirname(__file__), 'model.py')
    spec = importlib.util.spec_from_file_location('model', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules['model'] = module
except Exception:
    # Fallback: try regular package import alias if available
    try:
        sys.modules['model'] = importlib.import_module('Morpion.model')
    except Exception:
        pass


class Robot:

    def __init__(self):
        # connect to the robot when a new Robot object is created
        self.device = "cpu"
        self.model = torch.load(os.path.join("Morpion", "AI", "models", "model.pt"), weights_only= False, map_location=torch.device('cpu'))
        robot_ip_address = "10.10.10.10"
        robot = NiryoRobot(robot_ip_address)
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(100)
        self.robot = robot
        self.stock = PoseObject(x = -0.0220, y = -0.1308, z = 0.0989,
                                roll = -0.248, pitch = 1.259, yaw = 2.945)  # position of the stock of circles (pieces played by the robot)
        self.observation_pose = PoseObject(x = 0.0019, y = -0.2310, z = 0.3170,
                                           roll = -3.046, pitch = 1.204, yaw = 1.689) # DON'T USE THIS, prefer the next one which matches with the original camera
        self.observation_pose2 = PoseObject(x = -0.0039, y = -0.2469, z = 0.3117,
                                           roll = -2.849, pitch = 1.375, yaw = 1.852) # position adapted to analyse the board
        self.home_pos = PoseObject(x = -0.0003, y = -0.1231, z = 0.1630,
                                   roll = -0.014, pitch = 1.053, yaw = -1.560)



    def cam_pos(self, rd=False): # the robot moves towards a position from which it can analyse the board game
        target_pose = self.observation_pose
        if rd:
            # Add a small jitter to improve capture variation while keeping a safe camera pose.
            target_pose = PoseObject(
                x=self.observation_pose.x + float(np.random.uniform(-0.003, 0.003)),
                y=self.observation_pose.y + float(np.random.uniform(-0.003, 0.003)),
                z=self.observation_pose.z + float(np.random.uniform(-0.002, 0.002)),
                roll=self.observation_pose.roll + float(np.random.uniform(-0.01, 0.01)),
                pitch=self.observation_pose.pitch + float(np.random.uniform(-0.01, 0.01)),
                yaw=self.observation_pose.yaw + float(np.random.uniform(-0.01, 0.01)),
            )
        self.robot.move_pose(target_pose)

    def check_table(self, table0, table):
        # Valid transition when player 2 has just played: exactly one 0 -> 2 change.
        if isinstance(table0, torch.Tensor):
            table0 = table0.detach().cpu().numpy()
        else:
            table0 = np.asarray(table0)

        if isinstance(table, torch.Tensor):
            table = table.detach().cpu().numpy()
        else:
            table = np.asarray(table)

        if table0.shape != (3, 3) or table.shape != (3, 3):
            return False

        if not np.isin(table0, [0, 1, 2]).all() or not np.isin(table, [0, 1, 2]).all():
            return False

        old_values_mask = table0 != 0
        if not np.array_equal(table[old_values_mask], table0[old_values_mask]):
            return False

        diff_mask = table != table0
        if np.count_nonzero(diff_mask) != 1:
            return False

        i, j = np.argwhere(diff_mask)[0]
        return table0[i, j] == 0 and table[i, j] == 2


    def modif_table(self, table): # returns the table detected by the robot
        pred_table = None
        while pred_table is None or not self.check_table(table, pred_table):
            save_path = "current_game"
            os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
            self.cam_pos()
            mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
            img = self.robot.get_img_compressed() # getting image
            img_uncom = uncompress_image(img) # uncompressing image
            img_undis = undistort_image(img_uncom, mtx, dist) # undistort
            crop_l, crop_r, crop_t, crop_b = 140, 30, 100, 230
            width, height = img_undis.shape[0], img_undis.shape[1]
            img_undis = img_undis[crop_t: height - crop_b, crop_l: width - crop_r]
            img_undis = cv2.cvtColor(img_undis, cv2.COLOR_BGR2GRAY)
            # Save with timestamp
            image_name = "current.png"
            cv2.imwrite(os.path.join(save_path, image_name), img_undis)
            image = Image.open(os.path.join(save_path, image_name)).convert('L')
            X = transform(image)
            with torch.no_grad():
                # cv2.imshow("coucou", X.numpy())
                X = X.unsqueeze(0).to(self.device)  # Add batch dimension and move to device
                pred_table = torch.argmax(self.model(X), dim = 1).reshape([3,3]).cpu().numpy()
        return pred_table

    def pos_grid(self,i,j): # BE CAREFUL, THIS FUNCTION IS MADE FOR ME BECAUSE I DONT HAVE THE ORIGINAL CAMERA
        x,x,y,y = 0,0,0,0
        if i==0 :
            if j == 0:
                x,y = 250 , 198
            if j == 1:
                x,y = 356 , 202
            if j == 2:
                x,y = 466 , 201
        if i == 1:
            if j == 0:
                x, y = 259 , 305
            if j == 1:
                x, y = 369 , 308
            if j == 2:
                x, y = 483 , 316
        if i == 2:
            if j == 0:
                x, y = 239 , 443
            if j == 1:
                x, y = 361 , 437
            if j == 2:
                x, y = 486 , 450
        eps = 35
        return [y-eps,y+eps,x-eps,x+eps]

    def pos_grid2(self, i, j): # returns the position in the real space (x,y) of table[i,j] for the original camera
        x,x,y,y = 0,0,0,0
        if i==0 :
            if j == 0:
                x,y =  193 , 139
            if j == 1:
                x,y = 326 , 137
            if j == 2:
                x,y = 454 , 134
        if i == 1:
            if j == 0:
                x, y = 210 , 261
            if j == 1:
                x, y = 325 , 258
            if j == 2:
                x, y = 457 , 261
        if i == 2:
            if j == 0:
                x, y = 199 , 387
            if j == 1:
                x, y = 330 , 392
            if j == 2:
                x, y = 464 , 393
        eps = 35
        return [y-eps,y+eps,x-eps,x+eps]

    def rescaleFrame(self,frame,scale=0.75): # rescale the frame
        width = int(frame.shape[1]*scale)
        height = int(frame.shape[0]*scale)
        dimensions = (width,height)
        return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)

   

    def place(self, i, j):
        self.robot.move_pose(self.home_pos)
        if i == 0:
            if j == 0:
                pos = PoseObject(x = 0.0553, y = -0.3493, z = 0.1060,
                                  roll = 1.463, pitch = 1.533, yaw = -0.121)
            if j == 1:
                pos = PoseObject(x = -0.0038, y = -0.3382, z = 0.1047,
                                 roll = -0.044, pitch = 1.453, yaw = -1.575)
            if j == 2:
                pos = PoseObject(x = -0.0682, y = -0.3479, z = 0.1064,
                                 roll = 2.728, pitch = 1.560, yaw = 1.182)
        if i == 1:
            if j == 0:
                pos = PoseObject(x = 0.0567, y = -0.2814, z = 0.1048,
                                 roll = 0.621, pitch = 1.536, yaw = -0.979
)
            if j == 1:
                pos = PoseObject(x = -0.0047, y = -0.2879, z = 0.1082,
                                  roll = -2.996, pitch = 1.548, yaw = 1.733)
            if j == 2:
                pos = PoseObject(x = -0.0692, y = -0.2817, z = 0.1076,
                                  roll = 0.725, pitch = 1.553, yaw = -0.864)
        if i == 2:
            if j == 0:
                pos = PoseObject(x = 0.0574, y = -0.2201, z = 0.1066,
                                  roll = 1.589, pitch = 1.526, yaw = 0.022)
            if j == 1:
                pos = PoseObject(x = -0.0080, y = -0.2259, z = 0.1080,
                                  roll = 2.469, pitch = 1.545, yaw = 0.927)
            if j == 2:
                pos = PoseObject(x = -0.0700, y = -0.2197, z = 0.1037,
                                  roll = 0.201, pitch = 1.554, yaw = -1.308)
        self.robot.pick_and_place(self.stock,pos)
        self.robot.move_pose(self.home_pos)


    def say_no(self):
        pos1 = []
        pos2 = []
        self.robot.execute_trajectory_from_poses([pos1,pos2])

    def take_picture(self, rd):
        # Play sound to notify that picture is being taken
        
        save_path = "tictactoe_dataset"
        os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
        self.cam_pos(rd=rd)
        time.sleep(0.1)
        mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
        img = self.robot.get_img_compressed() # getting image
        img_uncom = uncompress_image(img) # uncompressing image
        img_undis = undistort_image(img_uncom, mtx, dist) # undistort
        # print(img_undis.shape)
        # crop_l, crop_r, crop_t, crop_b = 140, 30, 100, 230
        # width, height = img_undis.shape[0], img_undis.shape[1]
        # img_undis = img_undis[crop_t: height - crop_b, crop_l: width - crop_r]
        img_undis = cv2.cvtColor(img_undis, cv2.COLOR_BGR2GRAY)
        # Save with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(os.path.join(save_path, f'img_undis_{timestamp}.png'), img_undis)
        pygame.mixer.init()
        pygame.mixer.music.load('Morpion/beep.wav')
        pygame.mixer.music.play()
        time.sleep(0.2)

    
    def take_n_pictures(self, n, rd):
        for i in range(n):
            self.take_picture(rd=rd)
            time.sleep(1.0)
            print("Picture taken || num of the pic: ", i)

if __name__ == '__main__':
    robot1 = Robot()
    robot1.take_n_pictures(100, rd=True)
