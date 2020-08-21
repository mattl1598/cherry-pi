import base64
import hashlib
import secrets
import matplotlib.pyplot as plt
import numpy as np
import datetime
import io

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


def one_line_graph(graph_tuples, graph_series, xlim=None):
	if xlim is not None:
		plt.xlim(xlim)
		x = []
		y = []
	else:
		start_date = datetime.datetime.strptime(graph_tuples[0][0], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(days=1)
		plt.xlim(start_date, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
		# x = []
		# y = []
		x = [start_date]
		y = [graph_tuples[0][1]["values"][graph_series[0]]["value"]]

	for value in graph_tuples:
		x.append(datetime.datetime.strptime(value[0], "%Y-%m-%d %H:%M:%S"))
		print(value[1])
		y.append(value[1]["values"][graph_series[0]]["value"])
	# plot
	plt.step(x, y)

	# beautify the x-labels
	plt.gcf().autofmt_xdate()

	pic_IObytes = io.BytesIO()
	plt.savefig(pic_IObytes, format='png')
	pic_IObytes.seek(0)
	pic_hash = base64.b64encode(pic_IObytes.read())
	plt.clf()
	plt.close()

	return pic_hash


def multi_line_graph(graph_tuples, graph_series, xlim=None):
	if xlim is not None:
		plt.xlim(xlim)
		x = []
		y_squared = {}
		for series in graph_series:
			y_squared[series] = []
	else:
		start_date = datetime.datetime.strptime(graph_tuples[0][0], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(days=1)
		plt.xlim(start_date, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
		x = [start_date]
		y_squared = {}
		for series in graph_series:
			y_squared[series] = [graph_tuples[0][1]["values"][graph_series[0]]["value"]]


	for value in graph_tuples:
		x.append(datetime.datetime.strptime(value[0], "%Y-%m-%d %H:%M:%S"))
		print(value[1])
		for series in graph_series:
			y_squared[series].append(value[1]["values"][series]["value"])

	for series in graph_series:
		plt.step(x, y_squared[series])
	# beautify the x-labels
	plt.gcf().autofmt_xdate()

	pic_IObytes = io.BytesIO()
	plt.savefig(pic_IObytes,  format='png')
	pic_IObytes.seek(0)
	pic_hash = base64.b64encode(pic_IObytes.read())
	plt.clf()
	plt.close()

	return pic_hash

