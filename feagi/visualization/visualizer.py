# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
"""
This file contains all of the Visualization functions
"""

import ast
from time import sleep
import json

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pylab as pylab
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib import style

# style.use('dark_background')

from architect import connectome_location_data
from misc.neuron_functions import fire_candidate_locations
from configuration import runtime_data

print("777", runtime_data.cortical_list)


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

    runtime_data.parameters["Switches"]["vis_init_status"] = True


def init_figures():
    # global burst_figure
    # burst_figure = plt.figure(figsize=plt.figaspect(.15))
    # plt.thismanager = plt.get_current_fig_manager()
    # plt.thismanager.window.wm_geometry("+80+800")

    global input_figure
    input_figure = pylab.plt.figure(figsize=(2, 3))
    pylab.plt.thismanager = pylab.plt.get_current_fig_manager()
    pylab.plt.thismanager.window.wm_geometry("+20+600")
    pylab.plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    global vision_figure
    vision_figure = pylab.plt.figure(figsize=(6, 10))
    pylab.plt.thismanager = pylab.plt.get_current_fig_manager()
    pylab.plt.thismanager.window.wm_geometry("+300+20")
    pylab.plt.subplots_adjust(left=0, bottom=0, right=1, top=.98, wspace=0.2, hspace=0)

    global memory_figure
    memory_figure = pylab.plt.figure(figsize=(2, 6))
    pylab.plt.thismanager = pylab.plt.get_current_fig_manager()
    pylab.plt.thismanager.window.wm_geometry("+920+300")
    pylab.plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    global output_figure
    output_figure = pylab.plt.figure(figsize=(2, 3))
    pylab.plt.thismanager = pylab.plt.get_current_fig_manager()
    pylab.plt.thismanager.window.wm_geometry("+1200+600")
    pylab.plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)


def setup_canvas(entry):

    global d_vision, d_ipu, d_memory, d_opu

    if runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'vision':
        if runtime_data.genome['blueprint'][entry[1]]['sub_group_id'] == 'vision_v1':
            d_vision = vision_figure.add_subplot(7,
                                                 3,
                                                 runtime_data.genome['blueprint'][entry[1]]['plot_index'],
                                                 projection='3d', aspect='equal')
            d_vision.set_title(entry[1])
            d_vision.set_xlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
            d_vision.set_ylim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
            d_vision.set_zlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
            d_vision.set_xlabel('X Label')
            d_vision.set_ylabel('Y Label')
            d_vision.set_zlabel('Z Label')

        elif runtime_data.genome['blueprint'][entry[1]]['sub_group_id'] == 'vision_v2':
            d_vision = vision_figure.add_subplot(7, 3, runtime_data.genome['blueprint']
            [entry[1]]['plot_index'], projection='3d', aspect='equal')
            d_vision.set_title(entry[1])
            d_vision.set_xlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
            d_vision.set_ylim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
            d_vision.set_zlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
            d_vision.set_xlabel('X Label')
            d_vision.set_ylabel('Y Label')
            d_vision.set_zlabel('Z Label')
        elif runtime_data.genome['blueprint'][entry[1]]['sub_group_id'] == 'vision_IT':
            d_vision = vision_figure.add_subplot(7, 3, runtime_data.genome['blueprint']
            [entry[1]]['plot_index'], projection='3d', aspect='equal')
            d_vision.set_title(entry[1])
            d_vision.set_xlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
            d_vision.set_ylim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
            d_vision.set_zlim(
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
                runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
            d_vision.set_xlabel('X Label')
            d_vision.set_ylabel('Y Label')
            d_vision.set_zlabel('Z Label')

    elif runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'Memory':
        d_memory = memory_figure.add_subplot(2, 1, runtime_data.genome['blueprint']
        [entry[1]]['plot_index'], projection='3d')
        d_memory.set_title(entry[1])
        d_memory.set_xlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
        d_memory.set_ylim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
        d_memory.set_zlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
        d_memory.set_xlabel('X Label')
        d_memory.set_ylabel('Y Label')
        d_memory.set_zlabel('Z Label')

    elif runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'IPU':
        d_ipu = input_figure.add_subplot(1, 1, runtime_data.genome['blueprint']
        [entry[1]]['plot_index'], projection='3d')
        d_ipu.set_title(entry[1])
        d_ipu.set_xlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
        d_ipu.set_ylim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
        d_ipu.set_zlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
        d_ipu.set_xlabel('X Label')
        d_ipu.set_ylabel('Y Label')
        d_ipu.set_zlabel('Z Label')

    elif runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'OPU':
        d_opu = output_figure.add_subplot(1, 1, runtime_data.genome['blueprint']
        [entry[1]]['plot_index'], projection='3d')
        d_opu.set_title(entry[1])
        d_opu.set_xlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["x"][1])
        d_opu.set_ylim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["y"][1])
        d_opu.set_zlim(
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][0],
            runtime_data.genome['blueprint'][entry[1]]["neuron_params"]["geometric_boundaries"]["z"][1])
        d_opu.set_xlabel('X Label')
        d_opu.set_ylabel('Y Label')
        d_opu.set_zlabel('Z Label')


