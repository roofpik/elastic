from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch
i = 0
j = 0
k = 0
class residentialclass(Resource):
		def get(self):
				try:
					es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
					query_builder = {}
					query_builder['query'] = {}
					query_builder['query']['bool'] = {}
					query_builder['query']['bool']['must'] = []
					query_builder['query']['bool']['should'] = []
					query_builder['sort'] = []					

					parser = reqparse.RequestParser()
					parser.add_argument('style', type=str)
					args = parser.parse_args()
					_style = args['style']
					if not _style:
							_style = ""
					if(_style):
						build_query_must("style", _style)
					#return query_builder
					res = es.search(index='index_res', doc_type='data', body=query_builder)
					return res

				except Exception:
					return Exception

def build_query_must(field, value):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['match'] = {}
	query_builder['query']['bool']['must'][i]['match'][field] = value
	i += 1