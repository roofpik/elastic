from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

class testclass2(Resource):
        def get(self):
		
        	return 'return this'
