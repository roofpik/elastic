from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
from firebase import firebase

#function to find city if exists and return its details
def viewCity(city, cityList):
	checker = 0
	for iterator in cityList:
		if iterator==city:
			checker = 1
			return cityList[iterator]
	if checker==0:
		return 'city not found'

#function to find a project and return its details
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

#function to find location or locality and return its details
def viewLL(city, id_, LList):
	checker = 0
	lister = {}
	for iteration in LList:
		if iteration == city:	
			for loc in LList[iteration]:
				if loc==id_:
					checker = 1
					lister.update(LList[iteration][loc])
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
		
		if 'projectType' in _args.keys():
			projectType = _args['projectType']
		else:
			projectType = ""

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

		#call above defined functions according to selected 'view'
		if view=='city':
			if city:
				cityList = fb.get('/city', None)
				return viewCity(city, cityList)
			else:
				return 'no city id provided for '+view

		elif view=='project':
			if city and projectType and projectId:
				projectList = fb.get('/projects', None)
				return viewProject(city, projectType, projectId, projectList)
			else:
				return 'incomplete info provided for '+view

		elif view=='locality':
			if city and localityId:
				localityList = fb.get('/locality', None)
				return viewLL(city, localityId, localityList)
			else:
				return 'incomplete info provided for '+view

		elif view=='location':
			if city and locationId:
				locationList = fb.get('/locations', None)
				return viewLL(city, locationId, locationList)
			else:
				return 'incomplete info provided for '+view

		else:
			return 'not a valid view type'
