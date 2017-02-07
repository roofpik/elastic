from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from search import *
from anu import *
from api_test_residential import *
from api_test_cghs import *
from api_test_2 import *
from api_reviews_residential import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')
api.add_resource(anuapi,'/anu-my-api')
api.add_resource(residentialclass,'/residential')
api.add_resource(cghsclass,'/cghs')
api.add_resource(testclass2,'/test-api-2')
api.add_resource(resReviewclass,'/residential-reviews')

if __name__ == "__main__":
	app.debug = True
	app.run()
