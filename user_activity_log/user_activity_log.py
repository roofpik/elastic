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

		config = {
    			'apiKey': "AIzaSyAapASzaLGFxHgbMpu9Cibfn97MSEheCcU",
    			'authDomain': "roofpik-f8f55.firebaseapp.com",
    			'databaseURL': "https://roofpik-f8f55.firebaseio.com",
    			'storageBucket': "roofpik-f8f55.appspot.com",
    			'messagingSenderId': "303104341936"
  		}

		firebase = pyrebase.initialize_app(config)
		db = firebase.database()

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if 'token' in _args.keys():
			_token = _args['token']
			del _args['token']
		else:
			return 'token not provided'
		if _token=='custom':
			db.child('userActivity').remove()
			return 'parent node userActivity deleted'

		if 'type' in _args.keys():
			_type = _args['type']
			del _args['type']

		else:
			return 'no type(loc, project, review...) specified'

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
		return _args
		if _token == 'random':
			stamp = int(time.time())
			counter = 0
			for key,val in _args.items():
				if counter==0:
					db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).set({key:val})
					counter += 1
				else:
					db.child('userActivity').child(stamp).child(_operation).child(_type).child(_id).update({key:val})
			return stamp

		else:
			userId = _token.split('$')[0]
			replacee = _token.split('$')[1]
			temp = db.child('userActivity').child(replacee).get()
			db.child('userActivity').child(userId).set(temp)
			db.child('userActivity').child(replacee).remove()
			return userId
