import json
import requests
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

class universalsearchclass(Resource):
	def get(self):
		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/universal_search_index/data/_search'

		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if not 'name' in _args.keys():
			return 'no search query as of now'
		
		_name = _args['name']

		query = {"query":{"match_phrase_prefix":{"name":_name}}}
		query = json.dumps(query)
		result = requests.post(url, data = query)
		result = json.loads(result.text)

		index = 0

		if(result['hits']['total']<10):
			counter = result['hits']['total']
		else:
			counter = 10
		
		final_result = {}

		while index<counter:
			final_result.update({index:result['hits']['hits'][index]['_source']})
			index += 1

		return final_result

