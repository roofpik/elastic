from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch
from decoder import decodeArgs

#check all comments before pushing code

def returnResults(res, r_count, _page_size):
	index_num = 0
	final_res = {}
	temp_res = {}
	final_res.update({'records': r_count})
	final_res.update({'hits': res['hits']['total']})
			
	if(res['hits']['total'] <= 10):
		page_counter = res['hits']['total']
	else:
		page_counter = int(_page_size)

	while index_num<page_counter:
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

#except for cghs in residential,select vertical and build query (propertyType mainly)
def select_category_residential(_propertyType, query_builder, i):
	count = _propertyType.count('$')
	if(count==0):
		query_builder = build_query_must("propertyType."+_propertyType, True, query_builder, i, 0)
		i += 1
	else:
		count += 1
		temp = []
		z = 0
		while z!=count:
			if(z==0):
				temp.append(_propertyType.split('$')[z])
				query_builder = build_query_must("propertyType."+temp[z], True, query_builder, i, z)
				z += 1
			else:
				temp.append(_propertyType.split('$')[z])
				query_builder = build_actual_query_must("propertyType."+temp[z], True, query_builder, i, z)
				z += 1			
		i += 1
	r_list = []
	r_list.append(query_builder)
	r_list.append(i)
	return r_list

#create filter for locationId, propertyType and amenity, irrespective of url selected
def select_filter_must(_type, field, val, query_builder, i):
	count = field.count('$')
	if(count == 0):
		query_builder = build_query_must(_type+field, query_builder, i, 0)
		i += 1
	else:
		count += 1
		temp = []
		z = 0
		while z!=count:
			if(z==0):
				temp.append(field.split('$')[z])
				query_builder = build_query_must(_type+temp[z], val, query_builder, i, z)
				z += 1
			else:
				temp.append(field.split('$')[z])
				query_builder = build_actual_query_must(_type+temp[z], val, query_builder, i, z)
				z += 1
		i+=1
	r_list = []
	r_list.append(query_builder)
	r_list.append(i)
	return r_list

