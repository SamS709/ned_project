from pyniryo import *


robot_ip_address = "10.10.10.10"


#Connect to robot & calibrate
robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()
robot.update_tool()
robot.set_arm_max_velocity(100)


class Robot:

    def __init__(self):
        self.stock = PoseObject(x=0.3195, y=-0.1041, z=0.1029,
                                roll=-0.894, pitch=1.529, yaw=-0.883)  # position du stock de cercles

    def place(self, i, j):
        if i == 0:
            if j == 0:
                return PoseObject(x=0.3027, y=0.0458, z=0.1038,
                                  roll=1.793, pitch=1.540, yaw=1.827)
            if j == 1:
                return PoseObject(x=0.3064, y=-0.0038, z=0.1074,
                                  roll=2.066, pitch=1.566, yaw=2.122
                                  )
            if j == 2:
                return PoseObject(x=0.3077, y=-0.0583, z=0.1123,
                                  roll=2.136, pitch=1.526, yaw=2.170)
        if i == 1:
            if j == 0:
                return PoseObject(x=0.2543, y=0.0383, z=0.1051,
                                  roll=1.515, pitch=1.459, yaw=1.485)
            if j == 1:
                return PoseObject(x=0.2525, y=-0.0050, z=0.1059,
                                  roll=2.056, pitch=1.548, yaw=2.067)
            if j == 2:
                return PoseObject(x = 0.2606, y = -0.0542, z = 0.1055, roll = 2.930, pitch = 1.523, yaw = 3.015)
        if i == 2:
            if j == 0:
                return PoseObject(x=0.2055, y=0.0412, z=0.1075,
                                  roll=2.030, pitch=1.495, yaw=2.054
                                  )
            if j == 1:
                return PoseObject(x=0.2066, y=-0.0036, z=0.1087,
                                  roll=-2.502, pitch=1.533, yaw=-2.425)
            if j == 2:
                return PoseObject(x=0.2066, y=-0.0564, z=0.1093,
                                  roll=1.452, pitch=1.523, yaw=1.460
                                  )

    def waiting_pos(self):
        robot.move_to_home_pose()

    def celebrate(self,i):
        if i == 1:
            pos1 = []
            pos2 = []
            pos3 = []
        if i ==2:
            pos1 = []
            pos2 = []
            pos3 = []
        robot.execute_trajectory_from_poses([pos1,pos2,pos3])

    def say_no(self):
        pos1 = []
        pos2 = []
        robot.execute_trajectory_from_poses([pos1,pos2])

if __name__ == '__main__':
    robot1 = Robot()
    #robot.move_to_home_pose()
    p = robot.get_pose()
    j = robot.get_joints()
    print(p)
    print(j)
    #robot.pick_and_place(robot1.stock,robot1.place(1,2))