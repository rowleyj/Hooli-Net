# Test API Functionality


#!/usr/bin/env python3


# import libraries
import requests


BASE = "http://127.0.0.1:5000/"

response = requests.get(
    BASE + "product",
    params={"a":2,"b":3}
    )
print(response.json())

response = requests.get(
    BASE + "process_video",
    params={
        "input_video_path":'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/cars4.mp4',
        "output_video_path":'C:/Users/tnaguib/Documents/GitHub/Hooli-Net/src/modules/models/cars_detection.avi',
        "token":'abc123'
    })
print(response.json())