from pyniryo import *
import numpy as np
import time
import cv2 as cv

# WARNING : only works with pyniryo==1.1.2




class Robot:

    def __init__(self):
        # connect to the robot when a new Robot object is created
        robot_ip_address = "10.10.10.10"
        robot = NiryoRobot(robot_ip_address)
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(100)
        self.robot = robot
        self.stock = PoseObject(x = -0.0220, y = -0.1308, z = 0.0989,
                                roll = -0.248, pitch = 1.259, yaw = 2.945)  # position of the stock of circles (pieces played by the robot)
        self.observation_pose2 = PoseObject(x = 0.0019, y = -0.2310, z = 0.3170,
                                           roll = -3.046, pitch = 1.204, yaw = 1.689) # DON'T USE THIS, prefer the next one which matches with the original camera
        self.observation_pose = PoseObject(x = -0.0039, y = -0.2469, z = 0.3117,
                                           roll = -2.849, pitch = 1.375, yaw = 1.852) # position adapted to analyse the board
        self.home_pos = PoseObject(x = -0.0003, y = -0.1231, z = 0.1630,
                                   roll = -0.014, pitch = 1.053, yaw = -1.560)



    def cam_pos(self): # the robot moves towards a position from which it can analyse the board game
            self.robot.move_pose(self.observation_pose)

    def init_cam(self): # use it to see what the robot currently sees
        self.cam_pos()
        mtx,dist = self.robot.get_camera_intrinsics() #renvoie: cam intrinsics, distortion coeff
        img = self.robot.get_img_compressed()
        img_uncom = uncompress_image(img)
        img_resize = self.rescaleFrame(img_uncom, scale=1.2)
        img_undis = undistort_image(img_resize, mtx, dist)
        img_gray = cv.cvtColor(img_undis, cv.COLOR_BGR2GRAY)
        print(img_gray.shape)
        print(img_gray)
        while 'User do not press Escapre neither Q':
            #getting image
            img = self.robot.get_img_compressed()
            #uncompressing image
            img_uncom= uncompress_image(img)
            #resize
            img_resize = self.rescaleFrame(img_uncom,scale=1.2)
            #undistort
            img_undis = undistort_image(img_resize,mtx,dist)
            #convert image to greyscale
            img_gray = cv.cvtColor(img_undis,cv.COLOR_BGR2GRAY)
            #apply blur
            img_gblur = cv.GaussianBlur(img_gray,(5,5),0)
            #apply otsu's binaryq
            ret, img_thres = cv.threshold(img_gblur,150,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C) #+ cv.THRESH_OTSU)
            contours, hierarchy = cv2.findContours(image = img_thres, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE ) #ou CHAIN_APPROX_NONE
            image_copy = img_gray.copy()
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if 7000>area >2000:
                    cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                    peri = cv2.arcLength(cnt,True)
                    approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                    print(len(approx))
                    x,y,w,h = cv2.boundingRect(approx)
                    cv2.rectangle(image_copy,(x,y),(x+w,y+h),(0,255,0),5)
            key = show_img("Otsu's Thresh vs Binary to zero", image_copy, wait_ms=30)

            if key in [ord("q")]:  # Will break if user press Q or Escape
                # cv.imwrite("thresh.jpg",img_thres)
                break

    def photo(self): # returns 2 undistort image returned by the robot's camera : the first one is just the conversion of colored image to B&W
                                                                                # the second one is processed to have a white board (rgb = 1,1,1) and black pieces(rgb = 0,0,0)
        self.cam_pos()
        time.sleep(0.5) # avoid problems of pieces detection : let time to the camera to adapt its luminosity
        mtx, dist = self.robot.get_camera_intrinsics() # see Niryo docuentation
        img = self.robot.get_img_compressed()
        img_uncom = uncompress_image(img)
        img_resize = self.rescaleFrame(img_uncom, scale=1.2)
        img_undis = undistort_image(img_resize, mtx, dist)
        img_gray = cv.cvtColor(img_undis, cv.COLOR_BGR2GRAY) # convert image to greyscale
        img_gblur = cv.GaussianBlur(img_gray, (5, 5), 0) # apply blur
        ret, img_thres = cv.threshold(img_gblur, 130, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C)  # apply otsu's binary
        image_copy = img_gray.copy()
        return image_copy,img_thres

    def affiche_contours(self): # displays contours of the pieces

        image_copy,img_thres = self.photo()
        contours, hierarchy = cv2.findContours(image=img_thres, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_SIMPLE)

        Nsquare = 0
        Ncircle = 0
        x,y,w,h = 0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 8000 > area > 2000: # pieces have an area between 8000 and 2000
                cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)
                if area>3000: # squares have an area>3000
                    Nsquare +=1
                else: # squares have an area<3000
                    Ncircle +=1
        image_copy[int(y-10+h/2):int(y+10+h/2),int(x-10+w/2):int(x+10+w/2)]=255
        key = cv2.imshow('MorpionDetection',img_thres)
        cv2.waitKey(0)
        # Destroys all the windows created

    def pos_shape(self):

        image_copy, img_thres = self.photo()
        contours, hierarchy = cv2.findContours(image=img_thres, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_SIMPLE)
        LSpos = []
        LCpos = []
        Nsquare = 0
        Ncircle = 0
        x,y,w,h = 0,0,0,0 # x,y -> min(abscissa) and min(ordinate) of the contour. w,h -> width and height of the contour
        shape = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 8000 > area > 2000: # pieces have an area between 7000 and 2000
                cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 5) # creates a rectangle around the pieces on the image
                if area > 3000 and 8>len(approx)>=4: # detect squares (len(approx) = number of sides of the piece => 4 for a square, but it is sometimes more due to 3D : the robot sees a cuboid
                    LSpos.append([int(y + h / 2), int(x + w/ 2)])
                    Nsquare += 1
                    shape = 'square'
                elif area<=5000 and 6<=len(approx)<=10 : # detect circles
                    LCpos.append([int(y + h / 2), int(x + w/ 2)])
                    shape = 'circle'
                    Ncircle += 1
        return LCpos,LSpos

    def index_pos(self): # returns 2 lists :
        # List of index of circles indexes (LCind) (indexes are between 0 and 2)
        # List of index of squares indexes (LSind) (indexes are between 0 and 2)
        LCpos,LSpos = self.pos_shape()
        LCind, LSind = [],[]
        for pos in LCpos:
            i,j = None,None
            if self.pos_grid(0, 0)[0]<=pos[0]<=self.pos_grid(0, 0)[1] or self.pos_grid(0, 1)[0]<=pos[0]<=self.pos_grid(0, 2)[1] or self.pos_grid(0, 2)[0]<=pos[0]<=self.pos_grid(0, 2)[1]:
                i = 0
            if self.pos_grid(1, 0)[0]<=pos[0]<=self.pos_grid(1, 0)[1] or self.pos_grid(1, 1)[0]<=pos[0]<=self.pos_grid(1, 1)[1] or self.pos_grid(1, 2)[0]<=pos[0]<=self.pos_grid(1, 2)[1]:
                i = 1
            if self.pos_grid(2, 0)[0]<=pos[0]<=self.pos_grid(2, 0)[1] or self.pos_grid(2, 1)[0]<=pos[0]<=self.pos_grid(2, 1)[1] or self.pos_grid(2, 2)[0]<=pos[0]<=self.pos_grid(2, 2)[1]:
                i = 2
            if self.pos_grid(0, 0)[2]<=pos[1]<=self.pos_grid(0, 0)[3] or self.pos_grid(1, 0)[2]<=pos[1]<=self.pos_grid(1, 0)[3] or self.pos_grid(2, 0)[2]<=pos[1]<=self.pos_grid(2, 0)[3]:
                j = 0
            if self.pos_grid(0, 1)[2]<=pos[1]<=self.pos_grid(0, 1)[3] or self.pos_grid(1, 1)[2]<=pos[1]<=self.pos_grid(1, 1)[3] or self.pos_grid(2, 1)[2]<=pos[1]<=self.pos_grid(2, 1)[3]:
                j = 1
            if self.pos_grid(0, 2)[2]<=pos[1]<=self.pos_grid(0, 2)[3] or self.pos_grid(1, 2)[2]<=pos[1]<=self.pos_grid(1, 2)[3] or self.pos_grid(2, 2)[2]<=pos[1]<=self.pos_grid(2, 2)[3]:
                j = 2
            if i!=None and j!=None:
                LCind.append([i,j])
        for pos in LSpos:
            i,j = None,None
            if self.pos_grid(0, 0)[0]<=pos[0]<=self.pos_grid(0, 0)[1] or self.pos_grid(0, 1)[0]<=pos[0]<=self.pos_grid(0, 2)[1] or self.pos_grid(0, 2)[0]<=pos[0]<=self.pos_grid(0, 2)[1]:
                i = 0
            if self.pos_grid(1, 0)[0]<=pos[0]<=self.pos_grid(1, 0)[1] or self.pos_grid(1, 1)[0]<=pos[0]<=self.pos_grid(1, 1)[1] or self.pos_grid(1, 2)[0]<=pos[0]<=self.pos_grid(1, 2)[1]:
                i = 1
            if self.pos_grid(2, 0)[0]<=pos[0]<=self.pos_grid(2, 0)[1] or self.pos_grid(2, 1)[0]<=pos[0]<=self.pos_grid(2, 1)[1] or self.pos_grid(2, 2)[0]<=pos[0]<=self.pos_grid(2, 2)[1]:
                i = 2
            if self.pos_grid(0, 0)[2]<=pos[1]<=self.pos_grid(0, 0)[3] or self.pos_grid(1, 0)[2]<=pos[1]<=self.pos_grid(1, 0)[3] or self.pos_grid(2, 0)[2]<=pos[1]<=self.pos_grid(2, 0)[3]:
                j = 0
            if self.pos_grid(0, 1)[2]<=pos[1]<=self.pos_grid(0, 1)[3] or self.pos_grid(1, 1)[2]<=pos[1]<=self.pos_grid(1, 1)[3] or self.pos_grid(2, 1)[2]<=pos[1]<=self.pos_grid(2, 1)[3]:
                j = 1
            if self.pos_grid(0, 2)[2]<=pos[1]<=self.pos_grid(0, 2)[3] or self.pos_grid(1, 2)[2]<=pos[1]<=self.pos_grid(1, 2)[3] or self.pos_grid(2, 2)[2]<=pos[1]<=self.pos_grid(2, 2)[3]:
                j = 2
            if i!=None and j!=None:
                LSind.append([i,j])
        return LCind,LSind

    def modif_table(self): # returns the table detected by the robot
        table = np.array([[0 for i in range(3)]for i in range(3)])
        LCind,LSind = self.index_pos()
        for L2 in LCind:
            table[L2[0],L2[1]] = 1
        for L2 in LSind:
            table[L2[0],L2[1]] = 2
        return table

    def pos_grid2(self,i,j): # BE CAREFUL, THIS FUNCTION IS MADE FOR ME BECAUSE I DONT HAVE THE ORIGINAL CAMERA
        x,x,y,y = 0,0,0,0
        if i==0 :
            if j == 0:
                x,y = 239 , 80
            if j == 1:
                x,y = 353 , 82
            if j == 2:
                x,y = 484 , 86
        if i == 1:
            if j == 0:
                x, y = 235 , 199
            if j == 1:
                x, y = 357 , 202
            if j == 2:
                x, y = 477 , 205
        if i == 2:
            if j == 0:
                x, y = 239 , 325
            if j == 1:
                x, y = 358 , 323
            if j == 2:
                x, y = 482 , 327
        eps = 35
        return [y-eps,y+eps,x-eps,x+eps]

    def pos_grid(self, i, j): # returns the position in the real space (x,y) of table[i,j] for the original camera
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

    def get_HSV_and_mousePos(self): # useful to set upper and lower bound of red and yellow masks (HSV color) defined in red_yellow_pos()
                                    # also to set x and y in pos_grid(i,j) function
        def on_mouse(event, x, y, flags, param):
            # Check if the event was the left mouse button being clicked
            if event == cv2.EVENT_LBUTTONDOWN:
                # Get the BGR pixel value at the clicked location
                pixel = frame[y, x]

                # Convert BGR to HSV and print the pixel value

                print("pixel pos: (", x, ',', y, ')')
                print()
                # Append the pixel value to the values list
                vals.append(1)

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
        frame = self.photo()[0]
        print(frame.shape)
        vals = []

        while True:
            # Capture frame-by-frame
            frame = self.photo()[0]
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

if __name__ == '__main__':
    robot1 = Robot()
    robot1.affiche_contours()
    #robot1.get_HSV_and_mousePos()
    print(robot1.modif_table())
    print(robot1.robot.get_pose())
    #robot1.place(0,0)
