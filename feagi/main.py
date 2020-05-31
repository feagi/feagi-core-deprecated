# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>

"""
This file contains the main Brain control code
"""

__author__ = 'Mohammad Nadji-Tehrani'


if __name__ == '__main__':
    from datetime import datetime
    from art import text2art
    from shutil import copyfile
    import sys
    import os

    print(text2art("FEAGI", font='block'))

    from misc import disk_ops
    disk_ops.load_parameters_in_memory()

    from configuration import runtime_data, settings

    try:
        connectome_file_path = sys.argv[1]
        if connectome_file_path:
            runtime_data.parameters["InitData"]["connectome_path"] = connectome_file_path
            print("Connectome path is:", connectome_file_path)
    except IndexError or NameError:
        print("Default connectome path has been selected")

    global connectome_path
    connectome_path = runtime_data.parameters["InitData"]["connectome_path"]

    def initialize_connectome():
        if not os.path.exists(connectome_path):
            os.makedirs(connectome_path)
            copyfile(runtime_data.parameters["InitData"]["static_genome_path"], connectome_path)

    initialize_connectome()

    # The following stages the genome in the proper connectome path and loads it into the memory
    disk_ops.genome_handler(connectome_path)

    # Initialize runtime cortical list
    blueprint = runtime_data.genome["blueprint"]
    cortical_list = []
    for key in blueprint:
        cortical_list.append(key)
    runtime_data.cortical_list = cortical_list
    from misc import brain_functions, neuron_functions_auto
    from evolutionary.brain_gen import brain_gen
    from evolutionary.architect import event_id_gen

    b = brain_functions.Brain()

    def initialize_the_brain():
        # # Initialize Fire Candidate List (FCL)
        FCL = []

        # Setting up Brain queue for multiprocessing
        brain_data = disk_ops.load_brain_in_memory()
        runtime_data.brain = brain_data

        block_dic_data = disk_ops.load_block_dic_in_memory()

        runtime_data.activity_stats = {}

        # Setting up genome data
        genome_stats = {}
        genome_stats["test_stats"] = []
        genome_test_stats = []

    if runtime_data.parameters["InitData"]["regenerate_brain"]:
        structural_fitness = 0
        while structural_fitness < 1:
            brain_generation_start_time = datetime.now()

            structural_fitness = brain_gen()
            print(">>****2", runtime_data.parameters['Switches']['use_static_genome'])
            brain_generation_duration = datetime.now() - brain_generation_start_time

        # todo: Move the following to stats module
        print("--------------------------------------------------------------")
        print("Brain generation lasted %s " % brain_generation_duration)
        print("--------------------------------------------------------------")
        print("Total Neuron count in Connectome is: ", b.connectome_neuron_count())
        print("--------------------------------------------------------------")
        print("Total Synapse count in Connectome is: ", b.connectome_synapse_count())
        print("--------------------------------------------------------------")
    initialize_the_brain()

    print("The burst engine has been started...")

    runtime_data.event_id = event_id_gen()
    print(" <> ^^ <> ^^ <> ^^ <> ^^ <> An event related to mnist reading with following id has been logged:", runtime_data.event_id)

    while 1==1:
        runtime_data.parameters["Switches"]["ready_to_exit_burst"] = False
        runtime_data.genome_test_stats = []
        neuron_functions_auto.burst()

        disk_ops.save_block_dic_to_disk(block_dic=runtime_data.block_dic,
                                        parameters=runtime_data.parameters, backup=True)

        disk_ops.save_brain_to_disk(brain=runtime_data.brain, parameters=runtime_data.parameters, backup=True)

        print("genome id called from main function: ", runtime_data.genome_id)
        disk_ops.save_genome_to_disk()
        if runtime_data.parameters["Switches"]["live_mode"] and not \
                runtime_data.parameters["Switches"]["one_round"]:
            runtime_data.parameters["Input"]["user_input"] = ""
            print("Starting a new generation...")
            # Regenerate the brain
            disk_ops.genome_handler(connectome_path)
            # disk_ops.stage_genome(connectome_path)
            # print("$")
            # disk_ops.load_genome_in_memory(connectome_path)
            # print("$$")
            structural_fitness = 0
            while structural_fitness < 1:
                brain_generation_start_time = datetime.now()
                print("$$$")
                runtime_data.block_dic = {}
                runtime_data.activity_stats = {}
                structural_fitness = brain_gen()
                print("$$$$")
                brain_generation_duration = datetime.now() - brain_generation_start_time
            initialize_the_brain()

            runtime_data.event_id = event_id_gen()

            print(
                " <> ^^ <> ^^ <> ^^ <> ^^ <> An event related to mnist reading with following id has been logged:",
                runtime_data.event_id)