def burst_visualization_manager():

    index = 0
    global indexed_cortical_list
    indexed_cortical_list = []
    for key in runtime_data.cortical_list:
        indexed_cortical_list.append([index, key])
        index += 1

    while 1==1:
        animate()

    pylab.plt.show()


def animate():
    global d_vision, d_ipu, d_memory, d_opu

    with open('./fcl_repo/fcl.json', 'r') as fcl_file:
        raw_data = fcl_file.read()
        success = False
        try:
            fcl = ast.literal_eval(raw_data)
            success = True
        finally:
            if not success:
                fcl = []

    if len(fcl) > 2:
        neuron_locations = fire_candidate_locations(fcl)
        for entry in indexed_cortical_list:
            try:
                setup_canvas(entry)

                for location in neuron_locations[entry[1]]:
                    if runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'vision':
                        d_vision.scatter3D(location[0], location[1], location[2], c='r', marker='^')
                    if runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'Memory':
                        d_memory.scatter3D(location[0], location[1], location[2], c='r', marker='^')
                    if runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'IPU':
                        d_ipu.scatter3D(location[0], location[1], location[2], c='r', marker='^')
                    if runtime_data.genome['blueprint'][entry[1]]['group_id'] == 'OPU':
                        d_opu.scatter3D(location[0], location[1], location[2], c='r', marker='^')
            finally:
                pass

        fig.canvas.draw()
        pylab.plt.pause(0.1)
        pylab.plt.clf()
        d_vision.cla()
        d_memory.cla()
        d_ipu.cla()
        d_opu.cla()

    else:
        sleep(1)


def connectome_visualizer(cortical_area, neighbor_show='false', threshold=0):
    """Visualizes the Neurons in the connectome"""
    if not runtime_data.parameters["Switches"]["vis_init_status"]:
        vis_init()
    neuron_locations = connectome_location_data(cortical_area)

    ax.set_xlim(
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][0],
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][1])
    ax.set_ylim(
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][0],
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][1])
    ax.set_zlim(
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["z"][0],
        runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["z"][1])

    for location in neuron_locations:
        ax.scatter(location[0], location[1], location[2], c='b', marker='.')

    # Displays the Axon-Dendrite connections when True is set
    if neighbor_show == 'true':
        data = runtime_data.brain[cortical_area]

        # The following code scans thru connectome and extract locations for source and destination neurons
        for key in data:
            if data[key]["neighbors"].keys():
                source_location = data[key]["location"]
                for subkey in data[key]["neighbors"]:
                    if (data[key]['neighbors'][subkey]['cortical_area'] == cortical_area) and (data[key]['neighbors']
                                [subkey]['postsynaptic_current'] > threshold):
                        destination_location = data[subkey]["location"]
                        a = Arrow3D([source_location[0], destination_location[0]],
                                    [source_location[1], destination_location[1]],
                                    [source_location[2], destination_location[2]],
                                    mutation_scale=10, lw=1, arrowstyle="->", color="r")
                        ax.add_artist(a)
    pylab.plt.show()
    pylab.plt.pause(runtime_data.parameters["Timers"]["burst_timer"])
    return


