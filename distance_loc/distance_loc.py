from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

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
		
		_page_start = '0'
		_page_size = '5'

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
		display_result.update({'hits' : res['hits']['total']})
		while index<page_counter:
			temp_result = {}
			temp_result.update({index : res['hits']['hits'][index]['_source']})
			index += 1
		display_result.update({'details' : temp_result})
		return display_result
