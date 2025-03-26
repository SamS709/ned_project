import time

import numpy as np
import cv2
from pyniryo import *
from Robot import robot


class Camera:

    def __init__(self):
        pass

    def cam_pos(self, i=1):
        if i == 1:
            robot.move_pose(PoseObject(
                x=0.2032, y=0.00, z=0.3231,
                roll=-3.140, pitch=1.234, yaw=-3.140
            ))
        else:
            robot.move_pose(PoseObject(x = 0.1346, y = 0.0077, z = 0.2262,
                                       roll = -0.014, pitch = 0.292, yaw = 0.056))

    def home_pos(self):
        robot.move_to_home_pose()

    def red_yellow_pos(self):
        self.cam_pos(2)
        time.sleep(0.5)
        mtx,dist = robot.get_camera_intrinsics() #renvoie: cam intrinsics, distortion coeff
        # getting image
        img = robot.get_img_compressed()
        # uncompressing image
        img_uncom = uncompress_image(img)
        # resize
        # undistort
        img_undis = undistort_image(img_uncom, mtx, dist)
        # turn on cam

        # while(1):
        imageFrame = img_undis

        # Convert BGR to HSV colorspace
        hsvFrame = cv2.cvtColor(img_undis, cv2.COLOR_BGR2HSV)

        # Set range for red color
        red_lower1 = np.array([0, 100, 100], np.uint8)
        red_upper1 = np.array([10, 255, 255], np.uint8)
        red_lower2 = np.array([165, 100, 75], np.uint8)
        red_upper2 = np.array([180, 255, 255], np.uint8)

        red_mask1 = cv2.inRange(hsvFrame, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsvFrame, red_lower2, red_upper2)


        yellow_lower = np.array([10,100,80], np.uint8)
        yellow_upper = np.array([30,255,255], np.uint8)

        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        # red color
        red_mask1 = cv2.dilate(red_mask1, kernal)
        res_red1 = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask1)
        red_mask2 = cv2.dilate(red_mask2, kernal)
        res_red2 = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask2)

        #yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(imageFrame, imageFrame, mask=yellow_mask)

        L_pos_red = np.array([[0, 0]])
        L_pos_yellow = np.array([[0, 0]])

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                L_pos_red = np.concatenate((L_pos_red,np.array([[int(x+w/2),int(y+h/2)]])))
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 0, 255), 2)

                cv2.putText(imageFrame, "Red", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        contours, hierarchy = cv2.findContours(red_mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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


        contours, hierarchy = cv2.findContours(yellow_mask,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 100):
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

    def show_image(self):
        imageFrame = self.red_yellow_pos()[0]
        cv2.imshow("Color Detection", imageFrame)
        cv2.waitKey(0)

    def pos_grid(self,i,j):  # IL FAUT REPERER LES POSITIONS SUR LA CAMERA
        #(on peut s'aider de red_green_pos et rajouter une barre d'incertitude en pernant une photo de la grille remplie de pions rouges par exemple)
        x0,x1,y0,y1 = 0,0,0,0
        eps = 20
        if i == 0:
            if j == 0:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 1:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 2:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 3:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 4:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 5:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 6:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps
            if j == 7:
                x = 0
                y = 0
                x0,x1 = x-eps,x+eps
                y0,y1 = y-eps,y+eps

        return [x0,x1,y0,y1 ]

    def modif_table(self):
        imageFrame,Lposred,Lposgreen = self.red_yellow_pos()
        table = np.array([[0 for i in range(7)]for i in range(6)])
        for pos in Lposred:
            for i in range(6):
                for j in range(7):
                    if self.pos_grid(i,j)[0]<=pos[0]<= self.pos_grid(i,j)[1] and self.pos_grid(i,j)[2]<=pos[1]<= self.pos_grid(i,j)[3]:
                        table[i,j]=1
        for pos in Lposgreen:
            for i in range(6):
                for j in range(7):
                    if self.pos_grid(i,j)[0]<=pos[0]<= self.pos_grid(i,j)[1] and self.pos_grid(i,j)[2]<=pos[1]<= self.pos_grid(i,j)[3]:
                        table[i,j]=2
        return table


    def get_HSV_and_mousePos(self):
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

if __name__=='__main__':
    camera = Camera()
    print(robot.get_pose())
    camera.get_HSV_and_mousePos()
    #imageFrame,Lposred,Lposgreen=camera.red_green_pos()
    '''print('Lposred=',Lposred)
    print('Lposgreen=', Lposgreen)'''
    '''grid=camera.modif_table()
    print(grid)'''