import requests
import json
from restful import Resource
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
import pyrebase
import time

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

		if 'id' in _args.keys():
			_id = _args['id']
			del _args['id']

		else:
			return 'no id specified'

		if 'operation' in _args.keys():
			_operation = _args['operation']
			del _args['operation']

		else:
			return 'no operation(like, dislike, bookmark...) specified'
		
		#if token is random, insert data in timestamp
		if _token == 'random':
			stamp = int(time.time())
			counter = 0
			for key,val in _args.items():
				#for first entry, use 'set' to set custom key
				if counter==0:
					db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).set({key:val})
					counter += 1
				#second entry onwards, use update 
				else:
					db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).update({key:val})
			db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).update({'createdDate':int(time.time())})
			return stamp

		elif '$' in _token:
			#split the token to recieve previously set custom key and userId
			userId = _token.split('$')[0]
			replacee = _token.split('$')[1]
			replacee = int(replacee)
			#get data from previous key
			try:
				temp = db.child('userActivity').child(replacee).get()
			except:
				return 'custom key not found'
			temp = json.loads(json.dumps(temp.val()))
			#set data into user
			db.child('userActivity').child(userId).set(temp)
			for key,val in _args.items():
				db.child('userActivity').child(userId).child(_operation).child(_type).child(_id).update({key:val})
			db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).update({'createdDate':int(time.time())})
			#delete previous key			
			db.child('userActivity').child(replacee).remove()
			return userId

		else:
			return 'not a valid token'
