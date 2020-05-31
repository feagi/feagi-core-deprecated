# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>

import os
import struct
import numpy as np


def read_mnist_labels(dataset="training", path="../../Fashion-MNIST/"):
    """
    For importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """
    if dataset is "training":
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset is "testing":
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise Exception(ValueError, "data set must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    get_img_lbl = lambda idx: (lbl[idx])

    # Create an iterator which returns each image in turn
    for i in range(len(lbl)):
        yield get_img_lbl(i)


mnist_labels = read_mnist_labels()
for label in mnist_labels:
    print(label)