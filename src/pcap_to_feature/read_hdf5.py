import h5py

with h5py.File("test.h5", "r") as f:
    group = list(f.keys())
    for key in group:
        print(key)
        print(list(f[key])) # [size, protocol, bandwidth, endpoint, T1, T2, T3]