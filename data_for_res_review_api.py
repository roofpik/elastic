import requests
import json
from flask import *
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

r = requests.request('get', 'https://roofpik-948d0.firebaseio.com/reviews/-KYJONgh0P98xoyPPYm9/residential.json')

data = r.json()

def getAverageRating(temp_res, t_reviews):
	sum = 0.0
	k = 0
	while k<temp_res['hits']['total']:
		try:
			sum = sum + int(temp_res['hits']['hits'][k]['_source']['overallRating'])
		except:
			pass
		k += 1
	return sum/t_reviews

def getIndividualRatingCount(temp_res):
	l = [0, 0, 0, 0, 0]
	k = 0
	while k<temp_res['hits']['total']:
		try:
			l[int(temp_res['hits']['hits'][k]['_source']['overallRating']) - 1] += 1
		except:
			pass
		k += 1
	return l

def checkExistance(query_builder, field):
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][1]['constant_score'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter']['exists'] = {}
	query_builder['query']['bool']['must'][1]['constant_score']['filter']['exists']['field'] = field
	return query_builder

def getParamsRating(query_builder, temp_num_reviews):
	ratingParamsNum = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	ratingParamsRating = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	finParamsRating = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	ratingParams = ['layoutOfApartment', 'electricityAndWaterSupply', 'convenienceOfParking', 'openAndGreenAreas', 'convenienceOfHouseMaids', 'infrastructure', 'amenities', 'security']
	k = 0
	while k<8:
		temp_s = es.search(index='res_reviews', doc_type='reviews', body=checkExistance(query_builder, 'ratings.'+ratingParams[k]), size=temp_num_reviews)
		j = 0
		while j<temp_s['hits']['total']: 
			ratingParamsRating[k] = ratingParamsRating[k] + int(temp_s['hits']['hits'][j]['_source']['ratings'][ratingParams[k]])
			j+=1
		ratingParamsNum[k] = temp_s['hits']['total']
		if(ratingParamsNum[k]==0):
			ratingParamsNum[k] = 1
		finParamsRating[k] = ratingParamsRating[k] / ratingParamsNum[k]
		finParamsRating[k] = round(finParamsRating[k], 2)
		k+=1
	return finParamsRating

d = {}

for pid in data:

	getPid = {'query':{'match':{'pid':pid}}}
	temp_temp_res = es.search(index='res_reviews', doc_type='reviews', body=getPid)
	temp_num_reviews = temp_temp_res['hits']['total']
	temp_res = es.search(index='res_reviews', doc_type='reviews', body=getPid, size=temp_num_reviews)
	t_reviews = temp_res['hits']['total']

	query_builder = {}
	query_builder['query'] = {}
	query_builder['query']['bool'] = {}
	query_builder['query']['bool']['must'] = []
	query_builder['query']['bool']['must'].append({})
	query_builder['query']['bool']['must'][0]['match'] = {}
	query_builder['query']['bool']['must'][0]['match']['pid'] = pid

	d.update({'averageRating':getAverageRating(temp_res, t_reviews)})
	d.update({'numberOfReviews':temp_res['hits']['total']})
	ind_rating = getIndividualRatingCount(temp_res)
	param_rating = getParamsRating(query_builder, temp_num_reviews)
	d.update({'oneStar':ind_rating[0]})
	d.update({'twoStar':ind_rating[1]})
	d.update({'threeStar':ind_rating[2]})
	d.update({'fourStar':ind_rating[3]})
	d.update({'fiveStar':ind_rating[4]})
	d.update({'layoutOfApartment':param_rating[0]})
	d.update({'electricityAndWaterSupply':param_rating[1]})
	d.update({'convenienceOfParking':param_rating[2]})
	d.update({'openAndGreenAreas':param_rating[3]})
	d.update({'convenienceOfHouseMaids':param_rating[4]})
	d.update({'infrastructure':param_rating[5]})
	d.update({'amenities':param_rating[6]})
	d.update({'security':param_rating[7]})

	es.index(index="reviews", doc_type="reviews", id=pid, body=d)


