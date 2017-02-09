from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

def build_query_must(field, value, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['match'] = {}
	query_builder['query']['bool']['must'][i]['match'][field] = value
	return query_builder

def build_query_must_range(value, query_builder, i):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][i]['range'] = {}
	query_builder['query']['bool']['must'][i]['range']["overallRating"] = {}
	query_builder['query']['bool']['must'][i]['range']["overallRating"]['gte'] = value
	return query_builder

class residentialreview3class(Resource):
	def get(self):
		try:
			i = 0
			
			query_builder = {}
			query_builder['query'] = {}
			query_builder['query']['bool'] = {}
			query_builder['query']['bool']['must'] = []					
			
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
			if not _overallRating:
					_overallRating = ""

			if(_pid):
				query_builder = build_query_must("pid", _pid, query_builder, i)
				i += 1

			if(_userType):
				query_builder = build_query_must("userType", _userType, query_builder, i)
				i += 1

			if(_overallRating):
				query_builder = build_query_must(_overallRating, query_builder, i)
				i += 1

			url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/res_reviews/reviews/_search'

			r = requests.post(url, data=query_builder)
			r = json.loads(r.text)
			return r
