from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from search import *
from residential import *
from cghs import *
from residential_review_1 import *
from residential_review_2 import *
from residential_review_3 import *
from send_email import *
from locality_search import *
from distance_loc import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(test,'/test')
api.add_resource(residentialclass,'/GetResidential_1.0')
api.add_resource(cghsclass,'/GetCghs_1.0')
api.add_resource(residentialreview1class,'/GetReviewSummary_1.0')
api.add_resource(residentialreview2class,'/GetReviewDetails_1.0')
api.add_resource(residentialreview3class,'/GetProjectReviews_1.0')
api.add_resource(sendemailclass,'/SendMail_1.0')
api.add_resource(localityclass,'/GetLocality_1.0')
api.add_resource(locationdistanceclass,'/SortDistance_1.0')

if __name__ == "__main__":
	app.debug = True
	app.run()
