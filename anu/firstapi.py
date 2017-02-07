from restful import Resource
import requests
import json
from elasticsearch import Elasticsearch

class anuapi(Resource):
	def get(self):
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
		t = es.get(index='ecommerce', doc_type='product', id=1001)
		return t
