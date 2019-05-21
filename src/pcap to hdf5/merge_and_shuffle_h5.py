import h5py
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Merge two HDF5 files and shuffle their datas, and finally separate them into train set and test set.")
parser.add_argument("input1", type=str,
                    help="Input 1")
parser.add_argument("input2", type=str,
                    help="Input 2")
parser.add_argument("-r", "--ratio", type=int, choices=[9,8,7,6,5], default=8,
                    help="Ratio of training datasets")
args=parser.parse_args()

with h5py.File(args.input1, "r") as f1:
    with h5py.File(args.input2, "r") as f2:
        x1 = list(f1["data_x"])
        y1 = list(f1["data_y"])
        x2 = list(f2["data_x"])
        y2 = list(f2["data_y"])

        x = x1.append(x2)
        y = y1.append(y2)
        m = x.shape[0] # number of datas
        mini_batches = []
        np.random.seed(0)
        permutation = list(np.random.permutation(m))
        shuffled_x = x[permutation,:]
        shuffled_y = y[permutation,:]

        split_pos = int(m/args.ratio)
        test_x = shuffled_x[0:split_pos,:]
        test_y = shuffled_y[0:split_pos,:]
        train_x = shuffled_x[split_pos:m,:]
        train_y = shuffled_y[split_pos:m,:]

        with h5py.File("train.h5", "w") as train:
            with h5py.File("test.h5", "w") as test:
                train.create_dataset("data_x", data=train_x)
                train.create_dataset("data_y", data=train_y)

                test.create_dataset("data_x", data=test_x)
                test.create_dataset("data_y", data=test_y)

        