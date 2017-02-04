from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

class cghsclass(Resource):
        def get(self):
		return 'cghs space'
