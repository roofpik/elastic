from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

i = 0
j = 0
k = 0
true = True

class residentialclass(Resource):
		def get(self):
				try:
					es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

					parser = reqparse.RequestParser()
					parser.add_argument('style', type=str)
					args = parser.parse_args()
					_style = args['style']
					if not _style:
							_style = ""

					parser.add_argument('details_name', type=str)
					args = parser.parse_args()
					_details_name = args['details_name']
					if not _details_name:
							_details_name = ""

					parser.add_argument('details_builder', type=str)
					args = parser.parse_args()
					_details_builder = args['details_builder']
					if not _details_builder:
							_details_builder = ""

					parser.add_argument('area_range', type=str)
					args = parser.parse_args()
					_area_range = args['area_range']
					if not _area_range:
							_area_range = ""

					parser.add_argument('price_range', type=str)
					args = parser.parse_args()
					_price_range = args['price_range']
					if not _price_range:
							_price_range = ""

					parser.add_argument('sort_field', type=str)
					args = parser.parse_args()
					_sort_field = args['sort_field']
					if not _sort_field:
							_sort_field = ""

					parser.add_argument('bhk', type=str)
					args = parser.parse_args()
					_bhk = args['bhk']
					if not _bhk:
							_bhk = ""

					parser.add_argument('locationId', type=str)
					args = parser.parse_args()
					_locationId = args['locationId']
					if not _locationId:
							_locationId = ""

					parser.add_argument('propertyType', type=str)
					args = parser.parse_args()
					_propertyType = args['propertyType']
					if not _propertyType:
							_propertyType = ""

					parser.add_argument('amenity', type=str)
					args = parser.parse_args()
					_amenity = args['amenity']
					if not _amenity:
							_amenity = ""      

					parser.add_argument('page_start', type=int)
					args = parser.parse_args()
					_page_start = args['page_start']
					if not _page_start:
							_page_start = 0    

					parser.add_argument('page_size', type=int)
					args = parser.parse_args()
					_page_size = args['page_size']
					if not _page_size:
							_page_size = 10                  

					query_builder = {}
					query_builder['query'] = {}
					query_builder['query']['bool'] = {}
					query_builder['query']['bool']['must'] = []
					query_builder['query']['bool']['should'] = []
					query_builder['sort'] = []
					
					def build_query_must(field, value):
							global i
							query_builder['query']['bool']['must'].append({})
							query_builder['query']['bool']['must'][i]['match'] = {}
							query_builder['query']['bool']['must'][i]['match'][field] = value
							i += 1

					def build_query_should(field, value):
							global j
							query_builder['query']['bool']['should'].append({})
							query_builder['query']['bool']['should'][j]['match'] = {}
							query_builder['query']['bool']['should'][j]['match'][field] = value
							j += 1

					def build_query_must_range(field, lower, upper):
							global i
							query_builder['query']['bool']['must'].append({})
							query_builder['query']['bool']['must'][i]['range'] = {}
							query_builder['query']['bool']['must'][i]['range'][field] = {}
							query_builder['query']['bool']['must'][i]['range'][field]['from'] = lower
							query_builder['query']['bool']['must'][i]['range'][field]['to'] = upper
							i += 1

					def build_query_should_range(field, lower, upper):
							global j
							query_builder['query']['bool']['should'].append({})
							query_builder['query']['bool']['should'][j]['range'] = {}
							query_builder['query']['bool']['should'][j]['range'][field] = {}
							query_builder['query']['bool']['should'][j]['range'][field]['from'] = lower
							query_builder['query']['bool']['should'][j]['range'][field]['to'] = upper
							j += 1

					def build_query_sort(field, asc_or_dsc):
							global k
							query_builder['sort'].append({})
							query_builder['sort'][k][field] = {}
							query_builder['sort'][k][field]['order'] = asc_or_dsc
							k+=1

					def build_query_exists(field):
							global i
							query_builder['query']['bool']['must'].append({})
							query_builder['query']['bool']['must'][i]['constant_score'] = {}
							query_builder['query']['bool']['must'][i]['constant_score']['filter'] = {}
							query_builder['query']['bool']['must'][i]['constant_score']['filter']['exists'] = {}
							query_builder['query']['bool']['must'][i]['constant_score']['filter']['exists']['field'] = field
							i += 1

					if(_style):
							count = _style.count('$')
							if(count == 0):
									build_query_must("style", _style)
							else:
									count += 1
									temp = []
									z = 0
									while z!=count:
											temp.append(_style.split('$')[z])
											build_query_must("style", temp[z])
											z += 1

					if(_details_name):
							build_query_must("details.name", _details_name)

					if(_details_builder):
							build_query_must("details.builder", _details_builder)

					if(_area_range):
							low = _area_range.split('$')[0]
							high = _area_range.split('$')[1]
							build_query_should_range("area.min", low, high)
							build_query_should_range("area.max", low, high)

					if(_price_range):
							low = _price_range.split('$')[0]
							high = _price_range.split('$')[1]
							build_query_should_range("rent.min", low, low)
							build_query_should_range("rent.max", high, high)

					if(_sort_field):
							low = _sort_field.split('$')[0]
							high = _sort_field.split('$')[1]
							build_query_sort(low, high)

					if(_bhk):
							count = _bhk.count('$')
							if(count == 0):
								build_query_exists("bhk."+_bhk)
							else:
								count += 1
								temp = []
								z = 0
								while z!=count:
										temp.append(_bhk.split('$')[z])
										build_query_exists("bhk."+temp[z])
										z += 1

					if(_locationId):
							count = _locationId.count('$')
							if(count == 0):
									build_query_should("location."+_locationId, true)
							else:
									count += 1
									temp = []
									z = 0
									while z!=count:
											temp.append(_locationId.split('$')[z])
											build_query_should("location."+temp[z], true)
											z += 1

					if(_propertyType):
							count = _propertyType.count('$')
							if(count==0):
									build_query_should("propertyType."+_propertyType, true)
							else:
									count += 1
									temp = []
									z = 0
									while z!=count:
											temp.append(_propertyType.split('$')[z])
											build_query_should("propertyType."+temp[z], true)
											z += 1

					if(_amenity):
							count = _amenity.count('$')
							if(count==0):
									build_query_should("amenities."+_amenity, "Yes")
							else:
									count += 1
									temp = []
									z = 0
									while z!=count:
											temp.append(_amenity.split('$')[z])
											build_query_should("amenities."+temp[z], "Yes")
											z += 1

					res = es.search(index='live_index_1', doc_type='data', body=query_builder, from_=_page_start, size=_page_size)
					index_num = 0
					final_res = {}
					temp_res = {}
					final_res.update({'records': es.count(index='live_index_1')['count']})
					final_res.update({'hits': res['hits']['total']})
					while index_num<_page_size:
						bhk = []
						temp_temp_res = {}
						temp_temp_res.update({'id': res['hits']['hits'][index_num]['_source']['projectId']})
						temp_temp_res.update({'name': res['hits']['hits'][index_num]['_source']['details']['name']})
						temp_temp_res.update({'address': res['hits']['hits'][index_num]['_source']['address']})
						temp_temp_res.update({'cover': res['hits']['hits'][index_num]['_source']['cover_pic']})
						temp_temp_res.update({'area': res['hits']['hits'][index_num]['_source']['area']})
						temp_temp_res.update({'rent': res['hits']['hits'][index_num]['_source']['rent']})
						for key in res['hits']['hits'][index_num]['_source']['bhk']:
							bhk.append(key)
						bhk.sort()
						fbhk = ', '.join(str(e) for e in bhk)
						temp_temp_res.update({'bhks': fbhk})
						temp_res.update({index_num : temp_temp_res})
						index_num += 1
					final_res.update({'details': temp_res})
					return final_res    

				except:
					pass
