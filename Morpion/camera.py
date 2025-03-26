import cv2
import numpy as np
import math
import time
import cv2 as cv
from pyniryo import *
from Morpion.Robot import robot





class Camera:

    def __init__(self):
        self.observation_pose = PoseObject(
            x=0.2032, y=0.00, z=0.3231,
        roll = -3.140, pitch = 1.234, yaw = -3.140
        )
        self.Lhide = []
        self.grid = np.array([[0 for i in range(3)]for i in range(3)])


    def cam_pos(self):
            robot.move_pose(PoseObject(
                x=0.2032, y=0.00, z=0.3231,
            roll = -3.140, pitch = 1.234, yaw = -3.140
            ))

    def home_pos(self):
        robot.move_to_home_pose()

    def init_cam(self):
        self.cam_pos()
        mtx,dist = robot.get_camera_intrinsics() #renvoie: cam intrinsics, distortion coeff
        img = robot.get_img_compressed()
        img_uncom = uncompress_image(img)
        img_resize = self.rescaleFrame(img_uncom, scale=1.2)
        img_undis = undistort_image(img_resize, mtx, dist)
        img_gray = cv.cvtColor(img_undis, cv.COLOR_BGR2GRAY)
        print(img_gray.shape)
        print(img_gray)
        while 'User do not press Escapre neither Q':
            #getting image
            img = robot.get_img_compressed()

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
            ret, img_thres = cv.threshold(img_gblur,180,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C) #+ cv.THRESH_OTSU)
            #ret, img_thres1 = cv.threshold(img_gblur,127,255,cv.THRESH_TOZERO_INV)
            # masking a part of the image:
            h, w = img_thres.shape
            img_thres[0:h, 0:220] = 1
            img_thres[0:h, 515:w] = 1
            img_thres[0:68, 0:w] = 1
            img_thres[360:h, 0:w] = 1

            contours, hierarchy = cv2.findContours(image = img_thres, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE ) #ou CHAIN_APPROX_NONE

            img_gray[0:h, 0:220] = 1
            img_gray[0:h, 515:w] = 1
            img_gray[0:68, 0:w] = 1
            img_gray[360:h, 0:w] = 1
            #img_gray[self.square(1,1)[0]:self.square(1,1)[1],self.square(1,1)[2]:self.square(1,1)[3]]=1
            #img_gray[self.square(0, 1)[0]:self.square(0, 1)[1], self.square(0, 1)[2]:self.square(0, 1)[3]] = 1
            #img_gray[101:181, 261:340] = 1
            #img_gray[101:181, 340:421] = 1
            #img_gray[101:181,421:505] = 1
            #img_gray[181:260, 261:340] = 1
            #img_gray[181:260, 340:421] = 1
            #img_gray[181:260, 421:505] = 1
            #img_gray[260:342,261:340] = 1
            #img_gray[260:342, 340:421] = 1
            #img_gray[260:342, 421:505] = 1
            image_copy = img_gray.copy()
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if 6500>area >2000:
                    cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                    peri = cv2.arcLength(cnt,True)
                    approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                    print(len(approx))
                    x,y,w,h = cv2.boundingRect(approx)
                    cv2.rectangle(image_copy,(x,y),(x+w,y+h),(0,255,0),5)

            #concat = concat_imgs((img_undis , image_copy))
            key = show_img("Otsu's Thresh vs Binary to zero", image_copy, wait_ms=30)

            if key in [ord("q")]:  # Will break if user press Q or Escape
                # cv.imwrite("thresh.jpg",img_thres)
                break

    def photo(self):
        self.cam_pos()
        time.sleep(0.5)
        mtx, dist = robot.get_camera_intrinsics()
        # getting image
        img = robot.get_img_compressed()

        # uncompressing image
        img_uncom = uncompress_image(img)

        # resize
        img_resize = self.rescaleFrame(img_uncom, scale=1.2)

        # undistort
        img_undis = undistort_image(img_resize, mtx, dist)
        # convert image to greyscale
        img_gray = cv.cvtColor(img_undis, cv.COLOR_BGR2GRAY)
        # apply blur
        img_gblur = cv.GaussianBlur(img_gray, (5, 5), 0)

        # apply otsu's binaryq
        ret, img_thres = cv.threshold(img_gblur, 100, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C)  # + cv.THRESH_OTSU)
        # ret, img_thres1 = cv.threshold(img_gblur,127,255,cv.THRESH_TOZERO_INV)
        # masking a part of the image:
        h, w = img_thres.shape
        img_thres[0:h, 0:220] = 1
        img_thres[0:h, 515:w] = 1
        img_thres[0:70, 0:w] = 1
        img_thres[360:h, 0:w] = 1

        img_gray[0:h, 0:220] = 1
        img_gray[0:h, 515:w] = 1
        img_gray[0:70, 0:w] = 1
        img_gray[360:h, 0:w] = 1
        '''
        for ind in self.Lhide:
            y0,y1,x0,x1 = self.square(ind[0],ind[1])[0],self.square(ind[0],ind[1])[1],self.square(ind[0],ind[1])[2],self.square(ind[0],ind[1])[3]
            img_thres[y0:y1,x0:x1]=1
            img_gray[y0:y1,x0:x1] = 1
        '''
        image_copy = img_gray.copy()
        return image_copy,img_thres

    def affiche_contours(self):

        image_copy,img_thres = self.photo()
        contours, hierarchy = cv2.findContours(image=img_thres, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_SIMPLE)  # ou CHAIN_APPROX_NONE

        Nsquare = 0
        Ncircle = 0
        x,y,w,h = 0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 5200 > area > 2000:
                cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)
                if area>3000:
                    Nsquare +=1
                else:
                    Ncircle +=1
        image_copy[int(y-10+h/2):int(y+10+h/2),int(x-10+w/2):int(x+10+w/2)]=255
        # concat = concat_imgs((img_undis , image_copy))
        key = cv2.imshow('coucou',image_copy)
        cv2.waitKey(0)
        # Destroys all the windows created

    def pos_shape(self):

        image_copy, img_thres = self.photo()
        contours, hierarchy = cv2.findContours(image=img_thres, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_SIMPLE)  # ou CHAIN_APPROX_NONE
        LSpos = []
        LCpos = []
        Nsquare = 0
        Ncircle = 0
        x,y,w,h = 0,0,0,0
        shape = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 6500 > area > 2000:
                cv2.drawContours(image=image_copy, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=2,
                                 lineType=cv2.LINE_4)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                print(len(approx))
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)
                if area > 3300 and 8>len(approx)>=4:
                    LSpos.append([int(y + h / 2), int(x + w/ 2)])
                    Nsquare += 1
                    shape = 'square'
                elif area<=3300 and 6<=len(approx)<=10 :
                    LCpos.append([int(y + h / 2), int(x + w/ 2)])
                    shape = 'circle'
                    Ncircle += 1
        return LCpos,LSpos

    def index_pos(self):
        LCpos,LSpos = self.pos_shape()
        LCind, LSind = [],[]
        for pos in LCpos:
            i,j = None,None
            if self.square(0,0)[0]<=pos[0]<=self.square(0,0)[1] or self.square(0,1)[0]<=pos[0]<=self.square(0,2)[1] or self.square(0,2)[0]<=pos[0]<=self.square(0,2)[1]:
                i = 0
            if self.square(1,0)[0]<=pos[0]<=self.square(1,0)[1] or self.square(1,1)[0]<=pos[0]<=self.square(1,1)[1] or self.square(1,2)[0]<=pos[0]<=self.square(1,2)[1]:
                i = 1
            if self.square(2,0)[0]<=pos[0]<=self.square(2,0)[1] or self.square(2,1)[0]<=pos[0]<=self.square(2,1)[1] or self.square(2,2)[0]<=pos[0]<=self.square(2,2)[1]:
                i = 2
            if self.square(0,0)[2]<=pos[1]<=self.square(0,0)[3] or self.square(1,0)[2]<=pos[1]<=self.square(1,0)[3] or self.square(2,0)[2]<=pos[1]<=self.square(2,0)[3]:
                j = 0
            if self.square(0,1)[2]<=pos[1]<=self.square(0,1)[3] or self.square(1,1)[2]<=pos[1]<=self.square(1,1)[3] or self.square(2,1)[2]<=pos[1]<=self.square(2,1)[3]:
                j = 1
            if self.square(0,2)[2]<=pos[1]<=self.square(0,2)[3] or self.square(1,2)[2]<=pos[1]<=self.square(1,2)[3] or self.square(2,2)[2]<=pos[1]<=self.square(2,2)[3]:
                j = 2
            if i!=None and j!=None:
                LCind.append([i,j])
        for pos in LSpos:
            i,j = None,None
            if self.square(0,0)[0]<=pos[0]<=self.square(0,0)[1] or self.square(0,1)[0]<=pos[0]<=self.square(0,2)[1] or self.square(0,2)[0]<=pos[0]<=self.square(0,2)[1]:
                i = 0
            if self.square(1,0)[0]<=pos[0]<=self.square(1,0)[1] or self.square(1,1)[0]<=pos[0]<=self.square(1,1)[1] or self.square(1,2)[0]<=pos[0]<=self.square(1,2)[1]:
                i = 1
            if self.square(2,0)[0]<=pos[0]<=self.square(2,0)[1] or self.square(2,1)[0]<=pos[0]<=self.square(2,1)[1] or self.square(2,2)[0]<=pos[0]<=self.square(2,2)[1]:
                i = 2
            if self.square(0,0)[2]<=pos[1]<=self.square(0,0)[3] or self.square(1,0)[2]<=pos[1]<=self.square(1,0)[3] or self.square(2,0)[2]<=pos[1]<=self.square(2,0)[3]:
                j = 0
            if self.square(0,1)[2]<=pos[1]<=self.square(0,1)[3] or self.square(1,1)[2]<=pos[1]<=self.square(1,1)[3] or self.square(2,1)[2]<=pos[1]<=self.square(2,1)[3]:
                j = 1
            if self.square(0,2)[2]<=pos[1]<=self.square(0,2)[3] or self.square(1,2)[2]<=pos[1]<=self.square(1,2)[3] or self.square(2,2)[2]<=pos[1]<=self.square(2,2)[3]:
                j = 2
            if i!=None and j!=None:
                LSind.append([i,j])
        return LCind,LSind

    def modif_table(self):
        table = np.array([[0 for i in range(3)]for i in range(3)])
        LCind,LSind = self.index_pos()
        for L2 in LCind:
            table[L2[0],L2[1]] = 1
        for L2 in LSind:
            table[L2[0],L2[1]] = 2
        return table


    def square(self,i,j):
        x0,x1,y0,y1 = 0,0,0,0
        if i==0 :
            y0,y1= 101, 181
        if i ==1:
            y0, y1 = 181, 260
        if i == 2:
            y0, y1 = 260, 342
        if j == 0:
            x0,x1 = 261,340
        if j == 1:
            x0,x1 = 340,421
        if j==2:
            x0,x1 = 421,505
        return [y0,y1,x0,x1]

    def rescaleFrame(self,frame,scale=0.75):
        width = int(frame.shape[1]*scale)
        height = int(frame.shape[0]*scale)
        dimensions = (width,height)
        return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)




if __name__ == "__main__":
    A = robot.get_pose()
    #robot1.dance1()
    print(A)


