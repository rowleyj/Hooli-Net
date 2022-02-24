# module to hold all local variables to ensure we can test api on local systems


#!/usr/bin/env python3


# import libraries
import os


# Local variables and paths - fill with applicable variables
PATH = os.getcwd()

tesseract_path =    'C:/Program Files/Tesseract-OCR/tesseract.exe'
video_inp_path =    os.path.join(PATH, 'src', 'modules', 'models', 'cars4.mp4')
video_out_path =    os.path.join(PATH, 'src', 'modules', 'models', 'cars_detection.mp4')
prototext_path =    os.path.join(PATH, 'src', 'modules', 'models', 'MobileNetSSD_deploy.prototxt')
model_path =        os.path.join(PATH, 'src', 'modules', 'models', 'MobileNetSSD_deploy.caffemodel')

tracking_video_inp_path =    os.path.join(PATH, 'src', 'modules', 'models', 'cars4.mp4')
tracking_video_out_path =    os.path.join(PATH, 'src', 'modules', 'models', 'cars_tracking.mp4')

plate_image_path = os.path.join(PATH, 'src', 'modules', 'models', 'plates', 'platevid2.png')

backend_url =       'http://127.0.0.1:8080'
