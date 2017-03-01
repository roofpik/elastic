from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Substitution
from decoder import decodeArgs

def sendMail(email, name, template_id):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	#do not send any empty field	
	subject = "Welcome!"
	to_email = Email(email)
	content = Content("text/html", "hi")
	mail = Mail(from_email, subject, to_email, content)
	#substitute name in the template
	mail.personalizations[0].add_substitution(Substitution("-name-", name))
	mail.set_template_id(template_id)		
	response = sg.client.mail.send.post(request_body=mail.get())
	return 'mail sent'

#sending welcome mail via sendgrid
def sendWelcomeMail(email, name):
	return sendMail(email, name, "a029e13d-b169-4bc5-891c-356b80d23a6f")

def sendVerifyNumberMail(email, name):
	return sendMail(email, name, "template_id with link for OTP")

def sendSuccessWOCoupon(email, name):
	return sendMail(email, name, "template_id without coupon with verified number")

def sendSuccessWCoupon(email, name):
	return sendMail(email, name, "template_id with coupon and number verified")

#main class
class sendemailclass(Resource):
	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('args', type=str)
		args = parser.parse_args()
		_args = args['args']
		
		#decoding coded args
		all_args = decodeArgs(_args)

		try:
			email = all_args['email']
			name = all_args['name']
		except:
			return 'params not provided correctly'

		if 'conf' in all_args.keys():
			_conf = all_args['conf']
		else:
			_conf = '1'

		if 'couponFlag' in all_args.keys():
			_couponFlag = bool(all_args['couponFlag'])
		else:
			_couponFlag = False

		if 'numberVerified' in all_args.keys():
			_numberVerified = bool(all_args['numberVerified'])
		else:
			_numberVerified = False

		_conf=int(_conf)

		#check _conf to jump to method
		if _conf==1:
			return sendWelcomeMail(email, name)

		elif _conf==2:
			if not _couponFlag and not _numberVerified:
				return sendVerifyNumberMail(email, name)
			if not _couponFlag and _numberVerified:
				return sendSuccessWOCoupon(email, name)
			if _couponFlag and not _numberVerified:
				return sendVerifyNumberMail(email, name)
			if _couponFlag and _numberVerified:
				return sendSuccessWCoupon(email, name)

		else:
			return 'conf not identified'
