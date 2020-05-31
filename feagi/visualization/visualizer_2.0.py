# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
"""
This standalone module is intended to launch independent of the main brain application with the purpose of reading the
contents of connectome and visualizing various aspects.
"""
import os
import json
import time
import random
import numpy as np

from vispy import app, visuals, scene


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


            # build visuals
            Plot3D = scene.visuals.create_visual_node(visuals.LinePlotVisual)

            # build canvas
            canvas = scene.SceneCanvas(keys='interactive', title='plot3d', show=True)

            # Add a ViewBox to let the user zoom/rotate
            view = canvas.central_widget.add_view()
            view.camera = 'turntable'
            view.camera.fov = 45
            view.camera.distance = 600

            # plot
            print(plot_delta)
            pos = np.array(plot_delta)
            print(pos)
            if pos != []:
                Plot3D(pos, width=2.0, color='red',
                       edge_color='w', symbol='o', face_color=(0.2, 0.2, 1, 0.8),
                       parent=view.scene)
                if sys.flags.interactive != 1:
                    app.run()
        time.sleep(5)






def visualize_cortical_mapping(source_area, destination_area):
    """Visualizes the connection between two cortical areas"""





if __name__ == '__main__':

    # connectome_visualizer(sys.argv[2], neuron_show=False, neighbor_show=True)
    connectome_visualizer('vision_memory', neuron_show=False, neighbor_show=True)

    # connectome_visualizer_xxx(sys.argv[2], sys.argv[3], neuron_show=False, neighbor_show=True)

    # if sys.flags.interactive != 1:
    #     app.run()
