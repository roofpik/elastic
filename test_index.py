import json
from elasticsearch import Elasticsearch
import requests

es = Elasticsearch(['https://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com'])

print es
print 'step 1 complete'

print 'step 2 complete'
print es.get(index='test_index', doc_type='data', id=100)
es.index(index='test_index', doc_type='data', id=102, body={"name":"test entry"})
print 'step 3 complete'
