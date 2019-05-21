import h5py
import numpy as np

def load_dataset():
    train_dataset = h5py.File("./datasets/train.h5", "r")
    train_set_x = np.array(train_dataset["data_x"][:]) # train set features
    train_set_y = np.array(train_dataset["data_y"][:]) # train set labels

    test_dataset = h5py.File("./datasets/test.h5", "r")
    test_set_x = np.array(test_dataset["data_x"][:]) # test set features
    test_set_y = np.array(test_dataset["data_y"][:]) # test set labels
    
    return train_set_x, train_set_y, test_set_x, test_set_y

