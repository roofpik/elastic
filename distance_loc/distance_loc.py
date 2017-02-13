from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

def checkRecentlyVisited():
	return True

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

def sendRecentlyVisited(_uid, _page_start, _page_size):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/dummy_data_1/data/_search?size='+_page_size+'&from='+_page_start
	query = {"query":{"match":{"uid":_uid}}}
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
		
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		if not _args:
			sendMostSearched(_page_start, _page_size)

		_args = decodeArgs(_args)

		if lon in _args.keys():
			_lon = _args['lon']
			location_flag = True
		else:
			location_flag = False
		
		if lat in _args.keys():
			_lat = _args['lat']
			location_flag = True
		else:
			location_flag = False

		if not page_start in _args.keys():
			_page_start = "0"
		if not page_size in _args.keys():
			_page_size = "5"

		if not uid in _args.keys():
			if(location_flag == True):
				answer = sortByLocation(_page_start, _page_size, _lat, _lon)
			else:
				answer = sendMostSearched(_page_start, _page_size)
		else:
			flag = checkRecentlyVisited()
			if(flag == True):
				answer = sendRecentlyVisited(_uid, _page_start, _page_size)
			else:
				flag = checkIfLocation()
				if(flag == True):
					answer = sortByLocation(_page_start, _page_size, _lat, _lon)
				else:
					answer = sendMostSearched(_page_start, _page_size)		
		
		return answer
