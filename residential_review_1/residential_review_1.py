from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

class residentialreview1class(Resource):
	def get(self):
		url = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/r_reviews/reviews/_search'

		parser.add_argument('id', type=str)
		args = parser.parse_args()
		_id = args['id']

		d = {}
 		d.update({'averageRating':0})
 		d.update({'numberOfReviews':0})
 		d.update({'oneStar':0})
 		d.update({'twoStar':0})
 		d.update({'threeStar':0})
 		d.update({'fourStar':0})
 		d.update({'fiveStar':0})
 		d.update({'layoutOfApartment':0})
 		d.update({'electricityAndWaterSupply':0})
 		d.update({'convenienceOfParking':0})
 		d.update({'openAndGreenAreas':0})
 		d.update({'convenienceOfHouseMaids':0})
 		d.update({'infrastructure':0})
 		d.update({'amenities':0})
 		d.update({'security':0})

		query = {"query": {"match": {"_id": _id}}}

		r = requests.post(url, data=query)
		try:
			return r['hits']['hits'][0]['_source']
		except:
			return d		
