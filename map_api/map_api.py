import json
import requests
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs

#send rating if available else return 0
def getRating(id, url):
	q = {"query":{"match":{"pid":id}}}
	q = json.dumps(q)
	res = requests.post(url, data = q)
	res = json.loads(res.text)
	try:
		return res['hits']['hits'][0]['_source']['rating']
	except:
		return 0

#send location and locality data
def getLocations(url1):
	res1 = requests.post(url1)
	res1 = json.loads(res1.text)
	size = res1['hits']['total']
	res1 = requests.post(url1+'?size='+str(size))
	res1 = json.loads(res1.text)
	temp2 = {}
	i=0
	while i<size:
		temp1 = {}
		temp1.update({'id':res1['hits']['hits'][i]['_source']['id']})
		temp1.update({'rating':'NA'})
		temp1.update({'cover':'NA'})
		temp1.update({'rent':'NA'})
		temp1.update({'bhks':'NA'})
		temp1.update({'location':res1['hits']['hits'][i]['_source']['location']})
		temp1.update({'type':res1['hits']['hits'][i]['_source']['type']})
		temp1.update({'name':res1['hits']['hits'][i]['_source']['name']})
		temp2.update({res1['hits']['hits'][i]['_source']['id']:temp1})
		i += 1
	return temp2

#send project data
def getProjects(distance_query, url, project_type, url4):	
	res1 = requests.post(url)
	res1 = json.loads(res1.text)
	size = res1['hits']['total']
	res1 = requests.post(url+'?size='+str(size))
	res1 = json.loads(res1.text)
	i=0
	temp2 = {}
	while i<size:
		temp1 = {}
		temp1.update({'id':res1['hits']['hits'][i]['_source']['projectId']})
		id = res1['hits']['hits'][i]['_source']['projectId']
		rating = getRating(id, url4)
		temp1.update({'rating':rating})
		bhk = []
		for key in res['hits']['hits'][i]['_source']['bhk']:
			bhk.append(key)
		bhk.sort()
		fbhk = ', '.join(str(e) for e in bhk)
		temp1.update({'bhks': fbhk})
		temp1.update({'cover':res1['hits']['hits'][i]['_source']['cover_pic']})
		temp1.update({'rent':res1['hits']['hits'][i]['_source']['rent']})
		temp1.update({'location':res1['hits']['hits'][i]['_source']['coordinates']})
		temp1.update({'name':res1['hits']['hits'][i]['_source']['details']['name']})
		temp1.update({'type':project_type})
		temp2.update({id:temp1})
		i += 1
	return temp2

class mapapiclass(Resource):
	def get(self):
		#urls for different es indices
		url1 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/locality_geo/data/_search'
		url2 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/cghs_index/data/_search'
		url3 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/residential_index/data/_search'
		url4 = 'https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/rating_projects/data/_search'

		#single argument to be decoded using decodeArgs

		#checking available parameters and allocating variables accordingly
		
		#query for different indices - due to difference in naming of fields
		#distance_query_location = { "query": { "bool" : { "must" : { "match_all" : {} }, "filter" : { "geo_distance" : { "distance" : _distance+"km", "location" : { "lat" : float(_lat), "lon" : float(_lon) } } } } } }
		
		#distance_query_location = json.dumps(distance_query_location)

		#distance_query_projects = { "query": { "bool" : { "must" : { "match_all" : {} }, "filter" : { "geo_distance" : { "distance" : _distance+"km", "coordinates" : { "lat" : float(_lat), "lon" : float(_lon) } } } } } }

		#distance_query_projects = json.dumps(distance_query_projects)
		
		result = {}
		#add data to final result accordingly - check comments above function definitions
		result.update(getLocations(url1))
		result.update(getProjects(url2, "cghs", url4))
		result.update(getProjects(url3, "residential", url4))

		return result
