# Test API Functionality


#!/usr/bin/env python3


# import libraries
import requests
import local_variables


BASE = "http://127.0.0.1:5000/"

response = requests.get(
    BASE + "product",
    params={"a":2,"b":3}
    )
print(response.json())

response = requests.get(
    BASE + "process_video",
    params={
        "input_video_path":local_variables.video_inp_path,
        "output_video_path":local_variables.video_out_path,
        "token":'abc123'
    })
print(response.json())