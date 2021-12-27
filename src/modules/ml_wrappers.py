# ml wrappers module to call ml functions and pass the correct information


#!/usr/bin/env python3


# import ml models and functions
from .models.ssd_object_detection import car_detection
from .models.license_plate_detection import license_reading


def vehicle_detect(input_video_path, output_video_path, auth_token):
    PROTOTXT = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.prototxt'
    MODEL = 'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/MobileNetSSD_deploy.caffemodel'

    return car_detection(PROTOTXT, MODEL, input_video_path, output_video_path)


def license_read():
    #set the arguments for licence reading
    return license_reading()