from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid

class uploadFile(Resource):
	def post(self):
		uFile = request.files['file']
		os.chdir('/var/www/api/uploaded_files')
		r = uFile.save(secure_filename(uFile.filename))
		return r