# def cortical_activity_visualizer(cortical_list, x=30, y=30, z=30):
#     """Visualizes the extent of Neuron activities"""
#     if not runtime_data.parameters["Switches"]["vis_init_status"]:
#         vis_init()
#
#     # fig = pylab.plt.figure()
#     fig = pylab.plt.figure(figsize=pylab.plt.figaspect(.2))
#     fig.suptitle('Cortical Activities\n')
#
#     for cortical_area in runtime_data.cortical_list:
#         neuron_locations = connectome_location_data(cortical_area)
#         aa = fig.add_subplot(1, len(runtime_data.cortical_areas)+1, runtime_data.cortical_areas.index(cortical_area)+1)
#         aa.set_title(cortical_area)
#         aa.set_xlim(0, x)
#         aa.set_ylim(0, y)
#         # aa.set_zlim(0, z)
#         for location in neuron_locations:
#             # aa.scatter(location[0], location[1], location[2], s=location[3])
#             aa.scatter(location[0], location[1], s=location[3])
#     pylab.plt.show()
#     pylab.plt.pause(1)


# def mnist_img_show(IPU_input):
#     """ Displays the image from MNIST database"""
#
#     aa = input_figure.add_subplot(2, 1, 2)
#     aa.set_title("User selection from MNIST")
#     aa.imshow(IPU_input)
#
#     # plt.suptitle('Heatmap of Cortical area Neuronal Fire count', fontsize=12)
#
#     # plt.pause(10)
#     # plt.show()
#     pylab.plt.draw()
#     pylab.plt.pause(runtime_data.parameters["Timers"]["burst_timer"])
#     return


def cortical_heatmap(IPU_input, cortical_areas):
    """
    Create a 2D heatmap for the requested Cortical area based on the level of Neuronal activity
    :param cortical_area:
    :return:
    """
    # if not settings.Switches.vis_init_status:
    #     settings.vis_init()
    pylab.plt.ion()

    cortical_arrays = []
    cortical_arrays.append(["IPU_Vision", IPU_input])
    # for cortical_area in runtime_data.cortical_areas:
    #     runtime_data.genome = runtime_data.genome
    #     x1 = runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][0]
    #     x2 = runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["x"][1]
    #     y1 = runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][0]
    #     y2 = runtime_data.genome['blueprint'][cortical_area]["neuron_params"]["geometric_boundaries"]["y"][1]
    #
    #     # Convert Cortical data to a numpy array
    #     data = runtime_data.brain[cortical_area]
    #     cortical_array = np.zeros((x2-x1, y2-y1))
    #     for key in data:
    #         xx = data[key]['location'][0]
    #         yy = data[key]['location'][1]
    #         cortical_array[xx, yy] = data[key]['cumulative_fire_count_inst']
    #     cortical_arrays.append([cortical_area, cortical_array])

    # print(cortical_arrays)
    # print(cortical_arrays[0][1])

    fig2 = pylab.plt.figure(num=None, figsize=(8, 8), dpi=28, facecolor='w', edgecolor='k')

    mpl.pylab.thismanager = mpl.pylab.get_current_fig_manager()
    mpl.pylab.thismanager.window.wm_geometry("+20+300")

    for i in range(1, len(runtime_data.cortical_areas)+2):
        aa = fig2.add_subplot(1, len(runtime_data.cortical_areas)+1, i)
        aa.set_title(cortical_arrays[i-1][0])
        aa.imshow(cortical_arrays[i-1][1])

    pylab.plt.suptitle('Heatmap of Cortical area Neuronal Fire count', fontsize=12)

    # plt.pause(10)
    pylab.plt.show()
    return


def main():
    vis_init()
    init_figures()
    burst_visualization_manager()


if __name__ == '__main__':
    vis_init()
    init_figures()
    burst_visualization_manager()
