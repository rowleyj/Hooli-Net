import numpy as np
import cv2
import sys

def car_detection(INP_VIDEO_PATH, OUT_VIDEO_PATH):
    PROTOTXT = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/MobileNetSSD_deploy.prototxt'
    MODEL = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/MobileNetSSD_deploy.caffemodel'
    INP_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars4.mp4'
    OUT_VIDEO_PATH = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/object_detection/cars_detection.mp4'
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
            
    cap = cv2.VideoCapture(INP_VIDEO_PATH)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(OUT_VIDEO_PATH, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
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


# placeholder function
def car_detection(PROTOTXT, MODEL, INP_VIDEO_PATH, OUT_VIDEO_PATH):
    #return true if the video was able to be fully processed and the output was stored correctly; return false otherwise
    pass
