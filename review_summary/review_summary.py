from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

class reviewsummaryclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('id', type=str)
		args = parser.parse_args()
		_id = args['id']
		parser.add_argument('type', type=str)
		args = parser.parse_args()
		_type = args['type']
		
		if not _type:
			_type='project'

		d = {_id:'not found'}
		
		if _type=='project':
			url = 'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/r_reviews/reviews/' + _id
		elif _type=='locality':
			url = 'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/localitysummary_reviews/reviews/' + _id
		elif _type=='location':
			url = 'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locationsummary_reviews/reviews/' + _id
		
		r = requests.get(url)
		r = json.loads(r.text)
		try:
			temp = {}
			temp1 ={}
			temp2 = {}
			for element in r['_source']:
				if isinstance(r['_source'][element],dict):
					temp1.update({element:r['_source'][element]})
				else:
					temp2.update({element:r['_source'][element]})
			temp.update({'yes_no':temp1})
			temp.update({'numbers':temp2})
			return temp
		except:
			return d		
