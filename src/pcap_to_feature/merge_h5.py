import h5py
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Merge two HDF5 files.")
parser.add_argument("input1", type=str,
                    help="Input 1")
parser.add_argument("input2", type=str,
                    help="Input 2")
parser.add_argument("-o", "--output", type=str, default="output.h5",
                    help="Output file name")
args=parser.parse_args()

with h5py.File(args.input1, "r") as f1:
    with h5py.File(args.input2, "r") as f2:
        x1 = np.array(f1["data_x"][:])
        y1 = np.array(f1["data_y"][:])
        x2 = np.array(f2["data_x"][:])
        y2 = np.array(f2["data_y"][:])

        x = np.append(x1, x2, axis=0)
        y = np.append(y1, y2, axis=0)

        with h5py.File(args.output, "w") as f:
            f.create_dataset("data_x", data=x)
            f.create_dataset("data_y", data=y)