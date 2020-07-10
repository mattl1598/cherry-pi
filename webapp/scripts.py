import base64
import hashlib
import secrets


def key_64(char_len):
	nbytes = round(char_len/1.34375)
	return str(secrets.token_urlsafe(nbytes))


def test_script(base):
	return str(base64.urlsafe_b64encode(hashlib.md5(str(base).encode('utf-8')).digest()), 'utf-8').rstrip("=")[0:15]
