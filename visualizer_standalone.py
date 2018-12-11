"""
This standalone module is intended to launch independent of the main brain application with the purpose of reading the
contents of connectome and visualizing various aspects.
"""


import sys
sys.path.append('/Users/mntehrani/Documents/PycharmProjects/Metis/venv/lib/python3.7/site-packages/')

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib import style
from matplotlib import pyplot as plt

style.use('dark_background')

def vis_init():
    # plt.ion()
    print("Initializing plot...")
    global Arrow3D

    class Arrow3D(FancyArrowPatch):
        def __init__(self, xs, ys, zs, *args, **kwargs):
            FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
            self._verts3d = xs, ys, zs

        def draw(self, renderer):
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
            self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
            FancyArrowPatch.draw(self, renderer)

        # plt.ion()
        global fig
        fig = pylab.plt.figure()
        global ax
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 30)
        ax.set_zlim(0, 30)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        fig.suptitle("Main plot")
        

if __name__ == '__main__':
    import os
    import json
    import matplotlib.pylab as pylab

    try:
        connectome_file_path = sys.argv[1]
        if connectome_file_path:
            print("Connectome path is:", connectome_file_path)
    except IndexError or NameError:
        print("Error occurred while setting the connectome path")


    with open(connectome_file_path+'genome_tmp.json', "r") as genome_file:
        genome_data = json.load(genome_file)
        genome = genome_data

    blueprint = genome["blueprint"]
    cortical_list = []
    for key in blueprint:
        cortical_list.append(key)

    brain = {}
    for item in cortical_list:
        if os.path.isfile(connectome_file_path + item + '.json'):
            with open(connectome_file_path + item + '.json', "r") as data_file:
                data = json.load(data_file)
                brain[item] = data
    print("Brain has been successfully loaded into memory...")

    vis_init()

    def connectome_visualizer(cortical_area, neuron_show=False, neighbor_show=False, threshold=0):
        """Visualizes the Neurons in the connectome"""

        neuron_locations = []
        for key in brain[cortical_area]:
            location_data = brain[cortical_area][key]["location"]
            location_data.append(brain[cortical_area][key]["cumulative_fire_count"])
            neuron_locations.append(location_data)

        ax.set_xlim(
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][0],
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][1])
        ax.set_ylim(
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][0],
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][1])
        ax.set_zlim(
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["z"][0],
            genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["z"][1])

        if neuron_show:
            for location in neuron_locations:
                ax.scatter(location[0], location[1], location[2], c='b', marker='.')

        # Displays the Axon-Dendrite connections when True is set
        if neighbor_show:
            data = brain[cortical_area]

            # The following code scans thru connectome and extract locations for source and destination neurons
            for key in data:
                if data[key]["neighbors"].keys():
                    source_location = data[key]["location"]
                    for subkey in data[key]["neighbors"]:
                        if (data[key]['neighbors'][subkey]['cortical_area'] == cortical_area) and (
                                data[key]['neighbors'][subkey]['postsynaptic_current'] >= threshold):
                            destination_location = data[subkey]["location"]
                            a = Arrow3D([source_location[0], destination_location[0]],
                                        [source_location[1], destination_location[1]],
                                        [source_location[2], destination_location[2]],
                                        mutation_scale=10, lw=1, arrowstyle="->", color="r")
                            ax.add_artist(a)
        pylab.plt.show()
        # pylab.plt.draw()
        pylab.plt.pause(1)
        return

    def connectome_visualizer_xxx(cortical_area_src, cortical_area_dst, neuron_show=False, neighbor_show=False, threshold=0):
        """Visualizes the Neurons in the connectome"""

        graph_constant = 200
        cortical_index = 0
        cortical_area_list = [cortical_area_src, cortical_area_dst]


        x_max = max(genome['blueprint'][cortical_area_list[0]]["neuron_params"]["geometric_boundaries"]["x"][1]-
                    genome['blueprint'][cortical_area_list[0]]["neuron_params"]["geometric_boundaries"]["x"][0],
                    genome['blueprint'][cortical_area_list[1]]["neuron_params"]["geometric_boundaries"]["x"][1]-
                    genome['blueprint'][cortical_area_list[1]]["neuron_params"]["geometric_boundaries"]["x"][0])

        y_max = max(genome['blueprint'][cortical_area_list[0]]["neuron_params"]["geometric_boundaries"]["y"][1]-
                    genome['blueprint'][cortical_area_list[0]]["neuron_params"]["geometric_boundaries"]["y"][0],
                    genome['blueprint'][cortical_area_list[1]]["neuron_params"]["geometric_boundaries"]["y"][1]-
                    genome['blueprint'][cortical_area_list[1]]["neuron_params"]["geometric_boundaries"]["y"][0])

        z_max = 300


        for cortical_area in cortical_area_list:
            delta = graph_constant * cortical_index
            neuron_locations = []
            for key in brain[cortical_area]:
                location_data = brain[cortical_area][key]["location"]
                location_data.append(brain[cortical_area][key]["cumulative_fire_count"])
                neuron_locations.append(location_data)

            ax.set_xlim(0, x_max)
            ax.set_ylim(0, y_max)
            ax.set_zlim(0, z_max)
            if neuron_show:
                for location in neuron_locations:
                    ax.scatter(location[0], location[1], location[2]+delta, c='b', marker='.')
            cortical_index += 1

        # Displays the Axon-Dendrite connections when True is set
        if neighbor_show:
            data = brain[cortical_area_src]

            # The following code scans thru connectome and extract locations for source and destination neurons
            for key in data:
                if data[key]["neighbors"].keys():
                    source_location = data[key]["location"]
                    for subkey in data[key]["neighbors"]:
                        if (data[key]['neighbors'][subkey]['cortical_area'] == cortical_area_dst) and (
                                data[key]['neighbors']
                                [subkey]['postsynaptic_current'] > threshold):
                            destination_location = brain[cortical_area_dst][subkey]["location"]
                            a = Arrow3D([source_location[0], destination_location[0]],
                                        [source_location[1], destination_location[1]],
                                        [source_location[2], destination_location[2]+graph_constant],
                                        mutation_scale=10, lw=1, arrowstyle="->", color="r")
                            ax.add_artist(a)

        pylab.plt.show()
        # pylab.plt.pause(0.01)
        return


    def visualize_cortical_mapping(source_area, destination_area):
        """Visualizes the connection between two cortical areas"""


    connectome_visualizer(sys.argv[2], neuron_show=False, neighbor_show=True)
    # connectome_visualizer_xxx(sys.argv[2], sys.argv[3], neuron_show=False, neighbor_show=True)
