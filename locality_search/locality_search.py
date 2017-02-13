from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

class localityclass(Resource):
	def get(self):
		
		parser = reqparse.RequestParser()
		parser.add_argument('id', type=str)
		args = parser.parse_args()
		_id = args['id']

		#_id = decodeArgs(_id)
	
		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_index/data/_search'

		query = {"query": {"match": {"name": _id}}}
		#return 'do'
		return query
		res = requests.post(url, data = query)
		res = json.loads(res.text)
		return res
