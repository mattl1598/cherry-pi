import requests
import json
import datetime
import hashlib

def get_time_stamp():
	return datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")


api_key = "0GVM6gyA-GbCfp7dSg1YDixAw0Pu51ECtPRxdH_k7wFXKz66U9sYox2XKlVtEZH1"
sensor_id = "test"
time_stamp = get_time_stamp()

header = {"content-type" : "application/json"}

test_data = {"type": "test", "values": {"Test Value": {"value": 75, "max": 100, "type": "test"}}}

request_json = {
				"sensor_id": sensor_id,
				"time_stamp": str(time_stamp),
				"verification": hashlib.sha256(str(time_stamp + api_key).encode()).hexdigest(),
				"data": test_data
				}

# Making a PUT request
r = requests.put('http://127.0.0.1:5000/sensor-api/update/', data=json.dumps(request_json), headers=header)

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)