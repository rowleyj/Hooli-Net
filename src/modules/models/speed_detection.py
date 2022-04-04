# module for all the speed detection functions


#!/usr/bin/env python3


# import libraries
import cv2
import imutils
import numpy as np
#import local_variables
#from .object_tracking import trackObject
#from modules import hooli_db
#from object_tracking import trackObject
#from license_plate_detection import license_reading


# constants
PI_FOCAL_LENGTH = 1049.03
LICENCE_PLATE_WIDTH = 0.315     # width of license plate should be 30.48cm or 31.5 with trims and covers
LICENCE_PLATE_HEIGHT = 0.155
CALIBRATION_DISTANCE = 1
FRAME_RATE = 60                 # since camera can record at 30 frames/second at 1080p


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
def getPixelHeight(frame) -> int:
    (x, y, w, h) = [int(v) for v in frame]
    
    return h


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
def getPlateDistance(frame, focalLength: float) -> float:
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
def getInstantSpeed(frame1, frame2, skippedFrames: int, focalLength: float) -> float:
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
def processFrames(plateTracking):
    # speed tracking gives instantaneos speed of each frame compared to the previous, so no speed for first frame
    
    speedDict = {}
    startFrame = plateTracking["startFrame"]
    endFrame = plateTracking["endFrame"]
    numFrames = endFrame - startFrame

    for i in range(numFrames):
        frame1 = startFrame - 1 + i
        frame2 = startFrame + i

        frame1BB = plateTracking["boxes"][frame1]
        frame2BB = plateTracking["boxes"][frame2]

        speedDict[frame2] = getInstantSpeed(frame1BB, frame2BB, 0, PI_FOCAL_LENGTH)
    
    return speedDict


# function to use license plate detection api to get plate
def detectPlate(frame):
    try:
        plateData = license_reading(None, frame)
        print(plateData)

        plateBox = plateData["results"]["box"]
        x = plateBox["xmin"]
        y = plateBox["ymin"]
        w = plateBox["xmax"] - plateBox["xmin"]
        h = plateBox["ymax"] - plateBox["ymin"]
        plateBB = (x, y, w, h)
    except:
        return False, None
    
    return True, plateBB


# function to warn of oncoming car and possible collision
def warnUser(speed: float):
    if speed > 30.0:
        print("Car Incoming - High Threat")
    elif speed > 20.0:
        print("Car Incoming - Medium Threat")
    elif speed > 10.0:
        print("Car Incoming - Low Threat")
    else:
        print("Car Passing - No Threat")


# function to debug speed detection
def debugSpeedDetection(input_video: str):
    bb = None       #init bounding box coordinates

    videoStream = cv2.VideoCapture(input_video)

    #loop over frames
    while True:
        #get frame
        ret, frame = videoStream.read()
        currentFrameNumber = int(videoStream.get(1)) - 1

        #end of video
        if frame is None:
            break

        (frameHeight, frameWidth) = frame.shape[:2]

        #write speed on frame if bb is not None
        if bb is not None:
            #get current frame's bounding box
            bb = trackedPlate["boxes"][currentFrameNumber]
            (x, y, w, h) = [round(v) for v in bb]

            #draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            #add speed to frame as text
            #print("currentFrameNumber: ", currentFrameNumber)
            #print("carSpeeds", carSpeeds)
            #print("trackedPlate: ", trackedPlate)
            try:
                carInstantSpeed = carSpeeds[currentFrameNumber]
                text = f"Speed: {carInstantSpeed}"
                warnUser(carInstantSpeed)
            except:
                text = "Speed: No speed detected!"
                bb = None
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        #output the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(50) & 0xFF

        #select bb if 's' is clicked or quit if 'q' is clicked
        if key == ord("s"):
            #select bb of object to be tracked
            #press ENTER or SPACE after selecting ROI
            status, bb = detectPlate(frame)
            print(bb)
            #bb = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

            if status:
                #track plate
                trackedPlate = trackObject(input_video, None, currentFrameNumber + 1, bb, 0, False)
                trackedPlate["boxes"][currentFrameNumber] = bb

                #process tracked frames to get speeds
                carSpeeds = processFrames(trackedPlate)
            else:
                print("error getting plate bounding box")
        
        elif key == ord("q"):
            break

    videoStream.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    from object_tracking import trackObject
    from license_plate_detection import license_reading

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
    print(testPlateDistance3)

    piFocalLength = calibrateSystem('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/speed/pi/testpic9.jpg')
    print("Focal Length: ", piFocalLength)'''

    debugSpeedDetection('C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/hwTest/car_speed_25_take2.mp4')

else:
    import local_variables
    from .object_tracking import trackObject
    from modules import hooli_db