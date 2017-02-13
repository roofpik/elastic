from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

class localityclass(Resource):
	def get(self):

		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_index/data/_search'
		parser = reqparse.RequestParser()
		parser.add_argument('id', type=str)
		args = parser.parse_args()
		_id = args['id']

		if not _id:
			res = requests.get(url)
			res = json.loads(res.text)
			count = res['hits']['total']
			index = 0
			r_temp = {}
			d_temp = {}
			d_temp.update({'hits' : count})
			while index<count:
				r_temp.update({index : res['hits']['hits'][index]['_source']})
				return count
				index += 1
			d_temp.update({'details' : r_temp})
			return d_temp

		#_id = decodeArgs(_id)

		query = {"query": {"match": {"name": _id}}}
		#return 'do'
		query = json.dumps(query)
		res = requests.post(url, data = query)
		res = json.loads(res.text)
		return res['hits']['hits'][0]['_source']
