import json
import requests
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

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

class mapapiclass(Resource):
	def get(self):

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

		if 'page_start' in _args.keys():
			_page_start = _args['page_start']
		else:
			_page_start = '0'

		if 'page_size' in _args.keys():
			_page_size = _args['page_size']
		else:
			_page_size = '10'

		url1 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/residential_index/data/'
		url2 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/cghs_index/data/'
		url3 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/rating_projects/data'

		
