import datetime

with open("test.txt", "w") as file:
	file.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

print("done")
