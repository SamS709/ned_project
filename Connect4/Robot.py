from pyniryo import *

robot_ip_address = "10.10.10.10"


#Connect to robot & calibrate
robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()
robot.update_tool()
robot.set_arm_max_velocity(100)

class Robot:

    def __init__(self):
        self.stock = PoseObject(1,1,1,1,1,1)

    def place(self,j):
        place_pose = 0
        if j == 0:
            place_pose = PoseObject()
        if j == 1:
            place_pose = PoseObject()
        if j == 2:
            place_pose = PoseObject()
        if j == 3:
            place_pose = PoseObject()
        if j == 4:
            place_pose = PoseObject()
        if j == 5:
            place_pose = PoseObject()
        if j == 6:
            place_pose = PoseObject()

        return place_pose

    def waiting_pos(self):
        robot.move_to_home_pose()

    def celebrate(self,i): #i=1 si le robot a gagné et 2 sinon
        if i == 1:
            pos1 = []
            pos2 = []
            pos3 = []
        if i == 2:
            pos1 = []
            pos2 = []
            pos3 = []
        robot.execute_trajectory_from_poses([pos1, pos2, pos3])

    def get_PosObject(self):
        return robot.get_pose()

if __name__=='__main__':
    robot1 = Robot()
    print(robot1.get_PosObject())