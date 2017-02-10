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
		count = _email.count('&')
		count += 1
		i=0
		l = []
		l1= []
		while i<count:
			l.append(_email.split('&')[i])
			l1.append(urllib.unquote(l[i]).decode('utf8'))
			i+=1
		return l1
