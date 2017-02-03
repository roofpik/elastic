from restful import Resource
import requests
import json
from flask_restful import reqparse
from flask import *
from elasticsearch import Elasticsearch

i = 0
j = 0
k = 0
true = True

class testclass(Resource):
        def get(self):
                try:
                    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

                    parser = reqparse.RequestParser()
                    parser.add_argument('style', type=str)
                    args = parser.parse_args()
                    _style = args['style']
                    if not _style:
                            _style = ""

                    parser.add_argument('details_name', type=str)
                    args = parser.parse_args()
                    _details_name = args['details_name']
                    if not _details_name:
                            _details_name = ""

                    parser.add_argument('details_builder', type=str)
                    args = parser.parse_args()
                    _details_builder = args['details_builder']
                    if not _details_builder:
                            _details_builder = ""

                    parser.add_argument('area_min_range', type=str)
                    args = parser.parse_args()
                    _area_min_range = args['area_min_range']
                    if not _area_min_range:
                            _area_min_range = ""

                    parser.add_argument('area_max_range', type=str)
                    args = parser.parse_args()
                    _area_max_range = args['area_max_range']
                    if not _area_max_range:
                            _area_max_range = ""

                    parser.add_argument('price_min_range', type=str)
                    args = parser.parse_args()
                    _price_min_range = args['price_min_range']
                    if not _price_min_range:
                            _price_min_range = ""

                    parser.add_argument('price_max_range', type=str)
                    args = parser.parse_args()
                    _price_max_range = args['price_max_range']
                    if not _price_max_range:
                            _price_max_range = ""

                    parser.add_argument('sort_field', type=str)
                    args = parser.parse_args()
                    _sort_field = args['sort_field']
                    if not _sort_field:
                            _sort_field = ""

                    parser.add_argument('locationId', type=str)
                    args = parser.parse_args()
                    _locationId = args['locationId']
                    if not _locationId:
                            _locationId = ""

                    parser.add_argument('propertyType', type=str)
                    args = parser.parse_args()
                    _propertyType = args['propertyType']
                    if not _propertyType:
                            _propertyType = ""

                    parser.add_argument('amenity', type=str)
                    args = parser.parse_args()
                    _amenity = args['amenity']
                    if not _amenity:
                            _amenity = ""      

                    parser.add_argument('page_start', type=int)
                    args = parser.parse_args()
                    _page_start = args['page_start']
                    if not _page_start:
                            _page_start = 0    

                    parser.add_argument('page_size', type=int)
                    args = parser.parse_args()
                    _page_size = args['page_size']
                    if not _page_size:
                            _page_size = 10                  

                    query_builder = {}
                    query_builder['query'] = {}
                    query_builder['query']['bool'] = {}
                    query_builder['query']['bool']['must'] = []
                    query_builder['query']['bool']['should'] = []
                    query_builder['sort'] = []
                    
                    def build_query_must(m, n):
                            global i
                            query_builder['query']['bool']['must'].append({})
                            query_builder['query']['bool']['must'][i]['match'] = {}
                            query_builder['query']['bool']['must'][i]['match'][m] = n
                            i += 1

                    def build_query_should(m, n):
                            global j
                            query_builder['query']['bool']['should'].append({})
                            query_builder['query']['bool']['should'][j]['match'] = {}
                            query_builder['query']['bool']['should'][j]['match'][m] = n
                            j += 1

                    def build_query_must_range(m, lower, upper):
                            global i
                            query_builder['query']['bool']['must'].append({})
                            query_builder['query']['bool']['must'][i]['range'] = {}
                            query_builder['query']['bool']['must'][i]['range'][m] = {}
                            query_builder['query']['bool']['must'][i]['range'][m]['from'] = lower
                            query_builder['query']['bool']['must'][i]['range'][m]['to'] = upper
                            i += 1

                    def build_query_should_range(m, lower, upper):
                            global j
                            query_builder['query']['bool']['should'].append({})
                            query_builder['query']['bool']['should'][j]['range'] = {}
                            query_builder['query']['bool']['should'][j]['range'][m] = {}
                            query_builder['query']['bool']['should'][j]['range'][m]['from'] = lower
                            query_builder['query']['bool']['should'][j]['range'][m]['to'] = upper
                            j += 1

                    def build_query_sort(m, asc_or_dsc):
                            global k
                            query_builder['sort'].append({})
                            query_builder['sort'][k][m] = {}
                            query_builder['sort'][k][m]['order'] = asc_or_dsc
                            k+=1

                    if(_style):
                            build_query_must('style', _style)

                    if(_details_name):
                            build_query_must("details.name", _details_name)

                    if(_details_builder):
                            build_query_must("details.builder", _details_builder)

                    if(_area_min_range):
                            a = _area_min_range.split('$')[0]
                            b = _area_min_range.split('$')[1]
                            build_query_should_range("area.min", a, b)

                    if(_price_min_range):
                            a = _price_min_range.split('$')[0]
                            b = _price_min_range.split('$')[1]
                            build_query_should_range("price.min", a, b)

                    if(_area_max_range):
                            a = _area_max_range.split('$')[0]
                            b = _area_max_range.split('$')[1]
                            build_query_should_range("area.max", a, b)

                    if(_price_max_range):
                            a = _price_max_range.split('$')[0]
                            b = _price_max_range.split('$')[1]
                            build_query_should_range("price.max", a, b)

                    if(_sort_field):
                            a = _sort_field.split('$')[0]
                            b = _sort_field.split('$')[1]
                            build_query_sort(a, b)

                    if(_locationId):
                            count = _locationId.count('$')
                            if(count==0):
                                    build_query_should("location."+_locationId, true)
                            else:
                                    count += 1
                                    l = []
                                    i = 0
                                    while i!=count:
                                            l.append(_locationId.split('$')[i])
                                            build_query_should("location."+l[i], true)
                                            i += 1

                    if(_propertyType):
                            count = _propertyType.count('$')
                            if(count==0):
                                    build_query_should("propertyType."+_propertyType, true)
                            else:
                                    count += 1
                                    l = []
                                    i = 0
                                    while i!=count:
                                            l.append(_propertyType.split('$')[i])
                                            build_query_should("propertyType."+l[i], true)
                                            i += 1

                    if(_amenity):
                            count = _amenity.count('$')
                            if(count==0):
                                    build_query_should("amenity."+_amenity, true)
                            else:
                                    count += 1
                                    l = []
                                    i = 0
                                    while i!=count:
                                            l.append(_amenity.split('$')[i])
                                            build_query_should("amenity."+l[i], true)
                                            i += 1

                    res = es.search(index='live_index_1', doc_type='data', body=query_builder, from_=_page_start, size=_page_size)
                    i = 0
                    x = {}
                    while i<_page_size:
                        d = {}
                        d.update({'id': res['hits']['hits'][i]['_source']['projectId']})
                        # d.update({'name': res['hits']['hits'][i]['_source']['details.name']})
                        # d.update({'adddress': res['hits']['hits'][i]['_source']['address']})
                        # d.update({'cover': res['hits']['hits'][i]['_source']['cover_pic']})
                        return d
                        x.update(d)
                        i += 1
                    return x    

                except:
                    pass