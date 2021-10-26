#!/usr/bin/env python3


# import flask
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)


def main():
    app.run(debug=True)