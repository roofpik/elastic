from restful import Resource
import requests
import json
from elasticsearch import Elasticsearch

class test(Resource):
	def get(self):
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
		t = es.search(index='live_index_1', doc_type='data', body={"query": {"match":{"projectId": "-Ka2SmvifAG0CKkfsjyw"}}})
		return t
