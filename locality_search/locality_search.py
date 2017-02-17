from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

#function to return object in prescribed format
def return_object(res, _page_size):
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

class localityclass(Resource):
	def get(self):

		#taking single argument to be decoded later
		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']
		_page_start = '0'
		_page_size = '10'

		#url for es index
		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_index/data/_search?size='+_page_size+'&from='+_page_start

		#call function without any query body
		if not _args:
			res = requests.get(url)
			res = json.loads(res.text)
			return return_object(res, _page_size)

		#decoding arguments and mapping them to variables
		_args = decodeArgs(_args)
		_id = _args['id']
		if 'page_start' in _args.keys():
			_page_start = _args['page_start']
		if 'page_size' in _args.keys():
			_page_size = _args['page_size']	

		#call function with a query body
		query = {"query": {"match": {"name": _id}}}
		query = json.dumps(query)
		res = requests.post(url, data = query)
		res = json.loads(res.text)
		return return_object(res, _page_size)
