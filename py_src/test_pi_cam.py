#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
test_cam.py

This script is intended to acquire
images from a Raspberry Pi
camera, save them, and report faults

NOTE: THIS IS NOT YET SUPPORTED AND MAY
REQUIRE MODIFICATION TO BE FUNCTIONAL
'''

#############################################################
#IMPORT MODULES
#############################################################
import os
import sys
import csv
import time
import psutil
import cv2
from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera


#############################################################
# SUPPORT FUNCTIONS
#############################################################
def cam_test(data_dirname):

    #define inputs
    time_interval  = 1 #sec
    ttime=[]

    #allocate available mem
    print('starting cam monitor!')
    
    upsets=[]

    start = time.time()
    # initialize the camera
    #cam = cv2.VideoCapture(0)   # 0 -> index of camera
    camera = PiCamera()
    
    while True:
        
        end = time.time()
        
        ttime+=[time.time()]

        if end-start > time_interval:

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            try:
                camera.start_preview(fullscreen=False, window=(100,200,800,800))
                time.sleep(1)
                camera.capture(os.path.join(data_dirname , now+"_img.jpg")) #save image
                print("image captured")
                camera.stop_preview()
                upsets+=[0]
            except:
                print("cam not read")
                upsets+=[1]

            '''
            #s, img = cam.read()
            if True:
                cv2.namedWindow("cam-test")
                cv2.imshow("cam-test",img)
                waitKey(0)
                print("image captured")
                time.sleep(1)
                destroyWindow("cam-test")

                imwrite(os.path.join(data_dirname , now+"_img.jpg",img)) #save image
                upsets+=[0]
            else :
                print("cam not read")
                upsets+=[1]
            '''
                
            time1 = time.time()

            data = {'time':ttime,'upsets':upsets}

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            #write stuff
 
            with open(os.path.join(data_dirname , now+'cam_log.csv'),'w', newline='') as csv_file:
                 writer=csv.writer(csv_file)
                 writer.writerow(keys)  
                 writer.writerows(zip(*[data[key] for  key in keys]))

            #reset vars
            ttime=[]
            upsets=[]


            #reset time
            start = time.time()


#############################################################
# MAIN CODE
#############################################################
if __name__ == '__main__':

    try:
        data_dirname = sys.argv[1]
    except:
        data_dirname = '../data/demo'
    if os.path.exists(os.path.join(data_dirname)):
        pass
    else:
        os.makedirs(os.path.join(data_dirname))
    #print(data_dirname)
    cam_test(data_dirname)




