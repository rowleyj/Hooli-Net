import numpy as np
import cv2
import sys
import local_variables
import object_tracking

def car_detection(INP_VIDEO_PATH, OUT_VIDEO_PATH):
    PROTOTXT = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.prototxt'
    MODEL = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.caffemodel'
    INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars4.mp4'
    OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars_detection.mp4'
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
            if confidence > 0.43:
                idx = int(detections[0, 0, i, 1])
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

car_detection(INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/plate1.MP4',
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
                    carTracking[str(carCounter)] = object_tracking.trackObject(video_inp_path, video_out_path, cap.get(cv2.CAP_PROP_POS_FRAMES), box, carCounter, False)
                    
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
