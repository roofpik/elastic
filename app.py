from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from search import *
from residential import *
from residential_review_1 import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')
api.add_resource(residentialclass,'/residential')
api.add_resource(residentialreview1class,'/r-review-1')

if __name__ == "__main__":
	app.debug = True
	app.run()
