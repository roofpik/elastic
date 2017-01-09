from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from search import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')

if __name__ == "__main__":
	app.debug = True
	app.run()
