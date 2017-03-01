from restful import Resource
from flask_restful import reqparse
import requests
from decoder import decodeArgs

class sendotpclass(Resource):
    def post(self):
        try:
			parser = reqparse.RequestParser()
			parser.add_argument('mobile', required=True, type=int, help='user phone number')
			parser.add_argument('otp', required=True, type=int,  help='one time password')
			args = parser.parse_args()
			return args
			args = decodeArgs(args)
			_mobile = args['mobile']
			_otp = args['otp']
			url = 'http://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=rNfGwBJ7xcV&MobileNo='+_mobile+'&SenderID=ROOFPK&Message=Greetings, '+_otp+' is your verification code for Roofpik.&ServiceName=TEMPLATE_BASED'
			response = requests.post(url)
			status = response.status_code
			content = response.content
			return {
                    'status' : status,
                    'msg': 'OTP successfully sent to '+str(_mobile)
                }
        except Exception as e:
			return str(e)

