from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
from firebase import firebase

def printCityList(cityList):
	index= 0
	lister = {}
	lister['cityList'] = {}
	for iteration in cityList:
		index += 1
		lister['cityList'].update({index:cityList[iteration]['cityName']})
	return lister

def printProjectList(city, cityList, projectList):
	checker = 0
	lister = {}
	for iteration in projectList:
		if (iteration == city):
			checker = 1
			lister['project listing for '+cityList[iteration]['cityName']] = {}			
			for type_ in projectList[iteration]:
				lister['project listing for '+cityList[iteration]['cityName']][type_] = {}
				index = 0
				for project in projectList[iteration][type_]:
					index += 1
					lister['project listing for '+cityList[iteration]['cityName']][type_].update({index:projectList[iteration][type_][project]})
	return lister
	if checker == 0:
		return {city:'city not found'}

def printllList(city, cityList, projectList, locationOrLocality):
	checker = 0
	lister = {}
	for iteration in projectList:
		if (iteration == city):
			checker = 1
			lister[locationOrLocality+'s for '+cityList[iteration]['cityName']] = {}			
			index = 0
			for project in projectList[iteration]:
				index += 1
				lister[locationOrLocality+'s for '+cityList[iteration]['cityName']].update({index:projectList[iteration][project][locationOrLocality]})
	return lister
	if checker == 0:
		return {city:'city not found'}

class adminlistclass(Resource):
	def get(self):

		fb = firebase.FirebaseApplication('https://roofpik-f8f55.firebaseio.com/', None)

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if 'listType' in _args.keys():
			view = _args['listType']
		else:
			return 'no listType provided'

		if 'city' in _args.keys():
			city = _args['city']
		else:
			city = ''

		cityList = fb.get('/city', None)
		if view=='city':
			return printCityList(cityList)

		elif view=='project':
			if city:
				projectList = fb.get('/projects', None)
				return printProjectList(city, cityList, projectList)
			else:
				return 'provide city to list projects'

		elif view=='locality':
			if city:
				localityList = fb.get('/locality', None)
				return printllList(city, cityList, localityList, 'localityName')
			else:
				return 'provide city to list localities'

		elif view=='location':
			if city:
				locationList = fb.get('/locations', None)
				return printllList(city, cityList, locationList, 'locationName')
			else:
				return 'provide city to list locations'

		else:
			return 'not a valid list type'
