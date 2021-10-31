# Test API Functionality


#!/usr/bin/env python3


# import libraries
import requests


BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "product", {"a":2,"b":3})
print(response.json())