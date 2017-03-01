from restful import Resource
from flask_restful import reqparse
import requests
from decoder import decodeArgs

class sendotpclass(Resource):
    def get(self):
        try:
			parser = reqparse.RequestParser()
			parser.add_argument('args', type=str)
			args = parser.parse_args()
			_args = args['args']
		
			_args = decodeArgs(_args)

			_mobile = _args['mobile']
			_otp = _args['otp']
			url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=rNfGwBJ7xcV&MobileNo=8527506109&SenderID=ROOFPK&Message=Greetings, 4567 is your verification code for Roofpik.&ServiceName=TEMPLATE_BASED'
			response = requests.post(url)
			status = response.status_code
			content = response.content
			return {
                    'status' : status,
                    'msg': 'OTP successfully sent to '+_mobile
                }
        except Exception as e:
			return str(e)

