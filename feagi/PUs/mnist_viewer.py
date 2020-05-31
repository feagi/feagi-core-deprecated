# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
import matplotlib.pyplot as plt
from IPU_vision import MNIST
import sys
import numpy as np


mnist = MNIST()


def mnist_plotter(mnist_type="training", subplot_dimension=5, desirable_label=6):
    counter = 0
    x_counter = 0
    y_counter = 0
    counter_limit = subplot_dimension * subplot_dimension
    f, axarr = plt.subplots(subplot_dimension, subplot_dimension)

    for entry in mnist.mnist_array[mnist_type]:

        label = entry[0]

        if label == desirable_label:

            # The rest of columns are pixels
            pixels = entry[1:]

            # Make those columns into a array of 8-bits pixels
            # This array will be of 1D with length 784
            # The pixel intensity values are integers from 0 to 255
            pixels = np.array(pixels, dtype='uint8')

            # Reshape the array into 28 x 28 array (2-dimensional array)
            pixels = pixels.reshape((28, 28))

            # Plot
            axarr[y_counter, x_counter].imshow(pixels)
            # Turn off tick labels
            axarr[y_counter, x_counter].set_yticklabels([])
            axarr[y_counter, x_counter].set_xticklabels([])
            axarr[y_counter, x_counter].axis('off')

            counter += 1
            if counter == counter_limit:
                # plt.tight_layout()
                plt.axis('off')
                # plt.figure(figsize=(1000, 1000))
                plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.001, hspace=0.001)
                plt.show()
                return

            if x_counter == (subplot_dimension - 1):
                y_counter += 1
                x_counter = 0
            else:
                x_counter += 1


if __name__ == "__main__":
    mnist_plotter(mnist_type='training', desirable_label=4, subplot_dimension=4)
    mnist_plotter(mnist_type='test', desirable_label=4, subplot_dimension=4)
