from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
from firebase import firebase

class adminpostclass(Resource):
	def get(self):

		fb = firebase.FirebaseApplication('https://roofpik-f8f55.firebaseio.com/', None)

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)
		
		if 'type' in _args.keys():
			_type = _args['type']
		else:
			return 'no type specified'

		if 'cityId' in _args.keys():
			cityId = _args['cityId']
		else:
			cityId = ''

		if 'projectType' in _args.keys():
			projectType = _args['projectType']
		else:
			projectType = ''

		if 'data' in _args.keys():
			_data = _args['data']
		else:
			return 'provide data'

		#post _data as requested
		#format to post - fb.post(url, _data)
		if _type=='city':
			res = fb.post('https://roofpik-f8f55.firebaseio.com/city/', _data)
			return res
			
		elif _type=='location':
			if cityId:
				res = fb.post('https://roofpik-f8f55.firebaseio.com/locations/'+cityId, _data)
				return res
			else:
				return 'provide city id'

		elif _type=='locality':
			if cityId:
				res = fb.post('https://roofpik-f8f55.firebaseio.com/locality/'+cityId, _data)
				return res
			else:
				return 'provide city id'

		elif _type=='builder':
			res = fb.post('https://roofpik-f8f55.firebaseio.com/builders/', _data)
			return res

		elif _type=='project':
			if cityId and projectType:
				res = fb.post('https://roofpik-f8f55.firebaseio.com/projects/'+cityId+'/'+projectType, _data)
				return res
			else:
				return 'provide city id and project type'
		
		else:
			return 'not a valid type'
