from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *

class residentialreview1class(Resource):
	def get(self):

		parser = reqparse.RequestParser()
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
		
		url = 'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/r_reviews/reviews/' + _id
		
		r = requests.get(url)
		r = json.loads(r.text)
		try:
			temp = {}
			temp1 ={}
			temp2 = {}
			temp1.update({r['_source']['24x7electricity']})
			temp1.update({r['_source']['apartmentLayoutEfficient']})
			temp1.update({r['_source']['dailyNeedItems']})
			temp1.update({r['_source']['easyAccessToPublicTransport']})
			temp1.update({r['_source']['goodHospitals']})
			temp1.update({r['_source']['goodSchools']})			
			temp1.update({r['_source']['markets']})
			temp1.update({r['_source']['regularCleanWaterSupply']})
			temp.update({'yes_no':temp1})
			temp2.update({r['source']['amenities']})
			temp2.update({r['source']['averageRating']})
			temp2.update({r['source']['convenienceOfHouseMaids']})
			temp2.update({r['source']['convenienceOfParking']})
			temp2.update({r['source']['fiveStar']})
			temp2.update({r['source']['fourStar']})
			temp2.update({r['source']['infrastructure']})
			temp2.update({r['source']['numberOfReviews']})
			temp2.update({r['source']['twoStar']})
			temp2.update({r['source']['oneStar']})
			temp2.update({r['source']['threeStar']})
			temp2.update({r['source']['openAndGreenAreas']})
			temp2.update({r['source']['security']})
			temp.update({'numbers':temp2})
			return temp
		except:
			return d		
