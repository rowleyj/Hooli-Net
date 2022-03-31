# module for all the speed detection functions


#!/usr/bin/env python3


# import libraries
import cv2
import imutils
import numpy as np


# constants
PI_FOCAL_LENGTH = 1049.03
LICENCE_PLATE_WIDTH = 0.315     # width of license plate should be 30.48cm or 31.5 with trims and covers
LICENCE_PLATE_HEIGHT = 0.155
CALIBRATION_DISTANCE = 1
FRAME_RATE = 30                 # since camera can record at 30 frames/second at 1080p


# function to select license plate in an image
def selectLicensePlate(frame: str):
    image = cv2.imread(frame)
    
    bb = cv2.selectROI("Frame", image, fromCenter=False, showCrosshair=True)
    '''print(bb)
    print(type(bb))'''
    return bb


# function to find license plate pixel width
def getPixelWidth(frame: str) -> int:
    licensePlateBB = selectLicensePlate(frame)

    if licensePlateBB != None:
        (x, y, w, h) = [int(v) for v in licensePlateBB]
        '''print(x)
        print(y)
        print(w)
        print(h)
        print("w:")
        print(licensePlateBB[2])'''
        return w

    print("Error reading bb!")


# function to find license plate pixel width
def getPixelHeight(frame: str) -> int:
    licensePlateBB = selectLicensePlate(frame)

    if licensePlateBB != None:
        (x, y, w, h) = [int(v) for v in licensePlateBB]
        '''print(x)
        print(y)
        print(w)
        print(h)
        print("w:")
        print(licensePlateBB[2])'''
        return h

    print("Error reading bb!")


# function to get camera's perceived focal length
def getFocalLength(frame: str, distance: float, width: float) -> float:
    '''
        @param      {str}   frame - path to frame with outlined licence plate
        @param      {float} distance - actual distance from control object to camera in meters
        @param      {float} width - actual width of control object in meters
        
        @returns    {float} focalLength - preceived focal length
    '''
    
    pixelWidth = getPixelWidth(frame)

    return (pixelWidth * distance) / width


# function to get estimated plate distance from camera
def getPlateDistance(frame: str, focalLength: float) -> float:
    '''
        @param      {str}   frame - path to frame with outlined licence plate
        @param      {float} focalLength - preceived focal length

        @returns    {float} distance - estimated distance from plate to camera in meters
    '''

    pixelHeight = getPixelHeight(frame)   #in px
    
    return (LICENCE_PLATE_HEIGHT * focalLength) / pixelHeight


# function to get focal length from calibration with plate 1m away from camera
def calibrateSystem(frame: str) -> float:
    return getFocalLength(frame, CALIBRATION_DISTANCE, LICENCE_PLATE_WIDTH)


# function to get instatnaneous relative speed by comparing distance in 2 frames
def getInstantSpeed(frame1: str, frame2: str, skippedFrames: int, focalLength: float) -> float:
    '''
        @param      {str}   frame1 - first frame of the 2 frames that need to be compared, order matters
        @param      {str}   frame2 - second frame of the 2 frames that need to be compared, order matters
        @param      {int}   skippedFrames - number of frames skipped between frame1 and frame2, zero is valid
        @param      {float} focalLength - preceived focal length based on calibration image

        @returns    {float} instantSpeedKpH - instantanous relative speed in km/h
    ''' 
    
    distance1 = getPlateDistance(frame1, focalLength)
    distance2 = getPlateDistance(frame2, focalLength)

    instantSpeed = (distance1 - distance2) / ((skippedFrames + 1) * (1 / FRAME_RATE))
    instantSpeedKpH = instantSpeed * 3.6    #to convert speed from m/s to km/h

    return instantSpeedKpH


# function to process frames and get speeds
def processFrames():
    pass


# function to warn of oncoming car and possible collision
def warnUser(threatLevel: int):
    pass


if __name__ == "__main__":
    '''iPhoneFocalLength = calibrateSystem('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/iphone_calibrate_1m.jpeg')
    print("Focal Length:")
    print(iPhoneFocalLength)

    testPlateDistance1 = getPlateDistance('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/IMG_0408.jpeg', iPhoneFocalLength) #should be 1m
    print("Test Plate 1 Distance (1.0m expected):")
    print(testPlateDistance1)

    testPlateDistance2 = getPlateDistance('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/IMG_0409.jpeg', iPhoneFocalLength) #should be 1.5m
    print("Test Plate 2 Distance (1.5m expected):")
    print(testPlateDistance2)

    testPlateDistance3 = getPlateDistance('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/IMG_0410.jpeg', iPhoneFocalLength) #should be 2m
    print("Test Plate 3 Distance (2.0m expected):")
    print(testPlateDistance3)'''

    piFocalLength = calibrateSystem('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/pi/testpic9.jpg')
    print("Focal Length: ", piFocalLength)