import urllib

#this module is to be imported in any api that requires parameter decoding
def decodeArgs(_args):
	#base64 decode of entire string
	_args = _args.decode('base64')
	#splitting base64 decoded string
	count = _args.count('&')
	count += 1
	index = 0
	split_list = []
	list_key = []	
	temp_list_val = []
	final_list = []
	while index < count:
		split_list.append(_args.split('&')[index])
		#splitting parameters with key and value in different lists
		list_key.append(split_list[index].split('=')[0])
		temp_list_val.append(split_list[index].split('=')[1])
		#url decoding the separated parameters
		final_list.append(str(urllib.unquote(temp_list_val[index]).decode('utf8')))
		index += 1
	i=0
	result = {}
	#creating a dictionary with name of parameter and its value as key-value pair in dictionary
	while i<len(list_key):
		result.update({list_key[i]:final_list[i]})
		i+=1
	#returning result
	return result
