from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
from firebase import firebase

def viewCity(city, cityList):
	checker = 0
	for iterator in cityList:
		if iterator==city:
			checker = 1
			return cityList[iterator]
	if checker==0:
		return 'city not found'

def viewProject(city, type_, projectId, projectList):
	checker = 0
	lister = {}
	for iteration in projectList:
		if iteration == city:			
			for type__ in projectList[iteration]:
				if type__ == type_:
					for project in projectList[iteration][type_]:
						if project==projectId:
							checker = 1
							lister.update(projectList[iteration][type_][project])
	return lister
	if checker == 0:
		return 'not found'

def viewLL(city, id_, LList):
	checker = 0
	lister = {}
	for iteration in LList:
		if iteration == city:	
			for loc in LList[iteration]:
				if loc==id_:
					checker = 1
					lister.update(LList[iteration][id_])
	return lister
	if checker == 0:
		return 'not found'

class adminviewclass(Resource):
	def get(self):

		fb = firebase.FirebaseApplication('https://roofpik-f8f55.firebaseio.com/', None)

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if 'city' in _args.keys():
			city = _args['city']
		else:
			city = ""
		
		if 'type' in _args.keys():
			_type = _args['type']
		else:
			_type = ""

		if 'projectId' in _args.keys():
			projectId = _args['projectId']
		else:
			projectId = ""
	
		if 'locationId' in _args.keys():
			locationId = _args['locationId']
		else:
			locationId = ""

		if 'localityId' in _args.keys():
			localityId = _args['localityId']
		else:
			localityId = ""

		if 'view' in _args.keys():
			view = _args['view']
		else:
			return 'no view requested'

		if view=='city':
			if city:
				cityList = fb.get('/city', None)
				return viewCity(city, cityList)
			else:
				return 'no city id provided for '+view

		if view=='project':
			if city and _type and projectId:
				projectList = fb.get('/projects', None)
				return viewProject(city, _type, projectId, projectList)
			else:
				return 'incomplete info provided for '+view

		if view=='locality':
			if city and localityId:
				localityList = fb.get('/locality', None)
				return viewLL(city, localityId, localityList)
			else:
				return 'incomplete info provided for '+view

		if view=='location':
			if city and locationId:
				locationList = fb.get('/projects', None)
				return viewLL(city, locationId, locationList)
			else:
				return 'incomplete info provided for '+view

