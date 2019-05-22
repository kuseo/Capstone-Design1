device = {"01":"asdf", "11":"1234", "96":"qwer"}
pair = ((key, 0) for key in list(device.keys()))
device_score = dict(pair)
print(device_score)
# device_score would be like
# { "11.22.33.44":0, "12.34.56.78":0, "99.88.77.66":0, ... }