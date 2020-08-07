import base64
import hashlib
import secrets

_trans_5C = bytes((x ^ 0x5C) for x in range(256))
_trans_36 = bytes((x ^ 0x36) for x in range(256))


def key_64(char_len):
	nbytes = round(char_len/1.34375)
	return str(secrets.token_urlsafe(nbytes))


def test_script(base):
	return str(base64.urlsafe_b64encode(hashlib.md5(str(base).encode('utf-8')).digest()), 'utf-8').rstrip("=")[0:15]


def nested_keys(input):
	dic = dict(input)
	keys_list = []
	dict_type = type(dic)
	for key, value in dic.items():
		if type(value) == dict_type:
			next_keys = nested_keys(value)
			for i in range(len(next_keys)):
				keys_list.append(key+"-"+next_keys[i])
		else:
			keys_list.append(key)
	return keys_list

