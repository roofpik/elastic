from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

def getAverageRating(temp_res, t_reviews):
	sum = 0.0
	k = 0
	while k<temp_res['hits']['total']:
		sum = sum + int(temp_res['hits']['hits'][k]['_source']['overallRating'])
		k += 1
	return sum/t_reviews

def getIndividualRatingCount(temp_res):
	l = [0, 0, 0, 0, 0]
	k = 0
	while k<temp_res['hits']['total']:
		l[int(temp_res['hits']['hits'][k]['_source']['overallRating']) - 1] += 1
		k += 1
	return l

def checkExistence(query_builder, field):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][1]['constant_score'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter']['exists'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter']['exists']['field'] = field
	return query_builder

def instantiate():
	query_builder = {}
	query_builder['query'] = {}
	query_builder['query']['bool'] = {}
	query_builder['query']['bool']['must'] = []
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][0]['match'] = {}
	query_builder['query']['bool']['must'][0]['match']['pid'] = _projectId
	return query_builder

def getParamsRating(query_builder, temp_num_reviews, es):
	ratingParamsNum = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	ratingParamsRating = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	finParamsRating = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	ratingParams = ['layoutOfApartment', 'electricityAndWaterSupply', 'convenienceOfParking', 'openAndGreenAreas', 'convenienceOfHouseMaids', 'infrastructure', 'amenities', 'security']
	k = 0
	while k<8:
		temp_s = es.search(index='res_reviews', doc_type='reviews', body=checkExistence(instantiate(), 'ratings.'+ratingParams[k]), size=temp_num_reviews)
		j = 0
		while j<temp_s['hits']['total']: 
			ratingParamsRating[k] = ratingParamsRating[k] + int(temp_s['hits']['hits'][j]['_source']['ratings'][ratingParams[k]])
			j+=1
		ratingParamsNum[k] = temp_s['hits']['total']
		finParamsRating[k] = ratingParamsRating[k] / ratingParamsNum[k]
		finParamsRating[k] = round(finParamsRating[k], 2)
		k+=1
	return finParamsRating

class resReviewclass(Resource):
	def get(self):
		try:
			es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
			
			parser = reqparse.RequestParser()
			parser.add_argument('projectId', type=str)
			args = parser.parse_args()
			_projectId = args['projectId']

			getPid = {'query':{'match':{'pid':_projectId}}}
			temp_temp_res = es.search(index='res_reviews', doc_type='reviews', body=getPid)
			temp_num_reviews = temp_temp_res['hits']['total']
			temp_res = es.search(index='res_reviews', doc_type='reviews', body=getPid, size=temp_num_reviews)
			t_reviews = temp_res['hits']['total']

			result = {}
			result.update({'overallRating' : getAverageRating(temp_res, t_reviews)})
			result.update({'numberOfReviews' : t_reviews})
			result.update({'oneStar' : getIndividualRatingCount(temp_res)[0]})
			result.update({'twoStar' : getIndividualRatingCount(temp_res)[1]})
			result.update({'threeStar' : getIndividualRatingCount(temp_res)[2]})
			result.update({'fourStar' : getIndividualRatingCount(temp_res)[3]})
			result.update({'fiveStar' : getIndividualRatingCount(temp_res)[4]})
			paramsRating = getParamsRating(query_builder, t_reviews, es)
			result.update({'layoutOfApartment' : paramsRating[0]})
			result.update({'electricityAndWaterSupply' : paramsRating[1]})
			result.update({'convenienceOfParking' : paramsRating[2]})
			result.update({'openAndGreenAreas' : paramsRating[3]})
			result.update({'convenienceOfHouseMaids' : paramsRating[4]})
			result.update({'infrastructure': paramsRating[5]})
			result.update({'amenities' : paramsRating[6]})
			result.update({'security' : paramsRating[7]})
			return result
		
		except Exception:
			return Exception

