from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *


class emailclass(Resource):
	def get(self):
		return 'this works'

