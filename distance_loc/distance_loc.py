from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

def checkIfLocation():
	return True

def checkRecentlyVisited():
	return False

def sortByLocation(_page_start, _page_size, _lat, _lon):
	query = { "sort": [ { "_geo_distance": { "location": { "lat": float(_lat), "lon": float(_lon) }, "order": "asc", "unit": "km", "distance_type": "plane" } } ] }
		
	query = json.dumps(query)

	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_geo/data/_search?size='+_page_size+'&from='+_page_start

	res = requests.post(url, data=query)
	res = json.loads(res.text)
	res_count = res['hits']['total']

	if(res_count <= 10):
		page_counter = res_count
	else:
		page_counter = int(_page_size)
	index=0
	display_result = {}
	temp_result = {}
	display_result.update({'hits' : res['hits']['total']})
	while index<page_counter:
		temp_result.update({index : res['hits']['hits'][index]['_source']})
		index += 1
	display_result.update({'details' : temp_result})
	return display_result

def sendMostSearched(_page_start, _page_size):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/dummy_data_2/data/_search?size='+_page_size+'&from='+_page_start
	res = requests.post(url)
	res = json.loads(res.text)
	res_count = res['hits']['total']

	if(res_count <= 10):
		page_counter = res_count
	else:
		page_counter = int(_page_size)
	index=0
	display_result = {}
	temp_result = {}
	display_result.update({'hits' : res['hits']['total']})
	while index<page_counter:
		temp_result.update({index : res['hits']['hits'][index]['_source']})
		index += 1
	display_result.update({'details' : temp_result})
	return display_result

def sendRecentlyVisited(uid, _page_start, _page_size):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/dummy_data_1/data/_search?size='+_page_size+'&from='+_page_start
	query = {"query":{"match":{"uid":uid}}}
	query = json.dumps(query)
	res = requests.post(url, data=query)
	res = json.loads(res.text)
	res_count = res['hits']['total']

	if(res_count <= 10):
		page_counter = res_count
	else:
		page_counter = int(_page_size)

	index=0
	display_result = {}
	temp_result = {}
	display_result.update({'hits' : res['hits']['total']})
	while index<page_counter:
		temp_result.update({index : res['hits']['hits'][index]['_source']})
		index += 1
	display_result.update({'details' : temp_result})
	return display_result
	
class locationdistanceclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()		
		
		#parser.add_argument('args', type=str)
		#args = parser.parse_args()
		#_args = args['args']

		#if not _args:
		#	return 'provide arguments'

		parser.add_argument('lat', type=str)
		args = parser.parse_args()
		_lat = args['lat']
		if not _lat:
			_lat = "0"

		parser.add_argument('lon', type=str)
		args = parser.parse_args()
		_lon = args['lon']
		if not _lon:
			_lon = "0"

		_page_start = "0"
		_page_size = "5"

		parser.add_argument('uid', type=str)
		args = parser.parse_args()
		_uid = args['uid']
		if not _uid:
			flag = checkIfLocation()
			if(flag == True):
				answer = sortByLocation(_page_start, _page_size, _lat, _lon)
			else:
				answer = sendMostSearched(_page_start, _page_size)

		else:
			flag = checkRecentlyVisited()
			if(flag == True):
				answer = sendRecentlyVisited()
			else:
				flag = checkIfLocation()
				if(flag == True):
					answer = sortByLocation(_page_start, _page_size, _lat, _lon)
				else:
					answer = sendMostSearched(_page_start, _page_size)		
		
		return answer
