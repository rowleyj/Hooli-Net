# hooli db module to call all the different db operations


#!/usr/bin/env python3


# import libraries
import requests
import local_variables


# function to create new vehicle in db
def dbCreateVehicle(licensePlate: str) -> bool:
    response = requests.post(
        local_variables.backend_url + '/vehicle',
        data={'licensePlate': licensePlate},
        headers={
            'Authorization': f'Bearer {local_variables.auth_token}'
        })

    print(response)

    # need to isolate vehicle id from response and return it

    return response


# function to create new bounding cube in db
def dbCreateBoundingCube(carId: int, videoPath: str, startFrame: int, endFrame: int, boxes) -> bool:
    response = requests.post(
        local_variables.backend_url + '/boundingCube',
        data={
            'vehicleId': carId,
            'videoUrl': videoPath,
            'start': startFrame,
            'end': endFrame,
            'boxes': boxes
        },
        headers={
            'Authorization': f'Bearer {local_variables.auth_token}'
        })
    
    print(response)

    return True


# function to get bounding cube from db
def dbGetBoundingCube(carId: int, token: str):
    response = requests.post(
        local_variables.backend_url + '/boundingCube',
        data={'vehicleId': carId},
        headers={
            'Authorization': f'Bearer {local_variables.auth_token}'
        })
    
    return response