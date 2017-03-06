import requests
import json
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
import pyrebase
import time

def update_user(db, data, operation, temp_stamp, userId):
	for x in data:
		if data[x]['userId'] == temp_stamp:
			db.child('userActivity').child(operation).child(x).update({'userId':userId})
	return db

class useractivityclass(Resource):
	def get(self):

		#creating connection to firebase 
		config = {
    			'apiKey': "AIzaSyAapASzaLGFxHgbMpu9Cibfn97MSEheCcU",
    			'authDomain': "roofpik-f8f55.firebaseapp.com",
    			'databaseURL': "https://roofpik-f8f55.firebaseio.com",
    			'storageBucket': "roofpik-f8f55.appspot.com",
    			'messagingSenderId': "303104341936"
  		}

		firebase = pyrebase.initialize_app(config)
		#db stores storage details		
		db = firebase.database()

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']
		#decoding arguments
		_args = decodeArgs(_args)

		if 'token' in _args.keys():
			_token = _args['token']
			del _args['token']
		else:
			return 'token not provided'
		if _token=='custom':
			db.child('userActivity').remove()
			return 'parent node userActivity deleted'

		if 'operation' in _args.keys():
			_operation = _args['operation']
			del _args['operation']
		else:
			return 'no operation(like, dislike, bookmark...) specified'

		#if token is random, insert data in timestamp
		if _token == 'random':
			stamp = int(time.time() * 1000)
			checker = 0
			_args.update({'userId':stamp})
			_args.update({'createdDate':stamp})
			db.child('userActivity').child(_operation).push(_args)
			return stamp

		elif '$' in _token:
			#split the token to recieve previously set custom key and userId
			userId = _token.split('$')[0]
			temp_stamp = _token.split('$')[1]
			temp_stamp = int(temp_stamp)
			#get data from previous key
			temp = db.child('userActivity').child(_operation).get()
			temp = json.loads(json.dumps(temp.val()))
			#update previously set temporary stamp to actual userId
			update_user(db, temp, _operation, temp_stamp, userId)
			return userId

		else:
			userId = _token
			stamp = int(time.time() * 1000)
			_args.update({'userId':userId})
			_args.update({'createdDate':stamp})
			db.child('userActivity').child(_operation).push(_args)
			return stamp