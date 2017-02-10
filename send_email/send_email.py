from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import urllib

class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('email', type=str)
		args = parser.parse_args()
		_email = args['email']

		_email = _email.decode('base64')
		_email = urllib.unquote(_email).decode('utf8')
		return _email
