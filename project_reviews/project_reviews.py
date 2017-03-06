from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
#add decoder module - pending

#function to build must query
#build must query if there is a single value in a type
def build_query_must(field, value, query_builder, i, z):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['bool'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'] = []
	return build_actual_query_must(field,value, query_builder, i, z)

#function called automatically if there are multiple values of a single type
def build_actual_query_must(field, value, query_builder, i, z):
	query_builder['query']['bool']['must'][i]['bool']['should'].append({})
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['match'] = {}
	query_builder['query']['bool']['must'][i]['bool']['should'][z]['match'][field] = value
	return query_builder

class projectreviewsclass(Resource):
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

			parser.add_argument('overallRating', type=str)
			args = parser.parse_args()
			_overallRating = args['overallRating']
			if _overallRating=='0':
					_overallRating = '5$4$3$2$1'

			parser.add_argument('page_start', type=str)
			args = parser.parse_args()
			_page_start = args['page_start']
			if not _page_start:
					_page_start = '0'

			parser.add_argument('type', type=str)
			args = parser.parse_args()
			_type = args['type']
			if not _type:
				_type = 'project'

			parser.add_argument('page_size', type=str)
			args = parser.parse_args()
			_page_size = args['page_size']
			if not _page_size:
					_page_size = '10'

			if(_pid):
				query_builder = build_query_must("pid", _pid, query_builder, i, 0)
				i += 1

			if(_userType):
				query_builder = build_query_must("userType", _userType, query_builder, i, 0)
				i += 1

			if _overallRating:
				count = _overallRating.count('$')
				if(count == 0):
					query_builder = build_query_must("overallRating", _overallRating, query_builder, i, 0)
					i += 1
				else:
					count += 1
					temp = []
					z = 0		
					while z!=count:
						if(z==0):
							temp.append(_overallRating.split('$')[z])
							query_builder = build_query_must("overallRating", temp[z], query_builder, i, z)
							z += 1
						else:
							temp.append(_overallRating.split('$')[z])
							query_builder = build_actual_query_must("overallRating", temp[z], query_builder, i, z)
							z += 1
					i += 1

			if _type=='project':
				url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/res_reviews,cghs_reviews/reviews/_search?size='+_page_size+'&from='+_page_start

			if _type=='location':
				url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/location_reviews/reviews/_search?size='+_page_size+'&from='+_page_start

			if _type=='locality':
				url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_reviews/reviews/_search?size='+_page_size+'&from='+_page_start	

			query_builder = json.dumps(query_builder)
			r = requests.post(url, data=query_builder)
			r = json.loads(r.text)
			r_count = r['hits']['total']
			
			final_res = {}
			d_res = {}
			result_count = 0
			if(r_count <= 10):
				page_counter = r_count
			else:
				page_counter = int(_page_size)
			#return data in format
			n_hits = 0
			index = 0
			while index<page_counter:
				try:
					d = {}
					d.update({'userId':r['hits']['hits'][index]['_source']['userId']})
					d.update({'userName':r['hits']['hits'][index]['_source']['userName']})
					d.update({'overalloverallRating':r['hits']['hits'][index]['_source']['overalloverallRating']})
					d.update({'createdDate':r['hits']['hits'][index]['_source']['createdDate']})
					try:
						title = r['hits']['hits'][index]['_source']['reviewTitle']
					except:
						title = r['hits']['hits'][index]['_source']['reviewText'].partition('.')[0]
					d.update({'reviewTitle':title})
					d.update({'wordCount':r['hits']['hits'][index]['_source']['wordCount']})
					d.update({'reviewId':r['hits']['hits'][index]['_id']})
					try:
						text = r['hits']['hits'][index]['_source']['reviewText'][:400]
					except:
						text = title
					d.update({'reviewText':text})
					d_res.update({index : d})
					index += 1
					result_count += 1
				except:
					index += 1
					n_hits += 1
					pass
			final_res.update({'details' : d_res})
			final_res.update({'hits': r_count-n_hits})
			return final_res

		except:
			pass
