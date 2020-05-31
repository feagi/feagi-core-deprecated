# -*- coding: utf-8 -*-
"""
    Animated 3D sinc function
"""

from pyqtgraph.Qt import QtCore, QtGui
# from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import time
import os
import json
import numpy as np


global connectome_file_path, cortical_area, latest_modification_date, plot_data, threshold, neuron_locations

cortical_area = 'vision_memory'
threshold = 0.1
neuron_locations = []
connectome_file_path = './connectome_4/'


try:
    # connectome_file_path = sys.argv[1]
    if connectome_file_path:
        print("Connectome path is:", connectome_file_path)
except IndexError or NameError:
    print("Error occurred while setting the connectome path")

with open(connectome_file_path + 'genome_tmp.json', "r") as genome_file:
    genome_data = json.load(genome_file)
    genome = genome_data


cortical_file_path = connectome_file_path + cortical_area + '.json'
latest_modification_date = os.path.getmtime(cortical_file_path)


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

def load_cortical_data(cortical_area_name):
    if os.path.isfile(connectome_file_path + cortical_area_name + '.json'):
        with open(connectome_file_path + cortical_area_name + '.json', "r") as data_file:
            return json.load(data_file)
    else:
        print("Error: (", cortical_area_name, ") is not a valid cortical area")

class Visualizer(object):
    def __init__(self):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 450
        self.w.orbit(-180, -15)
        self.w.pan(100, 75, 50)
        self.w.setWindowTitle('FEAGI')
        # self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()
        print("Camera position is:", self.w.cameraPosition())

        g = gl.GLGridItem()
        g.scale(20, 20, 20)
        g.translate(200, 200, 0)
        self.w.addItem(g)

        # self.pts = np.array(neuron_positions('vision_memory'))
        self.pts = neuron_positions('vision_memory')
        for i in range(self.pts.shape[0]):
            self.traces[i] = gl.GLScatterPlotItem(pos=self.pts,
                                                  color=(1, 1, 1, .3),
                                                  size=0.1,
                                                  pxMode=True)
            self.w.addItem(self.traces[i])


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, points, color, size):
        self.traces[name].setData(pos=points, color=color, size=size)

    def update(self):
        connectome_data_fetcher(cortical_area)
        data_points = self.pts.shape[0]
        for i in range(data_points):
            self.set_plotdata(
                name=i, points=self.pts,
                color=pg.glColor((i, 100)),
                size=3
            )


def neuron_positions(cortical_area):
    cortical_data = load_cortical_data(cortical_area)
    positions = []
    for neuron_id in cortical_data:
        neuron_position = [cortical_data[neuron_id]['location']]
        positions.append(neuron_position)
    return np.array(positions)


def build_plot_data(cortical_area, threshold):
    plot_data = []
    brain = load_brain()
    data = brain[cortical_area]
    for neuron_id in data:
        if data[neuron_id]["neighbors"].keys():
            source_location = data[neuron_id]["location"]
            for subkey in data[neuron_id]["neighbors"]:
                if (data[neuron_id]['neighbors'][subkey]['cortical_area'] == cortical_area) and (
                        data[neuron_id]['neighbors'][subkey]['postsynaptic_current'] >= threshold):
                    destination_location = data[subkey]["location"]
                    if source_location not in plot_data:
                        plot_data.append(source_location)
                    if destination_location not in plot_data:
                        plot_data.append(destination_location)
    print(">>>-->>>")
    i = 0
    for _ in plot_data:
        print(i,'', _)
        i += 1
    print("<<<--<<<")
    return plot_data

plot_data = build_plot_data(cortical_area, threshold)

def connectome_data_fetcher(cortical_area, threshold=0.1):
    """Visualizes the Neurons in the connectome"""

    global latest_modification_date, plot_data

    new_modification_date = os.path.getmtime(cortical_file_path)
    print('---')
    if latest_modification_date != new_modification_date:
        print('+++')
        print(new_modification_date)

        latest_modification_date = new_modification_date
        previous_plot_data = plot_data
        print("previous plot data size=", np.array(previous_plot_data).shape)

        plot_data = build_plot_data(cortical_area, threshold)
        print("plot data size=", np.array(plot_data).shape)

        plot_delta = []
        print("*************************************")

        if plot_data != previous_plot_data:
            for item in plot_data:
                if item not in previous_plot_data and item not in plot_delta:
                    plot_delta.append(item)

            print("plot_delta:")
            for _ in plot_delta:
                    print(_)
            print("^^^^^^^^^^")
            pos = np.array(plot_delta)
            total_points = np.array(plot_data)
            print(">>>>", pos.shape, total_points.shape)
            if pos != []:
                # print("POS:\n", pos)
                v.pts = pos
                print("Animation completed successfully")
        else:
            print("Plot data has remained unchanged...")

    time.sleep(5)


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    v = Visualizer()

    # neuron_locations = neuron_positions('vision_memory')

    timer = QtCore.QTimer()
    timer.timeout.connect(v.update)
    timer.start()
    v.start()

