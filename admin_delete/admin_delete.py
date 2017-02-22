from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
from firebase import firebase

class admindeleteclass(Resource):
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

		if 'localityId' in _args.keys():
			localityId = _args['localityId']
		else:
			localityId = ''

		if 'locationId' in _args.keys():
			locationId = _args['locationId']
		else:
			locationId = ''

		if 'projectType' in _args.keys():
			projectType = _args['projectType']
		else:
			projectType = ''

		if 'projectId' in _args.keys():
			projectId = _args['projectId']
		else:
			projectId = ''

		if _type=='city':
			if cityId:
				fb.delete('https://roofpik-f8f55.firebaseio.com/city/'+cityId, None)
			else:
				return 'provide city id'

		elif _type=='location':
			if cityId and locationId:
				fb.delete('https://roofpik-f8f55.firebaseio.com/locations/'+cityId+'/'+locationId, None)
			else:
				return 'provide both city id and location id'

		elif _type=='locality':
			if cityId and localityId:
				fb.delete('https://roofpik-f8f55.firebaseio.com/locality/'+cityId+'/'+localityId, None)
			else:
				return 'provide both city id and locality id'

		elif _type=='project':
			if cityId and projectType and projectId:
				fb.delete('https://roofpik-f8f55.firebaseio.com/projects/'+cityId+'/'+projectType+'/'+projectId, None)
			else:
				return 'provide city id, project id and project type'
		
		else:
			return 'not a valid type'	
