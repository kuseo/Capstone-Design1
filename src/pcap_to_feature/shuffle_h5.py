import h5py
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Shuffle datas, and separate them into train set and test set.")
parser.add_argument("input", type=str,
                    help="Input")
parser.add_argument("-r", "--ratio", type=int, choices=[9,8,7,6,5], default=8,
                    help="Ratio of training datasets")
args=parser.parse_args()

with h5py.File(args.input, "r") as f:
    x = np.array(f["data_x"][:])
    y = np.array(f["data_y"][:])

    m = x.shape[0] # number of datas

    np.random.seed(0)
    permutation = np.random.permutation(m)
    shuffled_x = np.take(x, permutation, axis=0)
    shuffled_y = np.take(y, permutation, axis=0)

    split_pos = int(m/args.ratio)
    test_x = shuffled_x[0:split_pos,:]
    test_y = shuffled_y[0:split_pos]
    train_x = shuffled_x[split_pos:m,:]
    train_y = shuffled_y[split_pos:m]

    with h5py.File("train.h5", "w") as train:
        with h5py.File("test.h5", "w") as test:
            train.create_dataset("data_x", data=train_x)
            train.create_dataset("data_y", data=train_y)

            test.create_dataset("data_x", data=test_x)
            test.create_dataset("data_y", data=test_y)

        