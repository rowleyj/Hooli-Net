#!/usr/bin/env python3


# import flask
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


# import modules
from modules import product


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


# Vehicle Detect


##################################


# Vehicle Identify


##################################


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()