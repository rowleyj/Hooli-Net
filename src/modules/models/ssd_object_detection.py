import numpy as np
import cv2
import sys
import imutils
#import local_variables
#from .object_tracking import trackObject
#from modules import hooli_db
#from object_tracking import trackObject
#from .. import hooli_db

def car_detection(INP_VIDEO_PATH, OUT_VIDEO_PATH):
    PROTOTXT = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.prototxt'
    MODEL = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.caffemodel'
    #INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars4.mp4'
    #OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars_detection.mp4'
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
            
    cap = cv2.VideoCapture(INP_VIDEO_PATH)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(OUT_VIDEO_PATH, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
                        10, (frame_width, frame_height))
    sys.path.append("..")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.0035, (260, 260), 46)
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.45:
                idx = int(detections[0, 0, i, 1])
                if (CLASSES[idx] == "car"):                    
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx],confidence*100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),    COLORS[idx], 2)
                    out.write(frame)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grey scale
                    gray = gray[startX:startX + endX,startY:startY + endY]
                    #gray = cv2.resize(gray, (700,700) )
                    #gray = cv2.bilateralFilter(gray, 100, 77, 77) #Blur to reduce noise
                    cv2.imshow('gray',gray)
                    edged = cv2.Canny(gray, 30, 250) #Perform Edge detection
                    #cv2.imshow('edged',edged)
                    # find contours in the edged image, keep only the largest
                    # ones, and initialize our screen contour
                    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)
                    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
                    screenCnt = None

                else:                
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx],confidence*100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),    COLORS[idx], 2)
                    out.write(frame)                
                cv2.imshow('frame', frame)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

#car_detection(INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/platetrim.mp4',
#    OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/plate_detection.mp4')


# function that incorporates object detection with tracking
def carDetectTrack(INP_VIDEO_PATH: str, OUT_VIDEO_PATH: str, debug: bool):
    if debug:
        #video_inp_path = local_variables.detect_track_video_inp_path
        #video_out_path = local_variables.detect_track_video_out_path
        #PROTOTXT = local_variables.prototext_path
        #MODEL = local_variables.model_path
        video_inp_path = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/hwTest/car_speed_40.mp4'
        video_out_path = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/hwTest/cars_detect_track.mp4'
        PROTOTXT = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/MobileNetSSD_deploy.prototxt'
        MODEL = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/MobileNetSSD_deploy.caffemodel'
    
    else:
        video_inp_path = INP_VIDEO_PATH
        video_out_path = OUT_VIDEO_PATH
        PROTOTXT = local_variables.prototext_path
        MODEL = local_variables.model_path

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
            
    cap = cv2.VideoCapture(video_inp_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frameCounter = 0
    carCounter = 0
    
    if debug:
        #out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
        #                    10, (frame_width, frame_height))
        pass
    
    sys.path.append("..")
    
    carTracking = {}
    activeCars = []
    detectedCars = []

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if debug and (cv2.waitKey(1) & 0xFF == ord('q')):
            break

        if debug:
            print("Detect Heartbeat: ", frameCounter)

        # mask detected cars
        maskedFrame = maskDetectedObjects(frame, int(cap.get(1)) - 1, carTracking, activeCars)
        
        h, w = frame.shape[:2]
        #print("frame width: ", w)
        #print("frame height: ", h)
        blob = cv2.dnn.blobFromImage(maskedFrame, 0.0035, (260, 260), 46)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.43:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                bb = (startX, startY, endX-startX, endY-startY)

                if CLASSES[idx] == "car":
                    if debug:
                        currentCarId = carCounter
                    else:
                        currentCarId = hooli_db.dbCreateVehicle(None)
                    
                    #track car and store bounding boxes
                    carTracking[currentCarId] = trackObject(video_inp_path, video_out_path, int(cap.get(1)), bb, currentCarId, False)

                    #add current frame and initial bb
                    carTracking[currentCarId]['boxes'][int(cap.get(1)) - 1] = bb

                    detectedCars.append(currentCarId)
                    activeCars.append(currentCarId)
                    
                    carCounter += 1
        
        if debug:
            '''label = "{}: {:.2f}%".format(CLASSES[idx],confidence*100)
            y = startY - 15 if startY - 15 > 15 else startY + 15'''

            # draw rectangles around cars
            for carId in activeCars:
                #print("current frame: ", int(cap.get(1)) - 1)
                #print("carId: ", carId)
                #print("carTracking: ", carTracking)

                (x, y, w, h) = carTracking[carId]["boxes"][int(cap.get(1)) - 1]

                cv2.rectangle(frame, (x, y), (x+w, y+h), COLORS[idx], 2)
                cv2.rectangle(maskedFrame, (x, y), (x+w, y+h), COLORS[idx], 2)

            # show frame
            #cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            #cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            #out.write(frame)
            cv2.imshow('frame', frame)

            # show masked frame
            #cv2.rectangle(maskedFrame, (startX, startY), (endX, endY), COLORS[idx], 2)
            #cv2.putText(maskedFrame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            cv2.imshow('masked frame', maskedFrame)

            cv2.waitKey(5)

        #clear expired cars
        activeCars = clearExpiredObjects(carTracking, activeCars, int(cap.get(1)))

        frameCounter += 1

    status = False

    if debug:
        #out.release()
        status = True
    else:
        status = writeCarsToDB(video_inp_path, carTracking)
    
    cap.release()
    cv2.destroyAllWindows()

    return status, detectedCars


# function to remove expired objects from the active objects array
def clearExpiredObjects(carTracking, activeObjects, nextFrameNumber: int):
    for objectId in activeObjects:
        currentObject = carTracking[objectId]
        currentObjectEndFrame = currentObject['endFrame']
        
        if nextFrameNumber > currentObjectEndFrame:
            activeObjects.remove(objectId)

    return activeObjects


# function to mask detected cars in frame
def maskDetectedObjects(frame, frameNumber: int, carTracking, activeCars):
    mask = np.ones(frame.shape[:2], dtype="uint8")
    mask = np.multiply(mask, 255)
    
    for carId in activeCars:
        (x, y, w, h) = carTracking[carId]["boxes"][frameNumber]

        cv2.rectangle(mask, (x, y), (x+w, y+h), 0, -1)

    maskedFrame = cv2.bitwise_and(frame, frame, mask=mask)

    return maskedFrame


def writeCarsToDB(inputVideo: str, carTracking) -> bool:
    status = False
    
    for carId in carTracking:
        currentStartFrame = carTracking[carId]["startFrame"]
        currentEndFrame = carTracking[carId]["endFrame"]
        currentBoxes = carTracking[carId]["boxes"]

        status = hooli_db.dbCreateBoundingCube(carId, inputVideo, currentStartFrame, currentEndFrame, currentBoxes)

        if not status:
            return False
        
    return True



if __name__ == "__main__":
    from object_tracking import trackObject
    import hooli_db

    carDetectTrack("", "", True)

else:
    import local_variables
    from .object_tracking import trackObject
    from modules import hooli_db