#          <<<<<<<   T O   D O   L I S T   >>>>>>>>
# todo: Implement localized gene modification and localized fitness scores associated with various genome sections
        """
        This change can enable brain structure to carry its own fitness and neuron model a separate one
        """
# todo: Figure the fire power of each neuron and how to balance it
# todo: Find a way to cap different processes to not go out of hand
# todo: 0. Run with multiple variation of each number
# todo: 1. Run the system with a single genome and assess the deviation between fitness results
# todo: 2. Run the same genome with different exposure variables
# todo: Move more items to genome

# Performance
# todo: Cython adoption
# todo: proper use of multiprocessing
# todo: GPU support

# Scale-out
# todo: availability of accessing genome on a remote machine
# todo: Explore services like Digital ocean, AWS, Spark, etc.

# Key problem on hand
# todo: memory formation is not spread across the whole memory space
# todo: only when the right portion of cell assembly is activated the rest should become active
# todo: One number's visual memory is resembling all others
# todo: Neuron finder is too inefficient
# todo: Need a self tuning mechanism
# todo: find a way to measure layer level effectiveness metrics so it can be used for evolution

# Problems to fix
# todo: Synaptic activities in Memory eventually get to a point that does not ramp down
# todo: Event queue and events in general are not being used for any application or stored anywhere
# todo: Brain is being loaded in memory too regularly

# General Architecture - Anatomy
# todo: Add a generation age calculation to the main function
# todo: Consider Headache and Sleep needs
# todo: Move Rules to Genome
# todo: Consider Synaptic capacity as a property of each neuron
# todo: Account for Neuron morphology as a Neuron property
# todo: Dynamic synaptic capacity when system is shaping vs its established
# todo: Accounting for Synaptic rearrangement
# todo: Fine tune Genome to produce distinguishable results as Neurons fire
# todo: Define streams containing a chain of cortical areas for various functions such as vision, hearing, etc.
# todo: find a way to speed up brain building when synapse creation is not needed e.g. memory, utf8
# todo: Synapse creation takes a very long time in presence of large neurons. Think of a way to limit the scope. zipcode
# todo: Build a cost function to measure the effectiveness and quality of relative synapse count in each layer

# Input handling
# todo: Use directional kernel analysis data as part of input data
# todo: Update IPU module to include combination of multiple input types e.g. brightness, edges, etc.
# todo: Perform edge detection on the images from MNIST and feed them to network (OpenCL or other methods)
# todo: Figure how to Associate ASCii characters with neuronal readouts
# todo: Need to figure how the Direction sensitive neurons in brain function
# todo: Need to design a neuronal system that can receive an input and its output be a combination of matching objects

# Neuron functions - Physiology
# todo: Let all the Neuron times be a factor of average Burst duration instead of fix number
# todo: Create the pruner function
# todo: Synaptic_strenght currently growing out of bound. Need to impose limits
# todo: Handle burst scenarios where the input neuron does not have any neighbor neuron associated with
# todo: To account for LTD or Long Term Synaptic Depression
# todo: Update the algorithm responsible to improving the synapse strength to consider simultaneous firing of others
# todo: Figure how to pass the Brain Physiology to Genome as well. Currently Genome drives Brain Anatomy only.
# todo: Need to imp. a looped structure to account for connecting events happening within a time delay of each-other
# todo: Ability to detect the dominant direction before higher level processing

# Genetic Evolution
# todo: capture phenotype(connectome) highlights in database
# todo: regenerative model.
# todo: Consideration for how to evolve the network over generations. Update Genome based on some constraints
# todo: What could trigger evolution of a cortical area?
# todo: Consider a method to reward or punish neuron so it can evolve
# todo: Build a Genome Generator
# todo: Change evolutionary phase to evaluation check-point

# Multi processing
# todo: Look into  GPU leverage
# todo: Main function is running with every process along with all the initializations. This needs optimization

# Analysis
# todo: Come up with a way to analyze and categorize output data
# todo: Add ability to show activity percentage for each cortical area

# Memory
# todo: Think of how to implement an alternative path so when an object is seen by visual it can be labeled “trained”
# using alternate path.
#     1. In this case training the network is equal to exposing Network to two simultaneous events at the same time.
#  The simultaneous occurrence would trigger a binding between Neurons in the Memory Module
# todo: Figure how Memory Module should be configured so it can behave as explained above
# todo: Configure an output module so after Memory module is activated the activation can be read back.
# todo: How to get output from memory ??? How to comprehend it ????

# Visualization
# todo: Fix issue where some cortical activities are not showing up    <<<  NEXT !!!!!
# todo: Histogram of memory region activities when a single alphabet is trained

# Vision
# todo: Print visual memory to output in the form of pixels

# Speech
# todo: Make it learn to speak!

# Auto training
# todo: Compare results if you randomly show different variation of the same number vs one at a time



