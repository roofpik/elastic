from flask import request
from restful import Resource
from flask_restful import reqparse
from ftplib import FTP
from werkzeug.utils import secure_filename
import os
import uuid

class uploadFile(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, help='name of file')
		parser.add_argument('path', type=str, help='path to save file')
		args = parser.parse_args()
		uFile = request.files['file']

        _path = args['path']
        if not _path:
        	_path = ''

        _name = args['name']
        if not _name:
        	_name = uFile.filename
		
		os.chdir('/var/www/api/uploaded_files/'+_path)
		r = uFile.save(secure_filename(_name))
		return r