import json
from elasticsearch import Elasticsearch
import requests

es = Elasticsearch([{'host':'localhost', 'port':9200}])

r = requests.request('get', 'https://roofpik-948d0.firebaseio.com/reviews/-KYJONgh0P98xoyPPYm9/residential.json')

data = r.json()

d = {}

for pid in data:
	for iid in data[pid]:
		d = data[pid][iid]
		d.update({'pid':pid})
		es.index(index="res_reviews", doc_type="reviews", id=iid, body=d)

