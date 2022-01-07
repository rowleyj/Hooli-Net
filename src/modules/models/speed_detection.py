# module for all the speed detection functions


#!/usr/bin/env python3


# import libraries
import cv2
import imutils
import numpy as np



# function to find license plate pixel width
def getPixelWidth(frame: str) -> int:
    pass


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


# width of license plate should be 30.48cm or 31.5 with trims and covers

# function to get estimated plate distance from camera
def getPlateDistance(frame: str, focalLength: float) -> float:
    '''
        @param      {str}   frame - path to frame with outlined licence plate
        @param      {float} focalLength - preceived focal length

        @returns    {float} distance - estimated distance from plate to camera in meters
    '''

    plateWidth = 0.315                  #in meters
    pixelWidth = getPixelWidth(frame)   #in px
    
    return (plateWidth * focalLength) / pixelWidth


# function to get focal length from calibration with plate 1m away from camera
def calibrateSystem(frame: str) -> float:
    return getFocalLength(frame, 1, 0.315)


# function to get instatnaneous relative speed by comparing distance in 2 frames
def getInstantSpeed(frame1: str, frame2: str, skippedFrames: int, focalLength: float) -> float:
    '''
        @param      {str}   frame1 - first frame of the 2 frames that need to be compared, order matters
        @param      {str}   frame2 - second frame of the 2 frames that need to be compared, order matters
        @param      {int}   skippedFrames - number of frames skipped between frame1 and frame2, zero is valid
        @param      {float} focalLength - preceived focal length based on calibration image

        @returns    {float} instantSpeedKpH - instantanous relative speed in km/h
    '''

    frameRate = 30      #since camera can record at 30 frames/second at 1080p
    
    distance1 = getPlateDistance(frame1, focalLength)
    distance2 = getPlateDistance(frame2, focalLength)

    instantSpeed = (distance1 - distance2) / ((skippedFrames + 1) * (1 / frameRate))
    instantSpeedKpH = instantSpeed * 3.6    #to convert speed from m/s to km/h

    return instantSpeedKpH


if __name__ == "__main__":
    pass