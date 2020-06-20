import base64
import hashlib


def test_script(base):
	return str(base64.urlsafe_b64encode(hashlib.md5(str(base).encode('utf-8')).digest()), 'utf-8').rstrip("=")[0:15]
