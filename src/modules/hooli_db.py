# hooli db module to call all the different db operations


#!/usr/bin/env python3


# import libraries
import requests
import local_variables


# function to create new vehicle in db
def dbCreateVehicle(licensePlate, token):
    response = requests.post(
        local_variables.backend_url + '/vehicle',
        data={'licensePlate':licensePlate},
        headers={
            'Authorization': f'Bearer {token}'
        })
    return True