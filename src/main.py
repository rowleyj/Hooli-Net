#!/usr/bin/env python3


# import flask
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


# import modules
from modules import product
from modules import ml_wrappers


app = Flask(__name__)
api = Api(app)


##################################


productArgs = reqparse.RequestParser()
productArgs.add_argument("a", type=int, help="Error - Value 'a' is required!", required=True)
productArgs.add_argument("b", type=int, help="Error - Value 'b' is required!", required=True)


class Product(Resource):
    def get(self):
        #authenticate requester (use request.baseURL)
        
        args = productArgs.parse_args()

        a = args["a"]
        b = args["b"]
        p = product.multiply(a, b)

        response = {
            "a":a,
            "b":b,
            "product":p
        }

        return response, 200

api.add_resource(Product, "/product")


##################################


# Process Video
processVideoArgs = reqparse.RequestParser()
processVideoArgs.add_argument("input_video_path", type=str, help="Error - Value 'input_video_path' is required!", required=True)
processVideoArgs.add_argument("output_video_path", type=str, help="Error - Value 'output_video_path' is required!", required=True)
processVideoArgs.add_argument("token", type=str, help="Error - Vaule 'token' is required!", required=True)

class Process_Video(Resource):
    def get(self):
        #authenticate requester (use request.baseURL)

        args = processVideoArgs.parse_args()

        input_path = args["input_video_path"]
        output_path = args["output_video_path"]
        token = args["token"]
        
        # start processing video - add all steps later
        processed = True
        processed = ml_wrappers.vehicle_detect(input_path, output_path, token)

        response = {
            "input_video_path":input_path,
            "output_video_path":output_path,
            "processed":processed
        }

        return response, 200
    
api.add_resource(Process_Video, "/process_video")


##################################


def main():
    if __name__ == '__main__':
        app.run(host='0.0.0.0')
    else:
        app.run()


if __name__ == "__main__":
    main()