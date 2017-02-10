def decodeArgs(_args):
	_args = _args.decode('base64')
	count = _args.count('&')
	count += 1
	index = 0
	split_list = []
	temp_list = []
	final_list = []
	while index < count:
		split_list.append(_args.split('&')[index])
		temp_list.append(split_list[index].split('=')[1])
		final_list.append(str(urllib.unquote(temp_list[index]).decode('utf8')))
		index += 1
	return final_list
