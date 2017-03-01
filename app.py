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
from listing import *
from map_api import *
from universal_search_api import *
from admin_view import *
from admin_list import *
from admin_delete import *
from admin_update import *
from admin_post import *
from admin_control_user import *
from user_activity_log import *
from get_nearby import *
from get_relatedservices import *
from send_otp import *

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
api.add_resource(locationdistanceclass,'/GetLocations_1.0')
api.add_resource(listingclass,'/GetListing_1.0')
api.add_resource(mapapiclass,'/GetMapData_1.0')
api.add_resource(universalsearchclass,'/GetByName_1.0')
api.add_resource(adminviewclass,'/AdminViewData_1.0')
api.add_resource(adminlistclass,'/AdminListData_1.0')
api.add_resource(admindeleteclass,'/AdminDeleteData_1.0')
api.add_resource(adminupdateclass,'/AdminUpdateData_1.0')
api.add_resource(adminpostclass,'/AdminPostData_1.0')
api.add_resource(admincontrolclass,'/AdminControl_1.0')
api.add_resource(useractivityclass,'/LogActivity_1.0')
api.add_resource(nearbyclass,'/GetNearby_1.0')
api.add_resource(relatedservicesclass,'/GetRelatedServices_1.0')
api.add_resource(sendotpclass,'/SendOTP_1.0')

if __name__ == "__main__":
	app.debug = True
	app.run()
