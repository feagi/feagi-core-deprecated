# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
# -*- coding: utf-8 -*-
"""
This standalone module is intended to launch independent of the main brain application with the purpose of reading the
contents of connectome and visualizing various aspects.
"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg

import os
import json
import time
import random
import numpy as np


global connectome_file_path

try:
    # connectome_file_path = sys.argv[1]
    connectome_file_path = './connectome_4/'
    if connectome_file_path:
        print("Connectome path is:", connectome_file_path)
except IndexError or NameError:
    print("Error occurred while setting the connectome path")

with open(connectome_file_path + 'genome_tmp.json', "r") as genome_file:
    genome_data = json.load(genome_file)
    genome = genome_data

blueprint = genome["blueprint"]
cortical_list = []
for key in blueprint:
    cortical_list.append(key)

def load_brain():
    global connectome_file_path
    brain = {}
    for item in cortical_list:
        if os.path.isfile(connectome_file_path + item + '.json'):
            with open(connectome_file_path + item + '.json', "r") as data_file:
                data = json.load(data_file)
                brain[item] = data
    return brain


class Visualizer(object):
    def __init__(self):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        # create the background grids
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)

        # self.n = 1
        # self.m = 1000
        # self.y = np.linspace(-10, 10, self.n)
        # self.x = np.linspace(-10, 10, self.m)
        # self.phase = 0
        #
        # for i in range(self.n):
        #     yi = np.array([self.y[i]] * self.m)
        #     d = np.sqrt(self.x ** 2 + yi ** 2)
        #     z = 10 * np.cos(d + self.phase) / (d + 1)
        #     pts = np.vstack([self.x, yi, z]).transpose()
        #     self.traces[i] = gl.GLLinePlotItem(pos=pts, color=pg.glColor(
        #         (i, self.n * 1.3)), width=(i + 1) / 10, antialias=True)
        #     self.w.addItem(self.traces[i])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    # def update(self, pos):
    #     for i in range(self.n):
    #         # yi = np.array([self.y[i]] * self.m)
    #         # d = np.sqrt(self.x ** 2 + yi ** 2)
    #         # z = 10 * np.cos(d + self.phase) / (d + 1)
    #         # pts = np.vstack([self.x, yi, z]).transpose()
    #         self.set_plotdata(
    #             name=i, points=pos,
    #             color=pg.glColor((i, self.n * 1.3)),
    #             width=(i + 1) / 10
    #         )
    #         self.phase -= .003

    def animation(self, pos):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.set_plotdata(
                name=0, points=pos,
                color=pg.glColor((1, 1.3)),
                width=0.1
            ))
        timer.start(20)
        self.start()



def connectome_visualizer(cortical_area, neuron_show=False, neighbor_show=False, threshold=0):
    """Visualizes the Neurons in the connectome"""

    print('1')
    cortical_file_path = connectome_file_path + cortical_area + '.json'
    latest_modification_date = os.path.getmtime(cortical_file_path)
    print('2')
    brain = load_brain()
    neuron_locations = []
    for key in brain[cortical_area]:
        location_data = brain[cortical_area][key]["location"]
        location_data.append(brain[cortical_area][key]["cumulative_fire_count"])
        neuron_locations.append(location_data)
    print('3')
    print('4')
    color = ["r", "b", "g", "c", "m", "y", "k", "w"]

    # todo: Figure how to determine the delta between previous data-set and new one to solve cumulative plot issue
    plot_data = []




    while 1 == 1:
        new_modification_date = os.path.getmtime(cortical_file_path)
        print('5')
        if latest_modification_date != new_modification_date:
            print('6')
            print(new_modification_date)
            random_color = color[random.randrange(0, len(color))]
            latest_modification_date = new_modification_date
            old_brain = brain

            previous_plot_data = plot_data

            brain = load_brain()

            # Displays the Axon-Dendrite connections when True is set
            if neighbor_show:
                data = brain[cortical_area]

                # todo: need to compile a matrix with all source and destinations first before plotting them all
                plot_data = []

                for neuron_id in data:
                    if data[neuron_id]["neighbors"].keys():
                        source_location = data[neuron_id]["location"]
                        for subkey in data[neuron_id]["neighbors"]:
                            if (data[neuron_id]['neighbors'][subkey]['cortical_area'] == cortical_area) and (
                                    data[neuron_id]['neighbors'][subkey]['postsynaptic_current'] >= threshold):
                                destination_location = data[subkey]["location"]
                                plot_data.append(source_location)
                                plot_data.append(destination_location)

                # print(plot_data)

                # todo: build the delta between previous plot data and new plot data
                plot_delta = []
                for item in plot_data:
                    if item not in previous_plot_data:
                        plot_delta.append(item)

            pos = np.array(plot_delta)
            if pos != []:
                print("POS:\n", pos)
                v.animation(pos)

        time.sleep(5)




if __name__ == '__main__':
    v = Visualizer()
    # connectome_visualizer(sys.argv[2], neuron_show=False, neighbor_show=True)
    connectome_visualizer('vision_memory', neighbor_show=True, neuron_show=False)

    # connectome_visualizer_xxx(sys.argv[2], sys.argv[3], neuron_show=False, neighbor_show=True)

    # if sys.flags.interactive != 1:
    #     app.run()
