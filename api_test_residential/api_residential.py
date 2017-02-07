from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

# def build_query_must(field, value, query_builder, i):
# 	query_builder['query']['bool']['must'].append({})
# 	query_builder['query']['bool']['must'][i]['match'] = {}
# 	query_builder['query']['bool']['must'][i]['match'][field] = value
# 	return query_builder

# def build_query_should(field, value, query_builder, j):
# 	query_builder['query']['bool']['should'].append({})
# 	query_builder['query']['bool']['should'][j]['match'] = {}
# 	query_builder['query']['bool']['should'][j]['match'][field] = value
# 	return query_builder

# def build_query_must_range(field, lower, upper, query_builder, i):
# 	query_builder['query']['bool']['must'].append({})
# 	query_builder['query']['bool']['must'][i]['range'] = {}
# 	query_builder['query']['bool']['must'][i]['range'][field] = {}
# 	query_builder['query']['bool']['must'][i]['range'][field]['from'] = lower
# 	query_builder['query']['bool']['must'][i]['range'][field]['to'] = upper
# 	return query_builder

# def build_query_should_range(field, lower, upper, query_builder, j):
# 	query_builder['query']['bool']['should'].append({})
# 	query_builder['query']['bool']['should'][j]['range'] = {}
# 	query_builder['query']['bool']['should'][j]['range'][field] = {}
# 	query_builder['query']['bool']['should'][j]['range'][field]['from'] = lower
# 	query_builder['query']['bool']['should'][j]['range'][field]['to'] = upper
# 	return query_builder

# def build_query_sort(field, asc_or_dsc, query_builder, k):
# 	query_builder['sort'].append({})
# 	query_builder['sort'][k][field] = {}
# 	query_builder['sort'][k][field]['order'] = asc_or_dsc
# 	return query_builder

# def build_query_exists(field, query_builder, i):
# 	query_builder['query']['bool']['must'].append({})
# 	query_builder['query']['bool']['must'][i]['constant_score'] = {}
# 	query_builder['query']['bool']['must'][i]['constant_score']['filter'] = {}
# 	query_builder['query']['bool']['must'][i]['constant_score']['filter']['exists'] = {}
# 	query_builder['query']['bool']['must'][i]['constant_score']['filter']['exists']['field'] = field
# 	return query_builder

# def build_query_price(lower, upper, query_builder, j):
# 	query_builder['query']['bool']['should'].append({})
# 	query_builder['query']['bool']['should'][j]['bool'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'] = []
# 	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range']['rent.min'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range']['rent.min']['lte'] = upper
# 	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range']['rent.max'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range']['rent.max']['gte'] = lower
# 	return query_builder

# def build_query_area(lower, upper, query_builder, j):
# 	query_builder['query']['bool']['should'].append({})
# 	query_builder['query']['bool']['should'][j]['bool'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'] = []
# 	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range']['area.min'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range']['area.min']['lte'] = upper
# 	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range']['area.max'] = {}
# 	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range']['area.max']['gte'] = lower
# 	return query_builder

class residentialclass(Resource):
	def get(self):
		try:
			return 'works'
			i = 0
			j = 0
			k = 0
			
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
			
			if(_style):
				count = _style.count('$')
				if(count == 0):
					query_builder = build_query_must("style", _style, query_builder, i)
					i += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						temp.append(_style.split('$')[z])
						query_builder = build_query_must("style", temp[z], query_builder, i)
						i += 1
						z += 1

			if(_details_name):
				query_builder = build_query_must("details.name", _details_name, query_builder, i)
				i += 1

			if(_details_builder):
				query_builder = build_query_must("details.builder", _details_builder, query_builder, i)
				i += 1

			if(_area_range):
				low = _area_range.split('$')[0]
				high = _area_range.split('$')[1]
				query_builder = build_query_area(low, high, query_builder, j)
				j += 1
				query_builder = build_query_area(low, high, query_builder, j)
				j += 1

			if(_price_range):
				low = _price_range.split('$')[0]
				high = _price_range.split('$')[1]
				query_builder = build_query_price(low, high, query_builder, j)
				j += 1

			if(_sort_field):
				low = _sort_field.split('$')[0]
				high = _sort_field.split('$')[1]
				query_builder = build_query_sort(low, high, query_builder, k)
				k += 1

			if(_bhk):
				count = _bhk.count('$')
				if(count == 0):
					query_builder = build_query_exists("bhk."+_bhk, query_builder, i)
					i += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						temp.append(_bhk.split('$')[z])
						query_builder = build_query_exists("bhk."+temp[z], query_builder, i)
						i += 1
						z += 1

			if(_locationId):
				count = _locationId.count('$')
				if(count == 0):
					query_builder = build_query_should("location."+_locationId, True, query_builder, j)
					j += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						temp.append(_locationId.split('$')[z])
						query_builder = build_query_should("location."+temp[z], True, query_builder, j)
						j += 1
						z += 1

			if(_propertyType):
				count = _propertyType.count('$')
				if(count==0):
					query_builder = build_query_should("propertyType."+_propertyType, True, query_builder, j)
					j += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						temp.append(_propertyType.split('$')[z])
						query_builder = build_query_should("propertyType."+temp[z], True, query_builder, j)
						j += 1
						z += 1

			if(_amenity):
				count = _amenity.count('$')
				if(count==0):
					query_builder = build_query_should("amenities."+_amenity, "Yes", query_builder, j)
					j += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						temp.append(_amenity.split('$')[z])
						query_builder = build_query_should("amenities."+temp[z], "Yes", query_builder, j)
						j += 1
						z += 1
<<<<<<< HEAD
<<<<<<< HEAD
	
=======
			return 'works'
=======
>>>>>>> 2f3c144cc827309a9352827a9bdc2a701474db4f
			#return query_builder
>>>>>>> 5e71dfc237e5331a681e59ff1d03f51dbd85e3ec
			res = es.search(index='res_index', doc_type='data', body=query_builder, from_=_page_start, size=_page_size)
			index_num = 0
			final_res = {}
			temp_res = {}
			final_res.update({'records': es.count(index='res_index')['count']})
			final_res.update({'hits': res['hits']['total']})
			while index_num<res['hits']['total']:
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


		except Exception:
			return Exception
