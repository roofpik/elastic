from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch
from decoder import decodeArgs

def result(query, url):
	query = json.dumps(query)
	return query
	res = requests.post(url, data=query)
	res = json.loads(res.text)
	try:
		return res['source']
	except:
		return 'not found'

class nearbyclass(Resource):
	def get(self):
	
		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/nearby_index/data/_search'

		query_builder = {}
		query_builder['query'] = {}
		query_builder['query']['constant_score']={}
		query_builder['query']['constant_score']['filter']={}
		query_builder['query']['constant_score']['filter']['exists']={}

		if 'locationId' in _args.keys():
			locationId = _args['locationId']
		else:
			locationId = ''

		if locationId:
			query_builder['query']['constant_score']['filter']['exists']['field'] = 'details.address.location.primary.'+locationId
			return result(query_builder, url)

		if 'localityId' in _args.keys():
			localityId = _args['localityId']
		else:
			localityId = ''

		if localityId:
			query_builder['query']['constant_score']['filter']['exists']['field'] = 'details.address.location.primary.'+localityId
			return result(query_builder, url)
