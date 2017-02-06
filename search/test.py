from restful import Resource
import requests
import json
from elasticsearch import Elasticsearch

class test(Resource):
	def get(self):
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
		x = {
			  "sort": [],
			  "query": {
			    "bool": {
			      "should": [
			        {
			          "bool": {
			            "must": [
			              {
			                "range": {
			                  "rent.min": {
			                    "gte": "20000"
			                  }
			                }
			              },
			              {
			                "range": {
			                  "rent.max": {
			                    "lte": "90000"
			                  }
			                }
			              }
			            ]
			          }
			        }
			      ],
			      "must": []
			    }
			  }
			}
		t = es.search(index='live_index_1', doc_type='data', body=x)
		return t
