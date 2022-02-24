#!/usr/bin/env python3

import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
#import local_variables


def selectCar(frame:str):
    image = cv2.imread(frame)
    
    bb = cv2.selectROI("Frame", image, fromCenter=False, showCrosshair=True)
    
    return bb


if __name__ == "__main__":
    frame = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/plates/platevid2.png'
    
    bb = selectCar(frame)
    (x, y, w, h) = [int(v) for v in bb]
    
    img = cv2.imread(frame,cv2.IMREAD_COLOR)
    #cv2.imshow('origial',img)
    
    img = img[y:(y+h), x:(x+w)]
    #cv2.imshow('croppeded',img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 100, 77, 77) #Blur to reduce noise
    #cv2.imshow('gray',gray)
    edged = cv2.Canny(gray, 30, 250) #Perform Edge detection
    #cv2.imshow('edged',edged)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(cnts)
    
    cnts = imutils.grab_contours(cnts)
    #print(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    #print(cnts)
    screenCnt = None

    for c in cnts:
        for eps in np.linspace(0.001, 0.05, 20):
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, eps * peri, True)
            # draw the approximated contour on the image
            output = img.copy()
            cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
            cv2.imshow("Approximated Contour", output)
            if len(approx) == 5:
                screenCnt = approx

    key = cv2.waitKey(0)