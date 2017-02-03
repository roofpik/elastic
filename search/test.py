from restful import Resource
import requests
import json
from elasticsearch import Elasticsearch

class test(Resource):
	def get(self):
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
		t = es.get(index='sw', doc_type='people', id=5)
		return t
