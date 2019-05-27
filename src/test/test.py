'''
device = {"01":"asdf", "11":"1234", "96":"qwer"}
pair = ((key, 0) for key in list(device.keys()))
device_score = dict(pair)
print(device_score)
# device_score would be like
# { "11.22.33.44":0, "12.34.56.78":0, "99.88.77.66":0, ... }

li = [2,4,6,8]
it = iter(li)
for v in range(next(it), next(it)):
    print(v)

li = [1]
for v in li[0:0]:
    print(v)

import numpy as np
import h5py
with h5py.File("./merged.h5", "r") as f:
    x = np.array(f["data_x"][:])
    print(x.shape)

import numpy as np

np.random.seed(0)
test = np.array([1,2,3,4,5])
m = test.shape[0]
permutation = np.random.permutation(m)
new = np.take(test, permutation, axis=0)
print(new)

'''
import numpy as np
import h5py
test_dataset = h5py.File("test.h5", "r")
test_set_x = np.array(test_dataset["data_x"][:]) # test set features
test_set_y = np.array(test_dataset["data_y"][:]) # test set labels
print(test_set_x)
print(test_set_y)