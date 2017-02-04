from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

class testclass2(Resource):
        def get(self):
			d = {}
			d.update({'city1': 'Gurgaon'})
			d.update({'city2': 'Faridabad'})
			d.update({'city3': 'Noida'})
			d.update({'city4': 'Delhi'})
			d.update({'city5': 'Ghaziabad'})
			return d

