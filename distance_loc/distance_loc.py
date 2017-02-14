from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

#check if data exists for user
def checkRecentlyVisited(_uid):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/recentsearches/data/_search'
	query = {"query":{"match":{"user":_uid}}}
	query = json.dumps(query)
	res = requests.post(url, data=query)
	res = json.loads(res.text)
	if res['hits']['total']>0:
		return True
	else:
		return False

#calculate results based on parameters
def calculateResult(res, _page_start, _page_size):
	res_count = res['hits']['total']

	if(res_count <= 10):
		page_counter = res_count
	else:
		page_counter = int(_page_size)
	index=0
	display_result = {}
	temp_result = {}
	#push number of hits
	display_result.update({'hits' : res['hits']['total']})
	#push records into the object	
	while index<page_counter:
		temp_result.update({index : res['hits']['hits'][index]['_source']})
		index += 1
	display_result.update({'details' : temp_result})
	return display_result

#send data wrt location
def sortByLocation(_page_start, _page_size, _lat, _lon):
	query = { "sort": [ { "_geo_distance": { "location": { "lat": float(_lat), "lon": float(_lon) }, "order": "asc", "unit": "km", "distance_type": "plane" } } ] }

	query = json.dumps(query)

	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_geo/data/_search?size='+_page_size+'&from='+_page_start

	res = requests.post(url, data=query)
	res = json.loads(res.text)
	return calculateResult(res, _page_start, _page_size)

#send general data for most searched localities
def sendMostSearched(_page_start, _page_size):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/mostsearched/data/_search?size='+_page_size+'&from='+_page_start
	res = requests.post(url)
	res = json.loads(res.text)
	return calculateResult(res, _page_start, _page_size)

#send recently visited localities of user
def sendRecentlyVisited(_uid, _page_start, _page_size):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/recentsearches/data/_search?size='+_page_size+'&from='+_page_start
	query = {"query":{"match":{"user":_uid}}}
	query = json.dumps(query)
	res = requests.post(url, data=query)
	res = json.loads(res.text)
	return calculateResult(res, _page_start, _page_size)

def sendSeries1(name_query, _page_start, _page_size, _lat, _lon):
	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/recentsearches,locality_geo/data/_search?size='+_page_size+'&from='+_page_start
	query={}
	query.update({'query':name_query})
	query.update({'sort':[{ "_geo_distance": { "location": { "lat": float(_lat), "lon": float(_lon) }, "order": "asc", "unit": "km", "distance_type": "plane" } } ,{"flag": {"order": "asc"}}]})
	query = json.dumps(query)
	res = requests.post(url, data=query)
	res = json.loads(res.text)
	return calculateResult(res, _page_start, _page_size)

def sendSeries2(name_query, _page_start, _page_size, _lat, _lon):
	query = { "sort": [ { "_geo_distance": { "location": { "lat": float(_lat), "lon": float(_lon) }, "order": "asc", "unit": "km", "distance_type": "plane" } } ]}
	query.update({"query":name_query})
		
	query = json.dumps(query)

	url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_geo/data/_search?size='+_page_size+'&from='+_page_start

	res = requests.post(url, data=query)
	res = json.loads(res.text)
	return calculateResult(res, _page_start, _page_size)

class locationdistanceclass(Resource):
	def get(self):
		
		#generate single argument, decode later
		parser = reqparse.RequestParser()		
		
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		if not _args:
			return sendMostSearched('0', '10')
		#call decoder to decode arguments
		_args = decodeArgs(_args)

		#check and map variables
		if 'lon' in _args.keys() and 'lat' in _args.keys():
			_lon = _args['lon']
			_lat = _args['lat']
			location_flag = True
		else:
			location_flag = False

		if 'name' in _args.keys():
			_name = _args['name']
		else:
			_name = ""

		if not 'page_start' in _args.keys():
			_page_start = "0"
		else:
			_page_start = _args['page_start']
		if not 'page_size' in _args.keys():
			_page_size = "10"
		else:
			_page_size = _args['page_size']

		#call functions according to condition
		if not 'uid' in _args.keys():
			_uid = ""
			if(location_flag == True):
				#no user, given location, send locations sorted wrt given location
				answer = sortByLocation(_page_start, _page_size, _lat, _lon)
			else:
				#no user, no location, send most searched locations
				answer = sendMostSearched(_page_start, _page_size)
		else:
			_uid = _args['uid']
			#check if user id exists
			flag = checkRecentlyVisited(_uid)
			if(flag == True):
				#if user id exists, send recently visited of that user
				answer = sendRecentlyVisited(_uid, _page_start, _page_size)
			else:
				if(location_flag == True):
					#if user exists, and so does location, sort by location
					answer = sortByLocation(_page_start, _page_size, _lat, _lon)
				else:
					#if user exists, but no data and no location, send most searched
					answer = sendMostSearched(_page_start, _page_size)

		if _name:
			name_query = {"match_phrase_prefix":{"name":_name}}
			if _uid:
				if(checkRecentlyVisited(_uid) and location_flag == True):
					answer = sendSeries1(name_query, _page_start, _page_size, _lat, _lon)
			else:
				if(location_flag == True):
					answer = sendSeries2(name_query, _page_start, _page_size, _lat, _lon)
				else:
					answer = sendMostSearched(_page_start, _page_size)

		return answer
