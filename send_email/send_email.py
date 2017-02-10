from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from decoder import decodeArgs
from email_body import _body

#sending mail via sendgrid
def sendMail(email, name):
	sg = sendgrid.SendGridAPIClient(apikey='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')
	from_email = Email("noreply@roofpik.com")
	#do not send any empty field
	subject = "subject"
	to_email = Email(email)
	content = Content("text/html", "<html>\r\n\r\n<head>\r\n <title><\/title>\r\n<\/head>\r\n\r\n<body>\r\n <table cellpadding=\"0\" cellspacing=\"0\" style=\"border:solid 1px #eee; letter-spacing: 1px; font-family: arial; background-color: #fafafa; font-size: 14px; color: #444; width:600px; margin:0 auto;\">\r\n <tr>\r\n <td style=\"padding: 10px;\">\r\n <a href=\"http:\/\/www.roofpik.com\/\" target=\"blank\"><img src=\"http:\/\/www.roofpik.com\/images\/general\/logo.png\" width=\"99\" height=\"27\"><\/a>\r\n <\/td>\r\n <td align=\"right\" style=\"padding: 10px;\">\r\n <div style=\"font-size: 14px; font-weight: 700; line-height: 42px\">\r\n <a href=\"http:\/\/www.roofpik.com\/\" target=\"blank\" style=\"padding:5px;color: #666; text-decoration: none;\">Home<\/a>|\r\n <a href=\"http:\/\/www.roofpik.com\/#\/blogs\/gurgaon\/-KYJONgh0P98xoyPPYm9\/1\" target=\"blank\" style=\"padding:0 5px; color: #666; text-decoration: none;\">Blogs<\/a>|\r\n <a href=\"http:\/\/www.roofpik.com\/#\/cover-stories\/gurgaon\/-KYJONgh0P98xoyPPYm9\/1\" target=\"blank\" style=\"padding:5px; color: #666; text-decoration: none;\">Cover Stories<\/a>\r\n <\/div>\r\n <\/td>\r\n <\/tr>\r\n <tr>\r\n <td colspan=\"2\" align=\"center\" style=\"padding:20px; font-size: 21px; color:#fff; background-color: #4fc3f7\">\r\n <b>We\u2019re glad to see you here! <\/b><\/td>\r\n <\/tr>\r\n <tr>\r\n <td colspan=\"2\" style=\"font-size: 15px; background-color: #fff; padding: 20px; line-height: 24px; color:#666\">\r\n <div><b>Hi<\/b> "+name+"\r\n <br>\r\n <br>\r\n <\/div>\r\n <b>Welcome<\/b> to the the first of its fing real estate review community, we have thousands of reviews by verified end consumers.\r\n <br>\r\n <br> With a huge number of reviews, Roofpik can help you select the your next home. Compare and select from 1000\'s of properties in 100\'s of location to find a place that is best from your family or business.\r\n <br>\r\n <br> Our unique property ranking system helps make your choice simpler and easier.\r\n <div style=\"padding: 20px; text-align: center\"><a href=\"http:\/\/www.roofpik.com\" target=\"blank\" style=\"padding:10px 20px; color: #fff; text-decoration: none; background-color: #EF5350\">View Roofpik Website<\/a>\r\n <br>\r\n <\/div>\r\n <\/td>\r\n <\/tr>\r\n <tr>\r\n <td colspan=\"2\" style=\"font-size: 9px; line-height: 15px; color: #fff; background-color:#4fc3f7; padding: 10px\">\r\n <div style=\"font-size: 10px; color: #fff; line-height: 30px\">\r\n <a href=\"http:\/\/www.roofpik.com\/\" target=\"blank\" style=\"padding:5px;color: #fff; text-decoration: none;\">Home<\/a>|\r\n <a href=\"http:\/\/www.roofpik.com\/#\/about-us\" target=\"blank\" style=\"padding:5px; color: #fff; text-decoration: none;\">About<\/a>|\r\n <a href=\"http:\/\/www.roofpik.com\/#\/contact-us\" target=\"blank\" style=\"padding:5px; color: #fff; text-decoration: none;\">Contact Us<\/a>\r\n <\/div>\r\n <br> Please do not reply directly to this e-mail. This e-mail was sent from a notification-only address that cannot accept incoming e-mail. If you have questions or need assistance, ask us <a style=\"color: #236384; text-decoration: none;\" href=\"mailto:contact@roofpik.com\">here<\/a>\r\n <br>\r\n <br> 250, Vipul Trade Center, Sector 48, Gurgaon Haryana\r\n <br>\r\n <\/td>\r\n <\/tr>\r\n <\/table>\r\n<\/body>\r\n\r\n<\/html>")
	mail = Mail(from_email, subject, to_email, content)
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
