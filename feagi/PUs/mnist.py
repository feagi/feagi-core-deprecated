
"""
This Module provides the ability to read data from MNIST database
Source: https://gist.github.com/akesling/5358964

Loosely inspired by http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
which is GPL licensed.
"""

import os
import struct
import numpy as np
import random

# import sys
# sys.path.append('/usr/local/opt/opencv3/lib/python3.6/site-packages/')
# import cv2
# from matplotlib import pyplot as plt
# import IPU_vision
#
# import settings
# import multiprocessing as mp


# def read_mnist_raw2(dataset="training", path="../MNIST/"):
#     """
#     Python function for importing the MNIST data set.  It returns an iterator
#     of 2-tuples with the first element being the label and the second element
#     being a numpy.uint8 2D array of pixel data for the given image.
#     """
#     if dataset is "training":
#         fname_img = os.path.join(path, 'train-images.idx3-ubyte')
#         fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
#     elif dataset is "testing":
#         fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
#         fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
#     else:
#         raise Exception(ValueError, "data set must be 'testing' or 'training'")
#
#     # Load everything in some numpy arrays
#     with open(fname_lbl, 'rb') as flbl:
#         magic, num = struct.unpack(">II", flbl.read(8))
#         lbl = np.fromfile(flbl, dtype=np.int8)
#
#     with open(fname_img, 'rb') as fimg:
#         magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
#         img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)
#
#     get_img = lambda idx: (lbl[idx], img[idx])
#
#     # Create an iterator which returns each image in turn
#     for i in range(len(lbl)):
#         yield get_img(i)


# def cv_code(img):
#     laplacian = cv2.Laplacian(img, cv2.CV_64F)
#
#     sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
#     sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
#
#     edges = cv2.Canny(img, 1, 1)
#
#     rows, cols = img.shape
#     r45 = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
#     rotate45 = cv2.warpAffine(img, r45, (cols, rows))
#
#     rows, cols = img.shape
#     r90 = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
#     rotate90 = cv2.warpAffine(img, r90, (cols, rows))
#     return laplacian, sobelx, sobely, edges, rows, r45, rotate45, rotate90
#
# cv_process = mp.Process(name='CV Process', target=cv_code, args=(img,))
# cv_process.start()
# cv_process.join()
#
# if runtime_data.parameters["Switches"]["vis_show"]:
#     plt.subplot(3, 3, 1), plt.imshow(img, cmap='gray')
#     plt.title('Original'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 2), plt.imshow(laplacian, cmap='gray')
#     plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 3), plt.imshow(sobelx, cmap='gray')
#     plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 4), plt.imshow(sobely, cmap='gray')
#     plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 5), plt.imshow(edges, cmap='gray')
#     plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 6), plt.imshow(rotate45, cmap='gray')
#     plt.title('Rotate 45'), plt.xticks([]), plt.yticks([])
#     plt.subplot(3, 3, 7), plt.imshow(rotate90, cmap='gray')
#     plt.title('Rotate 90'), plt.xticks([]), plt.yticks([])


# def show(image):
#     """
#     Render a given numpy.uint8 2D array of pixel data.
#     """
#     fig = pyplot.figure()
#     ax = fig.add_subplot(1,1,1)
#     imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
#     imgplot.set_interpolation('nearest')
#     ax.xaxis.set_ticks_position('top')
#     ax.yaxis.set_ticks_position('left')
#     pyplot.show()
