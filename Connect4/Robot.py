from pyniryo import *
import time
import numpy as np
import cv2

class Robot:

    def __init__(self):
        # connect to the robot when a new Robot object is created
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

    def cam_pos(self): # the robot moves towards a position from which it can analyse the board game
        self.robot.move_pose(PoseObject(x = 0.1320, y = 0.0052, z = 0.2225,
                                            roll = -0.040, pitch = 0.273, yaw = 0.034))


    def red_yellow_pos(self): # returns the image frame, a list of red pieces positions and a list of yellow pieces positions
        self.cam_pos()
        time.sleep(1)  # avoid problems of pieces detection : let time to the camera to adapt its luminosity
        mtx,dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
        img = self.robot.get_img_compressed() # getting image
        img_uncom = uncompress_image(img) # uncompressing image
        img_undis = undistort_image(img_uncom, mtx, dist) # undistort
        imageFrame = img_undis
        # Convert BGR to HSV colorspace
        hsvFrame = cv2.cvtColor(img_undis, cv2.COLOR_BGR2HSV)

        # Set range for red color
        red_lower = np.array([165, 100, 75], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        # Set range for yellow color
        yellow_lower = np.array([10,100,80], np.uint8)
        yellow_upper = np.array([30,255,255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        # red color
        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

        #yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(imageFrame, imageFrame, mask=yellow_mask)

        L_pos_red = np.array([[0, 0]])
        L_pos_yellow = np.array([[0, 0]])

        # Creating contour to track red color

        contours, hierarchy = cv2.findContours(red_mask,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                L_pos_red = np.concatenate((L_pos_red, np.array([[int(x + w / 2), int(y + h / 2)]])))
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 0, 255), 2)

                cv2.putText(imageFrame, "Red", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        # Creating contour to track yellow color

        contours, hierarchy = cv2.findContours(yellow_mask,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                L_pos_yellow = np.concatenate((L_pos_yellow,np.array([[int(x+w/2),int(y+h/2)]])))
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 255), 2)

                cv2.putText(imageFrame, "Yellow", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 255))

        L_pos_red = L_pos_red[1:,:]
        L_pos_yellow = L_pos_yellow[1:,:]

        return imageFrame, L_pos_red, L_pos_yellow

    def show_image(self): # to show the image returned by red_yellow_pos
        imageFrame = self.red_yellow_pos()[0]
        cv2.imshow("Color Detection", imageFrame)
        cv2.waitKey(0)

    def pos_grid(self,i,j): # returns the position in the real space (x,y) of table[i,j]
        x0,x1,y0,y1 = 0,0,0,0
        eps = 30
        if i == 0:
            if j == 0:
                x,y= 50 , 134
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y= 147 , 133
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y=242 , 130
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y =329 , 131
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y =418 , 130
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 512 , 127
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 604 , 122
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
        if i == 1:
            if j == 0:
                x,y=55 , 199
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y=152 , 197
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y= 245 , 199
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y = 332 , 197
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y = 423 , 197
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 513 , 193
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 600 , 189
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
        if i == 2:
            if j == 0:
                x,y= 61 , 264
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y= 156 , 261
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y= 247 , 261
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y = 336 , 258
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y = 424 , 262
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 509 , 257
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 596 , 254
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
        if i == 3:
            if j == 0:
                x,y= 62 , 329
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y= 156 , 328
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y= 247 , 325
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y = 336 , 324
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y = 425 , 323
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 510 , 324
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 593 , 317
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
        if i == 4:
            if j == 0:
                x,y= 69 , 389
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y= 162 , 390
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y= 249 , 389
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y = 337 , 388
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y = 422 , 386
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 510 , 383
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 595 , 379
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
        if i == 5:
            if j == 0:
                x,y= 71 , 449
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x,y= 160 , 448
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x,y= 249 , 445
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x, y = 335 , 446
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x, y = 424 , 443
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x, y = 506 , 441
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x, y = 588 , 436
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps

        return [x0,x1,y0,y1 ]

    def modif_table(self): # returns the table (2d numpy array 6*7) detected by the robot
        imageFrame,Lposred,Lposyellow = self.red_yellow_pos()
        table = np.array([[0 for i in range(7)]for i in range(6)])
        for pos in Lposred:
            for i in range(6):
                for j in range(7):
                    if self.pos_grid(i,j)[0]<=pos[0]<= self.pos_grid(i,j)[1] and self.pos_grid(i,j)[2]<=pos[1]<= self.pos_grid(i,j)[3]:
                        table[i,j]=1
        for pos in Lposyellow:
            for i in range(6):
                for j in range(7):
                    if self.pos_grid(i,j)[0]<=pos[0]<= self.pos_grid(i,j)[1] and self.pos_grid(i,j)[2]<=pos[1]<= self.pos_grid(i,j)[3]:
                        table[i,j]=2
        return table


    def get_HSV_and_mousePos(self): # useful to set upper and lower bound of red and yellow masks (HSV color) defined in red_yellow_pos()
                                    # also to set x and y in pos_grid(i,j) function
        def on_mouse(event, x, y, flags, param):
            # Check if the event was the left mouse button being clicked
            if event == cv2.EVENT_LBUTTONDOWN:
                # Get the BGR pixel value at the clicked location
                pixel = frame[y, x]

                # Convert BGR to HSV and print the pixel value
                hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
                print("HSV:", hsv_pixel[0][0])
                print("pixel pos: (", x, ',', y, ')')
                print()
                # Append the pixel value to the values list
                vals.append(hsv_pixel[0][0])

        def get_thresh_from_vals(vals: np.array) -> np.array:
            # Calculate the minimum and maximum values for each channel
            min_h, min_s, min_v = np.min(vals, axis=0)
            max_h, max_s, max_v = np.max(vals, axis=0)
            lower_color = [min_h, min_s, min_v]
            upper_color = [max_h, max_s, max_v]
            # Output the results
            print(f"lower bound: {lower_color}")
            print(f"upper bound: {upper_color}")
            return lower_color, upper_color
        # Open a connection to the webcam (you may need to change the index)
        frame = self.red_yellow_pos()[0]
        print(frame.shape)
        vals = []

        while True:
            # Capture frame-by-frame
            frame = self.red_yellow_pos()[0]
            # Display the frame
            cv2.imshow('frame', frame)

            # Set the callback function for mouse events
            cv2.setMouseCallback('frame', on_mouse)  # Make sure 'Frame' matches the window name in cv2.imshow
            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        # Release the capture when everything is done
        cv2.destroyAllWindows()
        low, up = get_thresh_from_vals(vals)

    def place(self, j): # robot moves to puta piece in the j-th column

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


    def say_no(self):
        pos1 = [0.1271,-0.0404,0.2085,-0.122, 0.333,-0.305]
        pos2 = [0.1276, 0.0350,0.2117,-0.086,0.359,0.294]
        self.robot.set_arm_max_velocity(100)
        self.robot.execute_trajectory_from_poses([pos1, pos2,pos1,pos2])



if __name__=='__main__':

    robot1 = Robot()
    for j in range(7):
        robot1.place(j)
