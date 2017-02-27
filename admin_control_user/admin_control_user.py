from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from decoder import decodeArgs
import pyrebase
import time

#create admin or user according to conditions
def create(auth, db, userData, _type):
	if userData['email'] and userData['password'] and userData:
		if '@roofpik.com' in userData['email'] and _type=='admins':
			res = auth.create_user_with_email_and_password(userData['email'], userData['password'])
			userId = res['localId']
			db.child(_type).child(userId).set(data)
			db.child(_type).child(userId).update({"userId": userId})
			db.child(_type).child(userId).update({"createdDate": int(time.time())})
			sendVerificationEmail(auth, userData)
			return userId
		elif '@roofpik.com' in userData['email'] and _type=='users':
			return '@roofpik.com can be held by admins only'
		elif _type=='users':
			res = auth.create_user_with_email_and_password(userData['email'], userData['password'])
			userId = res['localId']
			db.child(_type).child(userId).set(data)
			db.child(_type).child(userId).update({"userId": userId})
			db.child(_type).child(userId).update({"createdDate": int(time.time())})
			sendVerificationEmail(auth, userData)
			return userId			
		else:
			return 'not a valid email'
	else:
		return 'userdata must be provided and should contain email and password'

#send verification mail to given mail by getting a fresh token
def sendVerificationEmail(auth, userData):
	user = auth.sign_in_with_email_and_password(userData['email'], userData['password'])
	user = auth.refresh(user['refreshToken'])
	token = user['idToken']
	res = auth.send_email_verification(token)

class admincontrolclass(Resource):
	def get(self):

		config = {
    			'apiKey': "AIzaSyAapASzaLGFxHgbMpu9Cibfn97MSEheCcU",
    			'authDomain': "roofpik-f8f55.firebaseapp.com",
    			'databaseURL': "https://roofpik-f8f55.firebaseio.com",
    			'storageBucket': "roofpik-f8f55.appspot.com",
    			'messagingSenderId': "303104341936"
  		}

		firebase = pyrebase.initialize_app(config)
		auth = firebase.auth()
		db = firebase.database()

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		_args = decodeArgs(_args)

		if 'operation' in _args.keys():
			operation = _args['operation']
		else:
			return 'provide an operation'

		if 'userData' in _args.keys():
			userEmail = _args['userEmail']
		else:
			userEmail = ''

		if operation=='createAdmin':
			return create(auth, db, userData, "admins")

		elif operation=='createUser':
			return create(auth, db, userData, "users")

		elif operation=='sendPasswordReset':
			if userData['email']:
				auth.send_password_reset_email("email")
			else:
				return 'send user email in user data'
				
		else:
			return 'not a valid operation'
