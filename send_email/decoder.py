import urllib

def decodeArgs(_args):
	_args = _args.decode('base64')
	count = _args.count('&') + 1
	index = 0
	split_list = []
	result = {}
	while index < count:
		split_list.append(_args.split('&')[index])
		result.update({str(urllib.unquote(split_list[index].split('=')[0]).decode('utf8')):split_list[index].split('=')[1]})
		index += 1
	return result