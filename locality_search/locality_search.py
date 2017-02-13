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
		#_page_start = _id[1]
		#_page_size = _id[2]
		_page_start = '0'
		_page_size = '10'

		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_index/data/_search?size='+_page_size+'&from='+_page_start

		if not _id:
			res = requests.get(url)
			res = json.loads(res.text)
			count = res['hits']['total']
			index = 0
			r_temp = {}
			d_temp = {}
			d_temp.update({'hits' : count})
			if(count>int(_page_size)):
				count = int(_page_size) 
			while index<count:
				r_temp.update({index : res['hits']['hits'][index]['_source']})
				index += 1
			d_temp.update({'details' : r_temp})
			return d_temp


		query = {"query": {"match": {"name": _id}}}
		query = json.dumps(query)
		res = requests.post(url, data = query)
		res = json.loads(res.text)
		return res['hits']['hits'][0]['_source']
