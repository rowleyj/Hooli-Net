# module for all object tracking functions


#!/usr/bin/env python3


# import libraries
from imutils.video import FPS
import cv2
import imutils
import numpy as np
import time
#import local_variables


tracking_video_inp_path =    'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/cars4.mp4'
tracking_video_out_path =    'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/cars_tracking.mp4'

tracker = cv2.TrackerCSRT_create()

initBB = None       #init bounding box coordinates
fps = None          #init fps throughput estimator

videoStream = cv2.VideoCapture(tracking_video_inp_path) #local_variables.tracking_video_inp_path)

#loop over frames
while True:
    #get frame
    ret, frame = videoStream.read()

    #end of video
    if frame is None:
        break

    #resize frame
    #frame = imutils.resize(frame, width=500)
    (frameHeight, frameWidth) = frame.shape[:2]

    #check if initBB is being used (if an object is being tracked)
    if initBB is not None:
        #get new bb corrdinates
        (isSuccessful, box) = tracker.update(frame)

        #check if tracker was successful
        if isSuccessful:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #update fps counter
        fps.update()
        fps.stop()

        #init info to be displayed on frame
        info = [
            ("Success", "Yes" if isSuccessful else "No"),
            ("FPS", f"{fps.fps():.2f}")
        ]

        for (i, (k, v)) in enumerate(info):
            text = f"{k}: {v}"
            cv2.putText(frame, text, (10, h - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    #output the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    #select bb if 's' is clicked or quit if 'q' is clicked
    if key == ord("s"):
        #select bb of object to be tracked
        #press ENTER or SPACE after selecting ROI
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
    
        #start OpenCV tracker using supplied bb
        tracker.init(frame, initBB)

        #start FPS throughput estimator
        fps = FPS().start()
    
    elif key == ord("q"):
        break

videoStream.release()
cv2.destroyAllWindows()