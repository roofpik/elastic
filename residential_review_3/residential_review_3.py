from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
#add decoder module - pending

#function to build must query
def build_query_must(field, value, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['match'] = {}
	query_builder['query']['bool']['must'][i]['match'][field] = value
	return query_builder

#function to build range query
def build_query_must_range(value, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['range'] = {}
	query_builder['query']['bool']['must'][i]['range']['overallRating'] = {}
	query_builder['query']['bool']['must'][i]['range']['overallRating']['gte'] = value
	return query_builder

class residentialreview3class(Resource):
	def get(self):
		try:
			#i is index for 'must'field in query builder that is to be incremented every time someone builds a query
			i = 0
			#initialize query build
			query_builder = {}
			query_builder['query'] = {}
			query_builder['query']['bool'] = {}
			query_builder['query']['bool']['must'] = []					
			
			#take arguments
			parser = reqparse.RequestParser()
			
			parser.add_argument('pid', type=str)
			args = parser.parse_args()
			_pid = args['pid']
			if not _pid:
				_pid = ""

			parser.add_argument('userType', type=str)
			args = parser.parse_args()
			_userType = args['userType']
			if not _userType:
				_userType = ""

			parser.add_argument('overallRating', type=int)
			args = parser.parse_args()
			_overallRating = args['overallRating']
			if not _overallRating:
					_overallRating = 0

			parser.add_argument('page_start', type=str)
			args = parser.parse_args()
			_page_start = args['page_start']
			if not _page_start:
					_page_start = '0'

			parser.add_argument('page_size', type=str)
			args = parser.parse_args()
			_page_size = args['page_size']
			if not _page_size:
					_page_size = '10'

			if(_pid):
				query_builder = build_query_must("pid", _pid, query_builder, i)
				i += 1

			if(_userType):
				query_builder = build_query_must("userType", _userType, query_builder, i)
				i += 1

			if(_overallRating):
				query_builder = build_query_must_range(_overallRating, query_builder, i)
				i += 1
			
			url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/res_reviews/reviews/_search?size='+_page_size+'&from='+_page_start	

			query_builder = json.dumps(query_builder)
			r = requests.post(url, data=query_builder)
			r = json.loads(r.text)
			r_count = r['hits']['total']
			
			final_res = {}
			d_res = {}
			final_res.update({'hits': r_count})
			result_count = 0
			if(r_count <= 10):
				page_counter = r_count
			else:
				page_counter = int(_page_size)
			#return data in format
			index = 0
			while index<page_counter:
				try:
					d = {}
					d.update({'userId':r['hits']['hits'][index]['_source']['userId']})
					d.update({'userName':r['hits']['hits'][index]['_source']['userName']})
					d.update({'overallRating':r['hits']['hits'][index]['_source']['overallRating']})
					d.update({'createdDate':r['hits']['hits'][index]['_source']['createdDate']})
					d.update({'reviewTitle':r['hits']['hits'][index]['_source']['reviewTitle']})
					d.update({'wordCount':r['hits']['hits'][index]['_source']['wordCount']})
					d.update({'reviewId':r['hits']['hits'][index]['_id']})
					d.update({'reviewText':r['hits']['hits'][index]['_source']['reviewText'][:400]})
					d_res.update({index : d})
					index += 1
					result_count += 1
				except:
					index += 1
					pass
			final_res.update({'details' : d_res})
			final_res.update({'hits': result_count})
			return final_res

		except:
			pass