def build_query_must(field, value, query_builder, i, z):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['bool'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'] = []
	return build_actual_query_must(field,value, query_builder, i, z)

def build_actual_query_must(field, value, query_builder, i, z):
	query_builder['query']['bool']['must'][i]['bool']['should'].append({})
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['match'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['match'][field] = value
	return query_builder

def build_query_must_range(field, lower, upper, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['range'] = {}
	query_builder['query']['bool']['must'][i]['range'][field] = {}
	query_builder['query']['bool']['must'][i]['range'][field]['from'] = lower
	query_builder['query']['bool']['must'][i]['range'][field]['to'] = upper
	return query_builder

def build_query_sort(field, asc_or_dsc, query_builder, k):
	query_builder['sort'].append({})
	query_builder['sort'][k][field] = {}
	query_builder['sort'][k][field]['order'] = asc_or_dsc
	return query_builder

def build_query_exists(field, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['bool'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'] = []
	return build_actual_query_exists(field, query_builder, i ,z)

def build_actual_query_exists(field, query_builder, i ,z):
	query_builder['query']['bool']['must'][i]['bool']['should'].append({})
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['constant_score'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['constant_score']['filter'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['constant_score']['filter']['exists'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['constant_score']['filter']['exists']['field'] = field
	return query_builder

def build_query_range(_type, lower, upper, query_builder, j):
	query_builder['query']['bool']['should'].append({})
	query_builder['query']['bool']['should'][j]['bool'] = {}
	query_builder['query']['bool']['should'][j]['bool']['must'] = []
	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range'] = {}
	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range'][_type+'.min'] = {}
	query_builder['query']['bool']['should'][j]['bool']['must'][0]['range'][_type+'.min']['lte'] = upper
	query_builder['query']['bool']['should'][j]['bool']['must'].append({})
	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range'] = {}
	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range'][_type+'.max'] = {}
	query_builder['query']['bool']['should'][j]['bool']['must'][1]['range'][_type+'.max']['gte'] = lower
	return query_builder

class listingclass(Resource):
	def get(self):
		try:

			#list index for must
			i = 0
			#list index for should
			j = 0
			#list index for sort
			k = 0

			#just to check connection to es, can be ommited
			try:		
				es = requests.get('https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com')		
			except:
				return 'connection to es not established'

			#initialize query builder, always pass and return this in every function related to building query
			query_builder = {}
			query_builder['query'] = {}
			query_builder['query']['bool'] = {}
			query_builder['query']['bool']['must'] = []
			query_builder['query']['bool']['should'] = []
			query_builder['sort'] = []					
			
			#passing and decoding args
			parser = reqparse.RequestParser()
			parser.add_argument('args', type=str)
			args = parser.parse_args()
			_args = args['args']
			if not _args:
				return "no category selected"
	
			_args = decodeArgs(_args)

			#not using this as of now
			if 'type' in _args.keys():
				_list_type = _args['type']

			if 'vertical' in _args.keys():
				_vertical = _args['vertical']
			else:
				return 'no vertical selected'

			if 'category' in _args.keys():
				_category = _args['category']
			else:
				return 'no category selected in '+_vertical

			#checking category and vertical to call url accordingly
			if(_vertical == 'residential'):
				url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/residential_index/data/_search'

				if(_category == 'CGHS'):
					url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/cghs_index/data/_search'

				else:
					try:
						return_list = select_category_residential(_category, query_builder, i)
						query_builder = return_list[0]
						i = return_list[1]
					except:
						return 'not a valid category in residential'

			elif(_vertical == 'commercial'):
				return 'no data as of yet'

			elif(_vertical == 'pg'):
				return 'no data as of yet'

			else:
				return 'not a valid vertical'

			#taking other arguments from _args
			if 'style' in _args.keys():
				_style = _args['style']
			else:
				_style = ""

			if 'details_name' in _args.keys():
				_details_name = _args['details_name']
			else:
				_details_name = ""

			if 'details_builder' in _args.keys():
				_details_builder = _args['details_builder']
			else:
				_details_builder = ""

			if 'area_range' in _args.keys():
				_area_range = _args['area_range']
			else:
				_area_range = ""

			if 'price_range' in _args.keys():
				_price_range = _args['price_range']
			else:
				_price_range = ""

			if 'sort_field' in _args.keys():
				_sort_field = _args['sort_field']
			else:
				_sort_field = ""

			if 'bhk' in _args.keys():
				_bhk = _args['bhk']
			else:
				_bhk = ""

			if 'locationId' in _args.keys():
				_locationId = _args['locationId']
			else:
				_locationId = ""

			if 'propertyType' in _args.keys():
				_propertyType = _args['propertyType']
			else:
				_propertyType = ""

			if 'amenity' in _args.keys():
				_amenity = _args['amenity']
			else:
				_amenity = ""

			if 'page_start' in _args.keys():
				_page_start = _args['page_start']
			else:
				_page_start = '0'

			if 'page_size' in _args.keys():
				_page_size = _args['page_size']
			else:
				_page_size = '10'

			#don't change anything above this
			if(_style):
				count = _style.count('$')
				if(count == 0):
					query_builder = build_query_must("style", _style, query_builder, i, 0)
					i += 1
				else:
					count += 1
					temp = []
					z = 0		
					while z!=count:
						if(z==0):
							temp.append(_style.split('$')[z])
							query_builder = build_query_must("style", temp[z], query_builder, i, z)
							z += 1
						else:
							temp.append(_style.split('$')[z])
							query_builder = build_actual_query_must("style", temp[z], query_builder, i, z)
							z += 1
					i += 1

			#flag
			#
			if(_details_name):
				query_builder = build_query_must("details.name", _details_name, query_builder, i)
				i += 1
		
			#build definitions for build multi query must and build multi query should
			if(_details_builder):
				count = _style.count('$')
				if(count == 0):
					query_builder = build_query_must("details.builder", _details_builder, query_builder, i, 0)
					i += 1
				else:
					count += 1
					temp = []
					z = 0		
					while z!=count:
						if(z==0):
							temp.append(_details_builder.split('$')[z])
							query_builder = build_query_must("details.builder", temp[z], query_builder, i, z)
							z += 1
						else:
							temp.append(_details_builder.split('$')[z])
							query_builder = build_actual_query_must("details.builder", temp[z], query_builder, i, z)
							z += 1
					i += 1

			if(_area_range):
				low = _area_range.split('$')[0]
				high = _area_range.split('$')[1]
				query_builder = build_query_range('area', low, high, query_builder, j)
				j += 1

			if(_price_range):
				low = _price_range.split('$')[0]
				high = _price_range.split('$')[1]
				query_builder = build_query_range('price', low, high, query_builder, j)
				j += 1

			if(_sort_field):
				low = _sort_field.split('$')[0]
				high = _sort_field.split('$')[1]
				query_builder = build_query_sort(low, high, query_builder, k)
				k += 1

			if(_bhk):
				count = _bhk.count('$')
				if(count == 0):
					query_builder = build_query_exists("bhk."+_bhk, query_builder, i, 0)
					i += 1
				else:
					count += 1
					temp = []
					z = 0
					while z!=count:
						if(z==0):
							temp.append(_bhk.split('$')[z])
							query_builder = build_query_exists("bhk."+temp[z], query_builder, i, z)
							z += 1
						else:
							temp.append(_bhk.split('$')[z])
							query_builder = build_actual_query_exists("bhk."+temp[z], query_builder, i, z)
							z += 1
					i+=1

			return 'works'
			#call select_filter_must
			if(_locationId):
				return_list = select_filter_must("location.", _locationId, True, query_builder, i)
				query_builder = return_list[0]
				i = return_list[1]

			if(_propertyType):
				return_list = select_filter_must("propertyType.", _propertyType, True, query_builder, i)
				query_builder = return_list[0]
				i = return_list[1]

			if(_amenity):
				return_list = select_filter_must("amenities.", _amenity, "Yes", query_builder, i)
				query_builder = return_list[0]
				i = return_list[1]

			query_builder = json.dumps(query_builder)
			#return query_builder
			#requesting data from index
			url = url+'?size='+_page_size+'&from='+_page_start
			try:
				res = requests.post(url, data=query_builder)
				
				res = json.loads(res.text)

			except:
				return 'unable to call es.search'

			try:
				r_count = requests.post(url)
				r_count = json.loads(r_count.text)
				r_count = r_count['hits']['total']
			except:
				return 'unable to count records'

			#processing object before returning
			result = returnResults(res, r_count, _page_size)
			return result
			#check all comments before pushing code
		except Exception:
			return Exception
