from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from search import *
from anu import *
from api_test import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')
api.add_resource(anuapi,'/anu-my-api')
api.add_resource(testclass,'/call-me-here')

if __name__ == "__main__":
	app.debug = True
	app.run()
