from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

class residentialreview2class(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('id', type=str)
		args = parser.parse_args()
		_id = args['id']

		url = 'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/res_reviews/reviews/' + _id

		r = requests.get(url)
		r = json.loads(r.text)
		try:		
			return r['_source']
		except:
			return 'record not found'

