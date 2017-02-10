from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import smtplib

#def send_mail(_email, _configuration):
	

class emailclass(Resource):
	def get(self):
		parser = reqparse.RequestParser()
			
		parser.add_argument('email', type=str)
		args = parser.parse_args()
		_email = args['email']
		if not _email:
			_email = ""

		_email = _email.decode('base64')
