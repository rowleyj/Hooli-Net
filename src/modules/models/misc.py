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
    cv2.imshow('origial',img)

    key = cv2.waitKey(0)
    
    img = img[y:(y+h), x:(x+w)]
    cv2.imshow('croppeded',img)

    key = cv2.waitKey(0)