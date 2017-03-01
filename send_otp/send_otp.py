from restful import Resource
from flask_restful import reqparse
import requests
from decoder import decodeArgs
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Substitution

def sendMail(email, _otp):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	#do not send any empty field	
	subject = "Greetings from Roofpik!"
	to_email = Email(email)
	content = Content("text/html", "Your OTP is "+_otp)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	return 'mail sent'

class sendotpclass(Resource):
    def get(self):
        try:
        	return 'ok'
			parser = reqparse.RequestParser()
			#requesting argument
			parser.add_argument('args', type=str)
			args = parser.parse_args()
			_args = args['args']
			#decoding arguments
			_args = decodeArgs(_args)
			_mobile = _args['mobile']
			_otp = _args['otp']
			#_email = _args['email']
			#url to hit external api
			url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=rNfGwBJ7xcV&MobileNo='+_mobile+'&SenderID=ROOFPK&Message=Greetings! '+_otp+' is your verification code for Roofpik.&ServiceName=TEMPLATE_BASED'
			response = requests.post(url)
			status = response.status_code
			content = response.content
			#send mail
			#mailStatus = sendMail(_email, _otp)
			#send response
			return {
                    'status' : status,
                    'msg': 'OTP successfully sent to '+_mobile
             #       'mail': mailStatus
                }
        except Exception as e:
			return str(e)

