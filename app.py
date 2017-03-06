from flask import Flask
from flask_restful import Api
from flask.ext.cors import CORS

from residential import *
from cghs import *
from review_summary import *
from review_details import *
from project_reviews import *
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
from universal_search_api_home import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(residentialclass,'/GetResidential_1.0')
api.add_resource(cghsclass,'/GetCghs_1.0')
api.add_resource(reviewsummaryclass,'/GetReviewSummary_1.0')
api.add_resource(reviewdetailsclass,'/GetReviewDetails_1.0')
api.add_resource(projectreviewsclass,'/GetProjectReviews_1.0')
api.add_resource(sendemailclass,'/SendMail_1.0')
api.add_resource(localityclass,'/GetLocality_1.0')
api.add_resource(locationdistanceclass,'/GetLocations_1.0')
api.add_resource(listingclass,'/GetListing_1.0')
api.add_resource(mapapiclass,'/GetMapData_1.0')
api.add_resource(universalsearchclass,'/GetByName_1.0')
api.add_resource(universalhomesearchclass,'/GetByNameHome_1.0')
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
