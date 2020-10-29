import requests
import json
import datetime
import hashlib

def get_time_stamp():
	return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


api_key = "0GVM6gyA-GbCfp7dSg1YDixAw0Pu51ECtPRxdH_k7wFXKz66U9sYox2XKlVtEZH1"
api_key2 = "_tHUemb1Kr-E36Hhv7ToGC1RyTjkmatfWA6nUADrC1vYnwIY6G_-z7NjeOefrgpZ"
sensor_id = "test"
sensor_id2 = "OUjb9xP5fYH32qbW"
time_stamp = get_time_stamp()

header = {"content-type": "application/json"}

test_data = {"type": "test", "values": {"Test Value": {"value": 64, "max": 100, "type": "test"}}}
test_data2 = {"type": "test", "values": {
	"Charger 1": {"value": 42, "max": 100, "type": "test"},
	"Charger 2": {"value": 25, "max": 100, "type": "test"},
	"Charger 3": {"value": 2, "max": 100, "type": "test"}
}}

request_json = {
				"sensor_id": sensor_id,
				"time_stamp": str(time_stamp),
				"verification": hashlib.sha256(str(time_stamp + api_key).encode()).hexdigest(),
				"data": test_data
				}

# Making a PUT request
r = requests.put('http://larby.co.uk/sensor-api/update/', data=json.dumps(request_json), headers=header)

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)