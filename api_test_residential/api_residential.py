from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

class residentialclass(Resource):
		def get(self):
				try:
					i = 0
					j = 0
					k = 0
					true = True

					es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

					# #return query_builder
					# res = es.search(index='index_res', doc_type='data', body=query_builder, from_=_page_start, size=_page_size)
					# index_num = 0
					# final_res = {}
					# temp_res = {}
					# final_res.update({'records': es.count(index='index_res')['count']})
					# final_res.update({'hits': res['hits']['total']})
					# while index_num<_page_size:
					# 	bhk = []
					# 	temp_temp_res = {}
					# 	temp_temp_res.update({'id': res['hits']['hits'][index_num]['_source']['projectId']})
					# 	temp_temp_res.update({'name': res['hits']['hits'][index_num]['_source']['details']['name']})
					# 	temp_temp_res.update({'address': res['hits']['hits'][index_num]['_source']['address']})
					# 	temp_temp_res.update({'cover': res['hits']['hits'][index_num]['_source']['cover_pic']})
					# 	temp_temp_res.update({'area': res['hits']['hits'][index_num]['_source']['area']})
					# 	temp_temp_res.update({'rent': res['hits']['hits'][index_num]['_source']['rent']})
					# 	for key in res['hits']['hits'][index_num]['_source']['bhk']:
					# 		bhk.append(key)
					# 	bhk.sort()
					# 	fbhk = ', '.join(str(e) for e in bhk)
					# 	temp_temp_res.update({'bhks': fbhk})
					# 	temp_res.update({index_num : temp_temp_res})
					# 	index_num += 1
					# final_res.update({'details': temp_res})
#					return final_res   
					return 'works' 

				except Exception:
					return Exception
