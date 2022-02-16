import numpy as np
import cv2
import sys
import imutils
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\tnaguib\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import local_variables
from .object_tracking import trackObject

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


                    for c in cnts:
                        for eps in np.linspace(0.001, 0.05, 15):
                            # approximate the contour
                            peri = cv2.arcLength(c, True)
                            approx = cv2.approxPolyDP(c, eps * peri, True)
                            # draw the approximated contour on the image
                            output = frame.copy()
                            if screenCnt is None:
                                detected = 0
                                break
                            else:
                                detected = 1

                            if detected == 1:
                                cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
                            #cv2.imshow("Approximated Contour", output)
                            if len(approx) == 5:
                                screenCnt = approx
                            # Masking the part other than the number plate
                            mask = np.zeros(gray.shape,np.uint8)
                            new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
                            new_image = cv2.bitwise_and(output,frame,mask=mask)

                            # Now crop
                            (x, y) = np.where(mask == 255)
                            (topx, topy) = (np.min(x), np.min(y))
                            (bottomx, bottomy) = (np.max(x), np.max(y))
                            Cropped = gray[topx:bottomx+1, topy:bottomy+1]

                            #Read the number plate
                            text = pytesseract.image_to_string(Cropped, config='--psm 11')
                            print("Detected Number is:",text)
                            if len(text)>3:
                                cv2.imshow('image',output)
                                cv2.imshow('Cropped',Cropped)
                                idx = int(detections[0, 0, i, 1])
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

car_detection(INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/platetrim.mp4',
    OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/plate_detection.mp4')


# function that incorporates object detection with tracking
def carDetectTrack(INP_VIDEO_PATH: str, OUT_VIDEO_PATH: str, debug: bool):
    if debug:
        video_inp_path = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/cars4.mp4'
        video_out_path = 'C:/Users/Mohamed/OneDrive - McMaster University/Documents/School/University/Fall 2021/Elec Eng 4OI6A/Hooli-Net/src/modules/models/cars_detection.mp4'
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
        out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
                            10, (frame_width, frame_height))
    
    sys.path.append("..")
    
    carTracking = {}

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if debug and (cv2.waitKey(1) & 0xFF == ord('q')):
            break
        
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.0035, (260, 260), 46)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.43:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                
                if CLASSES[idx] == "car":
                    carTracking[str(carCounter)] = trackObject(video_inp_path, video_out_path, cap.get(cv2.CAP_PROP_POS_FRAMES), box, carCounter, False)
                    
                    # mask car
                    
                    carCounter += 1

                    if debug:
                        print("Box:")
                        print(box)
                        (startX, startY, endX, endY) = box.astype("int")
                        label = "{}: {:.2f}%".format(CLASSES[idx],confidence*100)
                        cv2.rectangle(frame, (startX, startY), (endX, endY),    COLORS[idx], 2)
                        out.write(frame)
                        cv2.imshow('frame', frame)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        
        frameCounter += 1

    if debug:
        out.release()
    
    cap.release()
    cv2.destroyAllWindows()

    return True


if __name__ == "__main__":
    INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/cars4.mp4'
    OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/cars_detection.avi'
    carDetectTrack(INP_VIDEO_PATH, OUT_VIDEO_PATH, True)
