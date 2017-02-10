from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from urllib import parse

class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('email', type=str)
		args = parser.parse_args()
		_email = args['email']

		_email = _email.decode('base64')
		_email = parse.unquote(_email)
		return _email
