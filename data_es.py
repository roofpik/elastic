import json
from elasticsearch import Elasticsearch
import requests

es = Elasticsearch([{'host':'localhost', 'port':9200}])

r = requests.request('get', 'https://roofpik-948d0.firebaseio.com/projects/-KYJONgh0P98xoyPPYm9/residential/.json')
data1 = r.json()

for x in data1:
	
	data = data1[x]
	d = {}
	details = {}
	amenities = {} 
	d['bhk'] = {}
	d['propertyType'] = {}
	d['location'] = {}
	price = []
	area = []
	l1 = []
	l2 = []
	l3 = []
	l4 = []
	l5 = []
	l6 = []
	min_rent1 = []
	min_rent2 = []
	min_rent3 = []
	min_rent4 = []
	min_rent5 = []
	min_rent6 = []
	max_rent1 = []
	max_rent2 = []
	max_rent3 = []
	max_rent4 = []
	max_rent5 = []
	max_rent6 = []

	try:
		for j in data:
#for project id
	#j has ids of projects
			for k in data['configurations']:
		#k has all objects that were inside config

			#adding bhks in the format bhk : {}
				temp = {}
				temp[k] = data['configurations'][k]['bhk']
				a = temp[k]
				temp.pop(k)
				temp[a] = {}

			#for min price
				if(data['configurations'][k]['pricing']['rent']['min'] == 'NA'):
					temp[a].update({'min_price': 0})
				else:
					if(a=='1'):
						min_rent1.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent1))})
					elif(a=='2'):
						min_rent2.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent2))})
					if(a=='3'):
						min_rent3.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent3))})
					if(a=='4'):
						min_rent4.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent4))})
					if(a=='5'):
						min_rent5.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent5))})
					if(a=='6'):
						min_rent6.append(data['configurations'][k]['pricing']['rent']['min'])
						temp[a].update({'min_price': int(min(min_rent6))})
				price.append(json.dumps(data['configurations'][k]['pricing']['rent']['min']))

			#for max price
				if(data['configurations'][k]['pricing']['rent']['max'] == 'NA'):
					temp[a].update({'max_price': 15000})
				else:
					if(a=='1'):
						max_rent1.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent1))})
					elif(a=='2'):
						max_rent2.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent2))})
					elif(a=='3'):
						max_rent3.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent3))})
					elif(a=='4'):
						max_rent4.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent4))})
					elif(a=='5'):
						max_rent5.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent5))})
					elif(a=='6'):
						max_rent6.append(data['configurations'][k]['pricing']['rent']['max'])
						temp[a].update({'max_price': int(max(max_rent6))})
				price.append(json.dumps(data['configurations'][k]['pricing']['rent']['max']))
				
				#area
				if(data['configurations'][k]['superBuiltArea'] == 'NA'):
					temp[a].update({'min_area': 0})
					temp[a].update({'max_area': 0})
				else:
					if(a=='1'):
						l1.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l1))})
						temp[a].update({'max_area': int(max(l1))})
					elif(a=='2'):
						l2.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l2))})
						temp[a].update({'max_area': int(max(l2))})
					elif(a=='3'):
						l3.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l3))})
						temp[a].update({'max_area': int(max(l3))})
					elif(a=='4'):
						l4.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l4))})
						temp[a].update({'max_area': int(max(l4))})
					elif(a=='5'):
						l5.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l5))})
						temp[a].update({'max_area': int(max(l5))})
					elif(a=='6'):
						l6.append(int(data['configurations'][k]['superBuiltArea']))
						temp[a].update({'min_area': int(min(l6))})
						temp[a].update({'max_area': int(max(l6))})
				if(data['configurations'][k]['superBuiltArea'] == '"NA"' or data['configurations'][k]['superBuiltArea'] == ''):
					area.append(0)
				else:
					area.append(json.dumps(int(data['configurations'][k]['superBuiltArea'])))
				d['bhk'].update(temp)
				
				#adding propertyType in the format propertyType : true
				propertyType = {}
				propertyType[k] = data['configurations'][k]['unit']
				a = propertyType[k]
				propertyType.pop(k)
				propertyType[a] = True
				d['propertyType'].update(propertyType)

				#pushing in location
				location = {}
				location[k] = data['projectDetails']['address']['locations']['primary']['locationId']
				a = location[k]
				location.pop(k)
				location[a] = True
				d['location'].update(location)
				location[k] = data['projectDetails']['address']['localities']['primary']['localityId']
				a = location[k]
				location.pop(k)
				location[a] = True
				d['location'].update(location)

				
				try:
					for x in data['projectDetails']['address']['locations']['other']:
						location = {}
						location[x] = data['projectDetails']['address']['locations']['other'][x]['locationId']
						a = location[x]
						location.pop(x)
						location[a] = True
						d['location'].update(location)
				except:
					pass 

				try:
					for x in data['projectDetails']['address']['localities']['other']:
						location = {}
						location[x] = data['projectDetails']['address']['localities']['other'][x]['localityId']
						a = location[x]
						location.pop(x)
						location[a] = True
						d['location'].update(location)
				except:
					pass

			#pushing in amenities - basic and convenience
			#amenities.update({'basic': json.dumps(data['amenities']['basic'])})
			amenities['basic'] = data['amenities']['basic']
			amenities['convenience'] = data['amenities']['convenience']
			#amenities.update({'convenience': json.dumps(data['amenities']['basic'])})
			#json.loads(json.dumps(amenities['basic']))

			#style from segment in id
			d['style'] = data['segment']
			#details from projectName and projectDetails in id
			details['name'] = data['projectName']
			details['builder'] = data['projectDetails']['builderId']

			#loop ends
			#adding rent
			d['rent'] = {}
			if(min(price) == '"NA"'):
				d['rent']['min'] = 0
			else:		
				d['rent']['min'] = int(min(price))
			if(max(price) == '"NA"'):
				d['rent']['max'] = 15000
			else:
				d['rent']['max'] = int(max(price))

			#adding area
			d['area'] = {}
			d['area']['min'] = int(min(area))
			d['area']['max'] = int(max(area))

			d['amenities'] = amenities
			d['details'] = details

	#print json.dumps(d)

		es.index(index='ios1', doc_type='data', id=data['projectId'], body=d)
			
	except:
		print str(Exception)
