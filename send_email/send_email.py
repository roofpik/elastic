from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import urllib
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

#parsing the recorded argument
def decodeArgs(_args):
	_args = _args.decode('base64')
	count = _args.count('&')
	count += 1
	index = 0
	split_list = []
	temp_list = []
	final_list = []
	while index < count:
		split_list.append(_args.split('&')[index])
		temp_list.append(split_list[index].split('=')[1])
		final_list.append(str(urllib.unquote(temp_list[index]).decode('utf8')))
		index += 1
	return final_list

#sending mail via sendgrid
def sendMail(email):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	subject = "Hello World from the SendGrid Python Library on Heroku!"
	to_email = Email(email)
	content = Content("text/plain", "Hi")
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']

		all_args = decodeArgs(_args)

		sendMail(all_args[0])
