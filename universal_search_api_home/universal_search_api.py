import json
import requests
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

class universalhomesearchclass(Resource):
	def get(self):
		#url for es index
		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/universal_search_index_home/data/_search'
		#parsing argument 'args' that contains the encoded parameters
		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']
		if not _args:
			return 'no argument'
		_args = decodeArgs(_args)
		#searching for 'name' key in decoded arguments
		if not 'name' in _args.keys():
			return 'no search query as of now'
		
		_name = _args['name']
		_name = _name.lower()
		#query for matching search box input
		query = {"query":{"regexp":{"name":".*"+_name+".*"}}}
		query = json.dumps(query)
		#posting query to es
		result = requests.post(url, data = query)
		result = json.loads(result.text)

		index = 0
		#checking number of results to be sent
		if(result['hits']['total']<10):
			counter = result['hits']['total']
		else:
			counter = 10
		
		final_result = {}
		#iterating according to number of hits
		while index<counter:
			final_result.update({index:result['hits']['hits'][index]['_source']})
			index += 1

		return final_result
