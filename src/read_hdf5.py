import h5py

with h5py.File('sample.h5', 'r') as f:
    group = list(f.keys())
    data = list(f[group[1]])
    print(data) # [size, protocol, bandwidth, endpoint, T1, T2, T3]