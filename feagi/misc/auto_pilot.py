# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
import random
from PUs import IPU_vision


def training_num_gen(num):
    rand_img_index = random.randrange(10, 500, 1)
    mnist = IPU_vision.MNIST()
    mnist_data = mnist.read_image(rand_img_index)
    labeled_img = mnist.read_image(random.randrange(10, 500, 1))

    while int(num) != mnist_data[1]:
        rand_img_index = random.randrange(10, 500, 1)
        mnist_data = mnist.read_image(rand_img_index)
        print("mnist_data[1] type is: ", type(mnist_data[1]))
        labeled_img = mnist.read_image(random.randrange(10, 500, 1))
        print("training number generator is using the random index :", rand_img_index)
        print("training number is: ", num)
        print("mnist data label is:", mnist_data[1])
        print("\n")
    return rand_img_index, labeled_img









