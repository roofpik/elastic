import urllib

def decodeArgs(_args):
	_args = _args.decode('base64')
	count = _args.count('&')
	count += 1
	index = 0
	split_list = []
	list_key = []	
	temp_list_val = []
	final_list = []
	while index < count:
		split_list.append(_args.split('&')[index])
		list_key.append(split_list[index].split('=')[0])
		temp_list_val.append(split_list[index].split('=')[1])
		final_list.append(str(urllib.unquote(temp_list_val[index]).decode('utf8')))
		index += 1
	i=0
	result = {}
	while i<len(list_key):
		result.update({list_key[i]:final_list[i]})		
		i+=1
	return result
