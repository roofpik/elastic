import json
from elasticsearch import Elasticsearch
import requests

es = Elasticsearch([{'host':'http://search-roof-pnslfpvdk2valk5lfzveecww54.ap-south-1.es.amazonaws.com/'}])

es.index(index='test_index', doc_type='data', id=100, body={"name":"test entry"})

