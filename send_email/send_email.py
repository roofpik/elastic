from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import urllib

def decodeArgs(_args):
	_args = _args.decode('base64')
	count = _args.count('&')
	count += 1
	index = 0
	split_list = []
	temp_list = []
	final_list = []
	while index < count:
		split_list.append(_args.split('&')[index])
		temp_list.append(split_list[index].split('=')[1])

		return final_list.append(str(urllib.unquote(temp_list[index]).decode('utf8')))
		index += 1
	return final_list

#def sendmail(email, conf):
	

class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		all_args = decodeArgs(_args)
		return all_args
		
#		sendmail(all_args[0], all_args[1])
