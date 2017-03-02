from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Substitution
from decoder import decodeArgs

def sendMail(email, name, conf, template_id, *extra):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	#do not send any empty field
	if conf==1:	
		subject = "Greetings from Roofpik!"
	else:
		subject = "Review submitted successfully!"
	to_email = Email(email)
	content = Content("text/html", "hi")
	mail = Mail(from_email, subject, to_email, content)
	#substitute name in the template
	mail.personalizations[0].add_substitution(Substitution("-name-", name))
	#for extra substitutions - if any
	if extra:
		extra = list(extra)
	#add extra substitutions here
		if extra[1]==2:
			mail.personalizations[0].add_substitution(Substitution("-coupon-", extra[0]))
		else:
			mail.personalizations[0].add_substitution(Substitution("-url-", extra[0]))
	#send template_id
	mail.set_template_id(template_id)
	response = sg.client.mail.send.post(request_body=mail.get())
	return 'mail sent'

#sending mail via sendgrid
def sendWelcomeMail(email, name, _conf):
	return sendMail(email, name, _conf, "a029e13d-b169-4bc5-891c-356b80d23a6f")

def sendSuccessWOCoupon(email, name, _conf, url):
	return sendMail(email, name, _conf, "a790120a-899d-4a79-b3bb-7f07679a235f", url, 1)

def sendVerifiedWOCoupon(email, name, _conf):
	return sendMail(email, name, _conf, "331b64de-838d-4405-b56a-c6cf6f0b42dc")

def sendSuccessWCoupon(email, name, _conf, coupon):
	return sendMail(email, name, _conf, "9eb5e8e2-e91b-4a3d-bbb4-d7f03afee40e", coupon, 2)

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
			return 'email or name not provided correctly'

		if 'conf' in all_args.keys():
			_conf = all_args['conf']
		else:
			_conf = '1'

		if 'couponFlag' in all_args.keys():
			_couponFlag = bool(all_args['couponFlag'])
		else:
			_couponFlag = False

		if 'verifiedFlag' in all_args.keys():
			_verifiedFlag = bool(all_args['verifiedFlag'])
		else:
			_verifiedFlag = False

		_conf=int(_conf)

		#check _conf to jump to method
		if _conf==1:
			return sendWelcomeMail(email, name, _conf)

		elif _conf==2:
			try:
				if _verifiedFlag and not _couponFlag:
					return sendVerifiedWOCoupon(email, name, _conf) 
				elif _verifiedFlag and _couponFlag:
					coupon = all_args['coupon']
					return sendSuccessWCoupon(email, name, _conf, coupon)
				else:
					url = 'test.roofpik.com/#/profile'
					return sendSuccessWOCoupon(email, name, _conf, url)
			except:
				return 'some data is inconsistent'

		else:
			return 'conf not identified'