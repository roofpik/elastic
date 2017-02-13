from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Substitution
from decoder import decodeArgs

#sending mail via sendgrid
def sendMail(email, name):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	#do not send any empty field
	subject = "Welcome!"
	to_email = Email(email)
	content = Content("text/html", "hi")
	mail = Mail(from_email, subject, to_email, content)
	mail.personalizations[0].add_substitution(Substitution("-name-", name))
	mail.set_template_id("a029e13d-b169-4bc5-891c-356b80d23a6f")
	response = sg.client.mail.send.post(request_body=mail.get())

class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']
		
		#decoding coded args
		all_args = decodeArgs(_args)

		sendMail(all_args[0], all_args[1])
