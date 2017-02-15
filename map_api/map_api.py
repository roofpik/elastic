import json
import requests
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

def getProjects(location_id, url, url4, temp3):
	for l in location_id:
		query = {"query":{"match":{"location."+str(l) : True}}}
		query = json.dumps(query)
		res1 = requests.post(url, data = query)
		res1 = json.loads(res1.text)
		size = res1['hits']['total']
		res1 = requests.post(url+'?size='+str(size), data = query)
		res1 = json.loads(res1.text)
		i=0
		temp2 = {}
		while i<res1['hits']['total']:
			temp1 = {}
			temp1.update({'pid':res1['hits']['hits'][i]['_source']['projectId']})
			id = res1['hits']['hits'][i]['_source']['projectId']
			rating = getRating(id, url4)
			temp1.update({'rating':rating})
			temp1.update({'cover':res1['hits']['hits'][i]['_source']['cover_pic']})
			temp1.update({'rent':res1['hits']['hits'][i]['_source']['rent']})
			temp1.update({'location':res1['hits']['hits'][i]['_source']['coordinates']})
			temp1.update({'type':'cghs'})
			temp2.update({i:temp1})
			i += 1
		temp3.update({str(l):temp2})
		return temp3

class mapapiclass(Resource):
	def get(self):

		url1 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_geo/data/_search'
		url2 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/cghs_index/data/_search'
		url3 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/residential_index/data/_search'
		url4 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/rating_projects/data/_search'

		#single argument to be decoded using decodeArgs
		parser = reqparse.RequestParser()		
		
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if 'lat' in _args.keys() and 'lon' in _args.keys():
			_lat = _args['lat']
			_lon = _args['lon']
		else:
			return 'provide latitude and longitude'
	
		if 'distance' in _args.keys():
			_distance = _args['distance']
		else:
			_distance = '5'

		distance_query = { "query": { "bool" : { "must" : { "match_all" : {} }, "filter" : { "geo_distance" : { "distance" : _distance+"km", "location" : { "lat" : _lat, "lon" : _lon } } } } } }

		distance_query = json.dumps(distance_query)

		res = requests.post(url1, data=distance_query)
		res = json.loads(res.text)
		res = requests.post(url1+'?size='+res['hits']['total'], data=distance_query)
		res = json.loads(res.text)
		location_id = []
		while i<res['hits']['total']:
			location_id.append(res['hits']['hits'][i]['_source']['id'])
			i += 1

		temp3 = {}
		temp3 = getProjects(location_id, url2, url4, temp3)
		temp3 = getProjects(location_id, url3, url4, temp3)
		return temp3
