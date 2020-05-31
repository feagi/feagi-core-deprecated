# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
"""
This Library contains various functions simulating human cortical behaviors
Function list:
neuron:           This function is triggered as a Neuron instance and stays up for period of time
                  till Neuron is fired
neuron_prop:      Returns the properties for a given neuron
neuron_neighbors: Reruns the list of neighbors for a given neuron
"""
import os
import glob
import pickle
import json
import csv
from datetime import datetime
from collections import deque
from time import sleep
from PUs import OPU_utf8, IPU_utf8
from . import brain_functions
from misc import disk_ops
from misc import db_handler, stats
from configuration import settings, runtime_data
from PUs.IPU_vision import MNIST
from evolutionary.architect import test_id_gen, run_id_gen, synapse
from cython_libs import neuron_functions_cy as cy
from art import text2art


print(settings.Bcolors.YELLOW + "Module loaded: neuron_functions_auto" + settings.Bcolors.ENDC)


def candidate_list_counter(candidate_list):
    count = 0
    for cortical_area in candidate_list:
        count += len(candidate_list[cortical_area])
        # print("&&$$%%>>", cortical_area, len(candidate_list[cortical_area]))
    return count


def burst():
    """This function behaves as instance of Neuronal activities"""
    print("\n\n\n\n\n")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("**** **** **** **** ****       Starting the burst engine...      **** **** **** **** ****")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("**** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** **** ****")
    print("\n\n\n\n\n")

    print(runtime_data.parameters['Switches']['use_static_genome'])
    disk_ops.genome_handler(runtime_data.parameters['InitData']['connectome_path'])

    # todo: Move comprehension span to genome that is currently in parameters
    comprehension_span = runtime_data.parameters["InitData"]["comprehension_span"]
    
    # Initializing the comprehension queue
    comprehension_queue = deque(['-'] * comprehension_span)

    runtime_data.parameters["Auto_injector"]["injector_status"] = False
    runtime_data.termination_flag = False
    runtime_data.top_10_utf_memory_neurons = list_top_n_utf_memory_neurons("utf8_memory", 10)
    runtime_data.top_10_utf_neurons = list_top_n_utf_memory_neurons("utf8", 10)

    runtime_data.v1_members = []
    for item in runtime_data.cortical_list:
        if runtime_data.genome['blueprint'][item]['sub_group_id'] == "vision_v1":
            runtime_data.v1_members.append(item)

    injector = Injector()
    mongo = db_handler.MongoManagement()
    influxdb = db_handler.InfluxManagement()

    if not runtime_data.brain_is_running:
        toggle_brain_status()
        runtime_data.brain_run_id = run_id_gen()
        if runtime_data.parameters["Switches"]["capture_brain_activities"]:
            print(settings.Bcolors.HEADER + " *** Warning!!! *** Brain activities are being recorded!!" +
                  settings.Bcolors.ENDC)

    runtime_data.event_id = runtime_data.event_id

    print('runtime_data.genome_id = ', runtime_data.genome_id)
    cortical_list = []

    for cortical_area in runtime_data.genome['blueprint']:
        cortical_list.append(cortical_area)
        runtime_data.fire_candidate_list[cortical_area] = set()
        runtime_data.future_fcl[cortical_area] = set()
        runtime_data.previous_fcl[cortical_area] = set()
        runtime_data.upstream_neurons[cortical_area] = {}

    runtime_data.cortical_list = cortical_list
    runtime_data.memory_list = cortical_group_members('Memory')
    print("Memory list is: ", runtime_data.memory_list)

    verbose = runtime_data.parameters["Switches"]["verbose"]

    if runtime_data.parameters["Switches"]["capture_brain_activities"]:
        runtime_data.fcl_history = {}

    if runtime_data.parameters["Switches"]["capture_neuron_mp"]:
        with open(runtime_data.parameters['InitData']['connectome_path'] + '/neuron_mp.csv', 'w') as neuron_mp_file:
            neuron_mp_writer = csv.writer(neuron_mp_file, delimiter=',')
            neuron_mp_writer.writerow(('burst_number', 'cortical_layer', 'neuron_id', 'membrane_potential'))

    print("** ** ** Live mode, live mode status: ",
          runtime_data.parameters["Switches"]["live_mode"],
          runtime_data.live_mode_status)

    # Live mode condition
    if runtime_data.parameters["Switches"]["live_mode"] and runtime_data.live_mode_status == 'idle':
        runtime_data.live_mode_status = 'learning'
        print(
            settings.Bcolors.RED + "Starting an automated learning process...<> <> <> <>" + settings.Bcolors.ENDC)
        injector.injection_manager(injection_mode="l1", injection_param="")

    print("\n\n >> >> >> Ready to exist burst engine flag:", runtime_data.parameters["Switches"]["ready_to_exit_burst"])

    connectome_path = runtime_data.parameters['InitData']['connectome_path']
    while not runtime_data.parameters["Switches"]["ready_to_exit_burst"]:
        if runtime_data.parameters["Switches"]["influx_stat_logger"]:
            influxdb.insert_burst_checkpoints(connectome_path, runtime_data.burst_count)
        burst_start_time = datetime.now()
        runtime_data.pain_flag = False
        now = datetime.now()

        # print(datetime.now(), "Burst count = ", runtime_data.burst_count, file=open("./logs/burst.log", "a"))

        for cortical_area in runtime_data.fire_candidate_list:
            runtime_data.previous_fcl[cortical_area] = \
                set([item for item in runtime_data.fire_candidate_list[cortical_area]])

        runtime_data.burst_count += 1

        # logging neuron activities to the influxdb
        if runtime_data.parameters["Switches"]["influx_stat_logger"]:
            connectome_path = runtime_data.parameters['InitData']['connectome_path']
            for cortical_area in runtime_data.fire_candidate_list:
                for neuron in runtime_data.fire_candidate_list[cortical_area]:
                    influxdb.insert_neuron_activity(connectome_path=connectome_path,
                                                    cortical_area=cortical_area,
                                                    neuron_id=neuron,
                                                    membrane_potential=
                                                    runtime_data.brain[cortical_area][neuron]["membrane_potential"]/1)

        # Fire all neurons within fire_candidate_list (FCL) or add a delay if FCL is empty
        # time_firing_activities = datetime.now()
        # todo: replace the hardcoded vision memory statement
        if candidate_list_counter(runtime_data.fire_candidate_list) == \
                0 and not runtime_data.parameters["Auto_injector"]["injector_status"]:
            sleep(runtime_data.parameters["Timers"]["idle_burst_timer"])
            runtime_data.empty_fcl_counter += 1
            print("FCL is empty!")
        else:
            # Capture cortical activity stats
            for cortical_area in runtime_data.fire_candidate_list:
                if cortical_area in runtime_data.activity_stats:
                    cortical_neuron_count = len(runtime_data.fire_candidate_list[cortical_area])
                    runtime_data.activity_stats[cortical_area] = max(runtime_data.activity_stats[cortical_area],
                                                                     cortical_neuron_count)

                    if runtime_data.parameters["Switches"]["influx_stat_logger"]:
                        influxdb.insert_burst_activity(connectome_path=connectome_path,
                                                       burst_id=runtime_data.burst_count,
                                                       cortical_area=cortical_area,
                                                       neuron_count=cortical_neuron_count)

                    if runtime_data.parameters["Switches"]["global_logger"] and \
                            runtime_data.parameters["Logs"]["print_cortical_activity_counters"] and \
                            runtime_data.parameters["Auto_injector"]["injector_status"]:
                        print(settings.Bcolors.YELLOW + '    %s : %i  '
                              % (cortical_area, cortical_neuron_count)
                              + settings.Bcolors.ENDC)
                    if runtime_data.parameters["Switches"]["global_logger"] and \
                            runtime_data.parameters["Logs"]["print_cortical_activity_counters"] and \
                            runtime_data.parameters["Auto_tester"]["tester_status"]:
                        print(settings.Bcolors.OKGREEN + '    %s : %i  '
                              % (cortical_area, cortical_neuron_count)
                              + settings.Bcolors.ENDC)

                else:
                    runtime_data.activity_stats[cortical_area] = len(runtime_data.fire_candidate_list[cortical_area])

            # todo: Look into multi-threading for Neuron neuron_fire and wire_neurons function
            # Firing all neurons in the Fire Candidate List
            # Fire all neurons in FCL
            time_actual_firing_activities = datetime.now()
            # now = datetime.now()
            # runtime_data.time_neuron_update = datetime.now() - now
            # runtime_data.plasticity_time_total = datetime.now() - datetime.now()
            # runtime_data.plasticity_time_total_p1 = datetime.now() - datetime.now()
            # stats_utf_memory_membrane_potentials()
            # Firing all neurons in the fire_candidate_list
            for cortical_area in runtime_data.fire_candidate_list:
                while runtime_data.fire_candidate_list[cortical_area]:
                    neuron_to_fire = runtime_data.fire_candidate_list[cortical_area].pop()
                    neuron_fire(cortical_area, neuron_to_fire)
            # stats_utf_memory_membrane_potentials()
            # pfcl_total_neuron_count = candidate_list_counter(runtime_data.previous_fcl)
            # cfcl_total_neuron_count = candidate_list_counter(runtime_data.fire_candidate_list)

            # print("PFCL:", pfcl_total_neuron_count,
            #       "\nCFCL:", cfcl_total_neuron_count,
            #       "\nFFCL:", candidate_list_counter(runtime_data.future_fcl))

            # Transferring future_fcl to current one and resetting the future one in process
            for cortical_area in runtime_data.future_fcl:
                runtime_data.fire_candidate_list[cortical_area] = \
                    set([item for item in runtime_data.future_fcl[cortical_area]])
                runtime_data.future_fcl[cortical_area] = set()

            # try:
            #     print("Timing : .__________ Firing ops...........:",
            #           (datetime.now() - time_actual_firing_activities - runtime_data.time_neuron_update) /
            #           pfcl_total_neuron_count)
            #     print("Timing : |___________Neuron updates.......:",
            #           runtime_data.time_neuron_update / pfcl_total_neuron_count)
            #     print("Timing :             |__Ext plasticity....:",
            #           runtime_data.plasticity_time_total / pfcl_total_neuron_count)
            #     print("Timing :                |___Ext plast. P1.:",
            #           runtime_data.plasticity_time_total_p1 / pfcl_total_neuron_count)
            #
            #     print("\nTiming : Average time per fire ....................:",
            #           (datetime.now() - time_firing_activities) /
            #           pfcl_total_neuron_count)
            #     print("\nTiming : Total firing time per FCL.................:", datetime.now() - time_firing_activities)
            #
            # except ZeroDivisionError:
            #     pass

            if verbose:
                print(settings.Bcolors.YELLOW + 'Current fire_candidate_list is %s'
                      % runtime_data.fire_candidate_list + settings.Bcolors.ENDC)

            # print_cortical_neuron_mappings('vision_memory', 'utf8_memory')

        # todo: need to break down the training function into pieces with one feeding a stream of data
        # Auto-inject if applicable
        if runtime_data.parameters["Auto_injector"]["injector_status"]:
            # injection_time = datetime.now()
            # print("-------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ auto_injector")
            injector.auto_injector()
            # print("Timing : Injection:", datetime.now() - injection_time)

        # Auto-test if applicable
        if runtime_data.parameters["Auto_tester"]["tester_status"]:
            # test_time = datetime.now()
            injector.auto_tester()
            # print("Timing : Test:", datetime.now() - test_time)

        # todo: The following is to have a check point to assess the perf of the in-use genome and make on the fly adj.
        if runtime_data.burst_count % runtime_data.genome['evolution_burst_count'] == 0:
            print('Evolution phase reached...')
            for area in runtime_data.cortical_list:
                neuron_count, synapse_count = stats.connectome_total_synapse_cnt(area)
                if runtime_data.parameters["Switches"]["influx_stat_logger"]:
                    influxdb.insert_connectome_stats(connectome_path=connectome_path,
                                                     cortical_area=area,
                                                     neuron_count=neuron_count,
                                                     synapse_count=synapse_count)
            # genethesizer.generation_assessment()

        # Saving FCL to disk for post-processing and running analytics
        if runtime_data.parameters["Switches"]["save_fcl_to_db"]:
            disk_ops.save_fcl_in_db(runtime_data.burst_count,
                                    runtime_data.fire_candidate_list,
                                    injector.injector_num_to_inject)

        detected_char = utf_detection_logic(runtime_data.burst_detection_list)
        comprehension_queue.append(detected_char)
        comprehension_queue.popleft()

        def training_quality_test():
            upstream_general_stats_ = list_upstream_neuron_count_for_digits()
            for entry in upstream_general_stats_:
                if entry[1] == 0:
                    print(upstream_general_stats_, "This entry was zero >", entry)
                    return False

        # Monitor cortical activity levels and terminate brain if not meeting expectations
        # time_monitoring_cortical_activity = datetime.now()
        if runtime_data.parameters["Switches"]["evaluation_based_termination"]:
            if runtime_data.parameters["Auto_injector"]["injector_status"] and \
                    runtime_data.burst_count > runtime_data.parameters["InitData"]["kill_trigger_burst_count"]:
                if 'vision_memory' not in runtime_data.activity_stats:
                    runtime_data.activity_stats['vision_memory'] = 0
                elif runtime_data.activity_stats['vision_memory'] < \
                        runtime_data.parameters["InitData"]["kill_trigger_vision_memory_min"]:
                    print(settings.Bcolors.RED +
                          "\n\n\n\n\n\n!!!!! !! !Terminating the brain due to low performance! !! !!!" +
                          settings.Bcolors.ENDC)
                    print("vision_memory max activation was:", runtime_data.activity_stats['vision_memory'])
                    runtime_data.termination_flag = True
                    burst_exit_process()

        # print("Timing : Monitoring cortical activity:", datetime.now()-time_monitoring_cortical_activity)

        # Pain check
        if runtime_data.pain_flag:
            exhibit_pain()

        # Comprehension check
        # time_comprehension_check = datetime.now()
        counter_list = {}
        print("~~~~~~..... Burst detection list: ", runtime_data.burst_detection_list)
        if runtime_data.parameters["Logs"]["print_comprehension_queue"]:
            if runtime_data.burst_detection_list != {}:
                print(settings.Bcolors.RED + "<><><><><><><><><><><><><><>"
                                             "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"
                      + settings.Bcolors.ENDC)
            print(">>comprehension_queue  ", comprehension_queue, "  <<")

        for item in comprehension_queue:
            if item in counter_list:
                counter_list[item] += 1
            else:
                counter_list[item] = 1
        list_length = len(counter_list)

        if runtime_data.parameters["Logs"]["print_comprehension_queue"]:
            print("+++++++This is the counter list", counter_list)
        for item in counter_list:
            if list_length == 1 and item != '-':
                runtime_data.parameters["Input"]["comprehended_char"] = item[0]
                print(settings.Bcolors.HEADER + "UTF8 out was stimulated with the following character: <<< %s >>>"
                      % runtime_data.parameters["Input"]["comprehended_char"] + settings.Bcolors.ENDC)
                # In the event that the comprehended UTF character is not matching the injected one pain is triggered
                if runtime_data.parameters["Input"]["comprehended_char"] != str(runtime_data.labeled_image[1]):
                    trigger_pain()
                    runtime_data.pain_flag = True
            else:
                if list_length >= 2:
                    runtime_data.parameters["Input"]["comprehended_char"] = ''

        # Forming memories through creation of cell assemblies
        if runtime_data.parameters["Switches"]["memory_formation"]:
            # memory_formation_start_time = datetime.now()
            # todo: instead of passing a pain flag simply detect of pain neuron is activated
            form_memories(runtime_data.fire_candidate_list, runtime_data.pain_flag)
            # print("    Memory formation took--",datetime.now()-memory_formation_start_time)
        # print("Timing : Comprehension check:", datetime.now() - time_comprehension_check)

        # Burst stats
        if runtime_data.parameters["Logs"]["print_burst_stats"]:
            for area in runtime_data.brain:
                print("### Average postSynaptic current in --- %s --- was: %i"
                      % (area, average_postsynaptic_current(area)))

        if runtime_data.parameters["Logs"]["print_upstream_neuron_stats"]:
            # Listing the number of neurons activating each UTF memory neuron
            upstream_report_time = datetime.now()
            upstream_general_stats, upstream_fcl_stats = \
                list_upstream_neuron_count_for_digits(mode=1)
            print("list_upstream_neuron_count_for_digits:", upstream_general_stats)
            print("list_upstream___FCL__count_for_digits:", upstream_fcl_stats)

            print("Timing : Upstream + common neuron report:", datetime.now() - upstream_report_time)

        if runtime_data.parameters["Logs"]["print_common_neuron_report"]:
            # todo: investigate the efficiency of the common neuron report
            print("The following is the common neuron report:")
            common_neuron_report()

        # Resetting burst detection list
        runtime_data.burst_detection_list = {}

        # todo: *** Danger *** The following section could cause considerable memory expansion. Need to add limitations.
        # # Condition to save FCL data to disk
        # user_input_processing(user_input, user_input_param)
        # if runtime_data.parameters["Switches"]["capture_brain_activities"]:
        #     runtime_data.fcl_history[runtime_data.burst_count] = runtime_data.fire_candidate_list
        #
        # if runtime_data.parameters["Switches"]["save_fcl_to_disk"]:
        #     with open('./fcl_repo/fcl.json', 'w') as fcl_file:
        #         fcl_file.write(json.dumps(runtime_data.fire_candidate_list))
        #         fcl_file.truncate()
        #     sleep(0.5)

        # todo: This is the part to capture the neuron membrane potential values in a file, still need to figure how
        if runtime_data.parameters["Switches"]["capture_neuron_mp"]:
            with open(runtime_data.parameters['InitData']['connectome_path'] + '/neuron_mp.csv', 'a') as neuron_mp_file:
                neuron_mp_writer = csv.writer(neuron_mp_file,  delimiter=',')
                new_data = []
                for cortical_area in runtime_data.fire_candidate_list:
                    for neuron in runtime_data.fire_candidate_list[cortical_area]:
                        new_content = (runtime_data.burst_count, cortical_area, neuron,
                                       runtime_data.brain[cortical_area][neuron]["membrane_potential"])
                        new_data.append(new_content)
                neuron_mp_writer.writerows(new_data)

        if runtime_data.parameters["Switches"]["capture_neuron_mp_db"]:
            new_data = []
            for cortical_area in runtime_data.fire_candidate_list:
                for neuron in runtime_data.fire_candidate_list[cortical_area]:
                    new_content = (runtime_data.burst_count, cortical_area, neuron,
                                   runtime_data.brain[cortical_area][neuron]["membrane_potential"])
                    new_data.append(new_content)
                    mongo.inset_membrane_potentials(new_content)

        # Prune all prune candidate synapses
        pruning_start_time = datetime.now()
        prune_all_candidates()
        print("Timing : Pruning:", datetime.now() - pruning_start_time)

        burst_duration = datetime.now() - burst_start_time
        if runtime_data.parameters["Logs"]["print_burst_info"]:
            print(settings.Bcolors.YELLOW +
                  ">>> Burst duration: %s %i --- ---- ---- ---- ---- ---- ----"
                  % (burst_duration, runtime_data.burst_count) + settings.Bcolors.ENDC)


def utf_detection_logic(detection_list):
    # todo: Add a logic to account for cases were two top ranked items are too close
    # Identifies the detected UTF character with highest activity
    highest_ranked_item = '-'
    second_highest_ranked_item = '-'
    for item in detection_list:
        if highest_ranked_item == '-':
            highest_ranked_item = item
        else:
            if detection_list[item]['rank'] > detection_list[highest_ranked_item]['rank']:
                second_highest_ranked_item = highest_ranked_item
                highest_ranked_item = item
            elif second_highest_ranked_item == '-':
                second_highest_ranked_item = item
            else:
                if detection_list[item]['rank'] > detection_list[second_highest_ranked_item]['rank']:
                    second_highest_ranked_item = item

    # todo: export detection factor to genome not parameters
    detection_tolerance = 1.5
    if highest_ranked_item != '-' and second_highest_ranked_item == '-':
        print("Highest ranking number was chosen.")
        print("1st and 2nd highest ranked numbers are: ", highest_ranked_item, second_highest_ranked_item)
        return highest_ranked_item
    elif highest_ranked_item != '-' and second_highest_ranked_item != '-':
        if detection_list[highest_ranked_item]['rank'] / detection_list[second_highest_ranked_item]['rank'] > \
                detection_tolerance:
            print("Highest ranking number was chosen.")
            print("1st and 2nd highest ranked numbers are: ", highest_ranked_item, second_highest_ranked_item)
            return highest_ranked_item
        else:
            print(">>>> >>> >> >> >> >> > > Tolerance factor was not met!! !! !!")
            print("Highest and 2nd highest ranked numbers are: ", highest_ranked_item, second_highest_ranked_item)
            return '-'
    else:
        return '-'

    # list_length = len(detection_list)
    # if list_length == 1:
    #     for key in detection_list:
    #         return key
    # elif list_length >= 2 or list_length == 0:
    #     return '-'
    # else:
    #     temp = []
    #     counter = 0
    #     # print(">><<>><<>><<", detection_list)
    #     for key in detection_list:
    #         temp[counter] = (key, detection_list[key])
    #     if temp[0][1] > (3 * temp[1][1]):
    #         return temp[0][0]
    #     elif temp[1][1] > (3 * temp[0][1]):
    #         return temp[1][0]
    #     else:
    #         return '-'

    # Load copy of all MNIST training images into mnist_data in form of an iterator. Each object has image label + image


class Injector:

    def __init__(self):
        self.injector_img_flag = False
        self.injector_utf_flag = False
        self.injector_injection_has_begun = False
        self.injector_variation_handler = True
        self.injector_exposure_handler = True
        self.injector_utf_handler = True
        self.injector_variation_counter = runtime_data.parameters["Auto_injector"]["variation_default"]
        self.injector_exposure_default = runtime_data.parameters["Auto_injector"]["exposure_default"]
        runtime_data.exposure_counter_actual = self.injector_exposure_default
        self.injector_utf_default = runtime_data.parameters["Auto_injector"]["utf_default"]
        self.injector_utf_counter_actual = self.injector_utf_default
        self.injector_injection_start_time = datetime.now()
        self.injector_num_to_inject = ''
        self.injector_utf_to_inject = ''
        self.injector_injection_mode = ''
        self.injector_exit_flag = False
        self.injector_burst_skip_flag = False
        self.injector_burst_skip_counter = 0

        self.tester_img_flag = False
        self.tester_utf_flag = False
        self.tester_testing_has_begun = False
        self.tester_variation_handler = True
        self.tester_exposure_handler = True
        self.tester_utf_handler = True
        self.tester_variation_counter = runtime_data.parameters["Auto_tester"]["variation_default"]
        self.tester_exposure_default = runtime_data.parameters["Auto_tester"]["exposure_default"]
        self.tester_utf_default = runtime_data.parameters["Auto_tester"]["utf_default"]
        self.tester_utf_counter_actual = self.tester_utf_default
        self.tester_test_start_time = datetime.now()
        self.tester_num_to_inject = ''
        self.tester_test_mode = ''
        self.tester_comprehension_counter = 0
        self.tester_test_attempt_counter = 0
        self.tester_no_response_counter = 0
        # self.tester_temp_stats = []
        self.tester_test_id = ""
        self.tester_exit_flag = False
        self.tester_burst_skip_flag = False
        self.tester_burst_skip_counter = 0
        print("-------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Injector init")
        self.mnist = MNIST()
        print("*** *** ***\n\n\n*** *AA BB CC ** ***\n\n\n*** *** ***")

    def utf8_feeder(self):
        
        # inject label to FCL

        runtime_data.training_neuron_list_utf = set()

        if self.injector_injection_mode == 'c':
            runtime_data.training_neuron_list_utf = \
                IPU_utf8.convert_char_to_fire_list(self.injector_utf_to_inject)
        else:
            runtime_data.training_neuron_list_utf = \
                IPU_utf8.convert_char_to_fire_list(str(runtime_data.labeled_image[1]))
            print("!!! Image label: ", runtime_data.labeled_image[1])

        runtime_data.fire_candidate_list['utf8'].update(runtime_data.training_neuron_list_utf)

    @staticmethod
    def img_neuron_list_feeder():
        
        # inject neuron activity to FCL
        for cortical_area in runtime_data.v1_members:
            if runtime_data.training_neuron_list_img[cortical_area]:
                # print("Before FCL injection:", candidate_list_counter(runtime_data.fire_candidate_list),
                # len(runtime_data.training_neuron_list_img[cortical_area]))
                runtime_data.fire_candidate_list[cortical_area].\
                    update(runtime_data.training_neuron_list_img[cortical_area])
                # print("After FCL injection:", candidate_list_counter(runtime_data.fire_candidate_list))

    @staticmethod
    def image_feeder2(num, seq, mnist_type):
        
        brain = brain_functions.Brain()
        runtime_data.labeled_image = ['', num]

        # runtime_data.training_neuron_list_img = brain.retina(runtime_data.labeled_image)
        runtime_data.training_neuron_list_img = brain.retina2(num=num,
                                                              seq=seq,
                                                              mnist_type=mnist_type,
                                                              random_num=False)

    def injection_manager(self, injection_mode, injection_param):
        """
        This function has three modes l1, l2, r and c.
        Mode l1: Assist in learning numbers from 0 to 9
        Mode l2: Assist in learning variations of the same number
        Mode r: Assist in exposing a single image to the brain for a number of bursts
        Mode c: Assist in exposing a single utf8 char to the brain for a number of bursts
        """
        print("\nInjection Manager...")
        try:
            if injection_mode == 'l1':
                self.injector_injection_mode = "l1"
                print("Automatic learning for 0..9 has been turned ON!")
                self.injector_img_flag = True
                self.injector_utf_flag = True
                self.injector_exit_flag = False
                self.injector_burst_skip_flag = False
                self.injector_utf_handler = True
                self.injector_variation_handler = True
                # self.injector_exposure_counter_actual = runtime_data.parameters["Auto_injector"]["exposure_default"]
                self.injector_variation_counter = runtime_data.parameters["Auto_injector"]["variation_default"]
                runtime_data.variation_counter_actual = runtime_data.parameters["Auto_injector"]["variation_default"]
                self.injector_utf_default = runtime_data.parameters["Auto_injector"]["utf_default"]
                self.injector_utf_counter_actual = runtime_data.parameters["Auto_injector"]["utf_default"]
                self.injector_num_to_inject = self.injector_utf_default
                self.injector_burst_skip_counter = \
                    runtime_data.parameters["Auto_injector"]["injector_burst_skip_counter"]

            elif injection_mode == 'l2':
                self.injector_injection_mode = "l2"
                self.injector_img_flag = True
                self.injector_utf_flag = True
                self.injector_burst_skip_flag = False
                self.injector_utf_handler = False
                self.injector_variation_handler = True
                self.injector_variation_counter = runtime_data.parameters["Auto_injector"]["variation_default"]
                runtime_data.variation_counter_actual = runtime_data.parameters["Auto_injector"]["variation_default"]
                self.injector_utf_default = 1
                self.injector_utf_counter_actual = 1
                self.injector_num_to_inject = int(injection_param)
                self.injector_burst_skip_counter = \
                    runtime_data.parameters["Auto_injector"]["injector_burst_skip_counter"]
                print("   <<<   Automatic learning for variations of number << %s >> has been turned ON!   >>>"
                      % injection_param)

            elif injection_mode == 'r':
                self.injector_injection_mode = "r"
                self.injector_variation_handler = False
                self.injector_img_flag = True
                self.injector_utf_flag = False
                self.injector_burst_skip_flag = False
                self.injector_variation_counter = 0
                runtime_data.variation_counter_actual = 0
                self.injector_utf_default = -1
                self.injector_utf_counter_actual = -1
                self.injector_num_to_inject = injection_param

            elif injection_mode == 'c':
                self.injector_injection_mode = "c"
                self.injector_variation_handler = False
                self.injector_utf_handler = False
                self.injector_img_flag = False
                self.injector_utf_flag = True
                self.injector_burst_skip_flag = False
                self.injector_utf_to_inject = injection_param
                self.injector_variation_counter = 0
                runtime_data.variation_counter_actual = 0
                self.injector_utf_default = -1
                self.injector_utf_counter_actual = -1

            else:
                print("Error detecting the injection mode...")
                return

        finally:
            print("Injection Manager... Finally!")
            toggle_injection_mode()
            self.injector_injection_has_begun = True

    def auto_injector(self):
        
        if self.injector_injection_has_begun:
            # Beginning of a injection process
            print("----------------------------------------Data injection has begun-----------------------------------")
            self.injector_injection_has_begun = False
            self.injector_injection_start_time = datetime.now()
            self.image_feeder2(num=self.injector_num_to_inject,
                               seq=runtime_data.variation_counter_actual,
                               mnist_type='training')

        # Mechanism to skip a number of bursts between each injections to clean-up FCL
        if not self.injector_burst_skip_flag:

            if self.injector_img_flag:
                self.img_neuron_list_feeder()
            if self.injector_utf_flag:
                self.utf8_feeder()

            # Exposure counter
            if not self.injector_burst_skip_flag:
                runtime_data.exposure_counter_actual -= 1

            print('  ----------------------------------------------------------------------------------------    ### ',
                  runtime_data.variation_counter_actual, self.injector_utf_counter_actual,
                  runtime_data.exposure_counter_actual, ' ###')

            # Check if exit condition has been met
            if self.injection_exit_condition() or runtime_data.variation_counter_actual < 1:
                self.injection_exit_process()

            # Counter logic
            if runtime_data.exposure_counter_actual < 1:

                # Effectiveness check
                if runtime_data.parameters["Switches"]["evaluation_based_termination"]:
                    upstream_neuron_count_for_digits = \
                        list_upstream_neuron_count_for_digits(digit=self.injector_utf_counter_actual)
                    print('## ## ###:', upstream_neuron_count_for_digits)
                    if upstream_neuron_count_for_digits[0][1] == 0:
                        print(settings.Bcolors.RED +
                              "\n\n\n\n\n\n!!!!! !! !Terminating the brain due to low training capability! !! !!!" +
                              settings.Bcolors.ENDC)
                        runtime_data.termination_flag = True
                        burst_exit_process()
                        self.injector_exit_flag = True

                if not self.injector_exit_flag:
                    # Resetting exposure counter
                    runtime_data.exposure_counter_actual = self.injector_exposure_default

                    # UTF counter
                    self.injector_utf_counter_actual -= 1

                    # Turning on the skip flag to allow FCL to clear
                    self.injector_burst_skip_flag = True

                    if self.injector_utf_counter_actual < 0:
                        # Resetting counters to their default value
                        self.injector_utf_counter_actual = self.injector_utf_default
                        # Variation counter
                        runtime_data.variation_counter_actual -= 1

                    self.injector_num_to_inject = max(self.injector_utf_counter_actual, 0)
                    runtime_data.flag_ready_to_inject_image = True

                    # Saving brain to disk
                    # todo: assess the impact of the following disk operation
                    if runtime_data.parameters["Switches"]["save_connectome_to_disk"]:
                        for cortical_area in runtime_data.cortical_list:
                            with open(runtime_data.parameters['InitData']['connectome_path'] +
                                      cortical_area + '.json', "r+") as data_file:
                                data = runtime_data.brain[cortical_area]
                                for _ in data:
                                    data[_]['activity_history'] = ""
                                data_file.seek(0)  # rewind
                                data_file.write(json.dumps(data, indent=3))
                                data_file.truncate()

        else:
            print("Skipping the injection for this round...")
            self.injector_burst_skip_counter -= 1
            if self.injector_burst_skip_counter <= 0 or candidate_list_counter(runtime_data.fire_candidate_list) < 1:
                self.injector_burst_skip_counter = runtime_data.parameters["Auto_injector"][
                    "injector_burst_skip_counter"]
                self.injector_burst_skip_flag = False

        if runtime_data.flag_ready_to_inject_image and not self.injector_burst_skip_flag:
            print("self.num_to_inject: ", self.injector_num_to_inject)
            self.image_feeder2(num=self.injector_num_to_inject,
                               seq=runtime_data.variation_counter_actual,
                               mnist_type='training')
            runtime_data.flag_ready_to_inject_image = False

    def injection_exit_condition(self):
        if (self.injector_utf_handler and
            self.injector_utf_counter_actual < 1 and
            runtime_data.variation_counter_actual < 1 and
            runtime_data.exposure_counter_actual < 1) or \
                (not self.injector_utf_handler and
                 self.injector_variation_handler and
                 runtime_data.variation_counter_actual < 1 and
                 runtime_data.exposure_counter_actual < 1) or \
                (not self.injector_utf_handler and
                 not self.injector_variation_handler and
                 runtime_data.exposure_counter_actual < 1):
            exit_condition = True
            print(">> Injection exit condition has been met <<")
        else:
            exit_condition = False
        return exit_condition

    def injection_exit_process(self):
        
        runtime_data.parameters["Auto_injector"]["injector_status"] = False
        self.injector_num_to_inject = ''
        runtime_data.exposure_counter_actual = runtime_data.parameters["Auto_injector"]["exposure_default"]
        runtime_data.variation_counter_actual = runtime_data.parameters["Auto_injector"]["variation_default"]
        self.injector_utf_counter_actual = runtime_data.parameters["Auto_injector"]["utf_default"]
        injection_duration = datetime.now() - self.injector_injection_start_time
        print("----------------------------All injection rounds has been completed-----------------------------")
        print("Total injection duration was: ", injection_duration)
        print("-----------------------------------------------------------------------------------------------")
        if runtime_data.parameters["Auto_injector"]["epochs"] == 0:
            if runtime_data.parameters["Switches"]["live_mode"] and \
                    runtime_data.live_mode_status == 'learning':
                runtime_data.live_mode_status = 'testing'
                print(settings.Bcolors.RED + "\n\n\n\n\n"
                                             "Starting automated testing process \n\n\n\n\nXXX XXX XXX XXX XXX\n\n\n\n"
                                             "-----------------------------------------------------------------\n"
                                             "-----------------------------------------------------------------" +
                      settings.Bcolors.ENDC)
                self.test_manager(test_mode="t1", test_param="")
        else:
            runtime_data.parameters["Auto_injector"]["epochs"] -= 1
            self.injection_manager(injection_mode="l1", injection_param="")
            print(text2art("EPOCH_" + str(runtime_data.parameters["Auto_injector"]["epochs"]), font='block'))

    def test_manager(self, test_mode, test_param):
        """
        This function has three modes t1, t2.
        Mode t1: Assist in learning numbers from 0 to 9
        Mode t2: Assist in learning variations of the same number
        """
        
        try:
            if test_mode == 't1':
                self.tester_test_mode = "t1"
                print("Automatic learning for 0..9 has been turned ON!")
                self.tester_img_flag = True
                self.tester_utf_flag = True
                self.tester_exit_flag = False
                self.tester_burst_skip_flag = False
                self.tester_utf_handler = True
                self.tester_variation_handler = True
                self.tester_variation_counter = runtime_data.parameters["Auto_tester"]["variation_default"]
                runtime_data.variation_counter_actual = runtime_data.parameters["Auto_tester"]["variation_default"]
                self.tester_utf_default = runtime_data.parameters["Auto_tester"]["utf_default"]
                self.tester_utf_counter_actual = runtime_data.parameters["Auto_tester"]["utf_default"]
                self.tester_num_to_inject = self.tester_utf_default
                self.tester_burst_skip_counter = runtime_data.parameters["Auto_tester"]["tester_burst_skip_counter"]

            elif test_mode == 't2':
                self.tester_test_mode = "t2"
                self.tester_img_flag = True
                self.tester_utf_flag = True
                self.tester_exit_flag = False
                self.tester_burst_skip_flag = False
                self.tester_utf_handler = False
                self.tester_variation_handler = True
                self.tester_variation_counter = runtime_data.parameters["Auto_tester"]["variation_default"]
                runtime_data.variation_counter_actual = runtime_data.parameters["Auto_tester"]["variation_default"]
                self.tester_utf_default = -1
                self.tester_utf_counter_actual = -1
                self.tester_num_to_inject = int(test_param)
                self.tester_burst_skip_counter = runtime_data.parameters["Auto_tester"]["tester_burst_skip_counter"]
                print("   <<<   Automatic learning for variations of number << %s >> has been turned ON!   >>>"
                      % test_param)

            else:
                print("Error detecting the test mode...")
                return

        finally:
            toggle_test_mode()
            self.tester_test_id = test_id_gen()
            runtime_data.tester_test_stats["genome_id"] = runtime_data.genome_id
            print('Genome_id = ', runtime_data.genome_id)
            runtime_data.tester_test_stats["test_id"] = self.tester_test_id
            self.tester_testing_has_begun = True


    @staticmethod
    def create_test_stat_template():
        template = {}
        for i in range(10):
            template[i] = {
                "exposed": 0,
                "no_response": 0,
                "comprehended": 0
            }
        return template

    @staticmethod
    def test_stat_counter_incrementer(digit, stat_type):
        runtime_data.tester_test_stats[digit][stat_type] += 1

    def auto_tester(self):
        """
        Test approach:

        - Ask user for number of times testing every digit call it x
        - Inject each number x rounds with each round conclusion being a "Comprehensions"
        - Count the number of True vs. False Comprehensions
        - Collect stats for each number and report at the end of testing

        """
        if self.tester_testing_has_begun:
            # Beginning of a injection process
            print("----------------------------------------Testing has begun------------------------------------")
            self.tester_testing_has_begun = False
            runtime_data.tester_test_stats = self.create_test_stat_template()
            self.tester_test_start_time = datetime.now()
            if self.tester_img_flag:
                # todo: temporarily changing test data set to training instead <<< CHANGE IT BACK!!! >>>
                self.image_feeder2(num=self.tester_num_to_inject,
                                   seq=runtime_data.variation_counter_actual,
                                   mnist_type='test')

        # Mechanism to skip a number of bursts between each injections to clean-up FCL
        if not self.tester_burst_skip_flag:

            print("                                              .... .. .. .. ... New Exposure ... ... ... .. .. ")

            # Injecting test image to the FCL
            if self.tester_img_flag:
                self.img_neuron_list_feeder()
                # print("Test image data just got injected into FCL")

            # Exposure counter
            runtime_data.exposure_counter_actual -= 1

            print('  ----------------------------------------------------------------------------------------    ### ',
                  runtime_data.variation_counter_actual,
                  self.tester_utf_counter_actual,
                  runtime_data.exposure_counter_actual, ' ###')

            if runtime_data.exposure_counter_actual < 1:
                # Turning on the skip flag to allow FCL to clear
                self.tester_burst_skip_flag = True

        else:
            print("Skipping the injection for this round...")
            self.tester_burst_skip_counter -= 1
            if self.tester_burst_skip_counter <= 0 or candidate_list_counter(runtime_data.fire_candidate_list) < 1:
                self.tester_burst_skip_counter = runtime_data.parameters["Auto_tester"]["tester_burst_skip_counter"]
                self.tester_burst_skip_flag = False

                # Final phase of a single test instance is to evaluate the comprehension when FCL is cleaned up
                self.test_comprehension_logic()
                self.tester_test_attempt_counter += 1

                print("Number to inject:", self.tester_num_to_inject)
                print("Default counters:", self.tester_variation_counter,
                      self.tester_utf_default,
                      self.tester_exposure_default)

                print("Current Counters:", runtime_data.variation_counter_actual,
                      self.tester_utf_counter_actual,
                      runtime_data.exposure_counter_actual)

                # Resetting exposure counter
                runtime_data.exposure_counter_actual = self.tester_exposure_default

                # UTF counter
                self.tester_utf_counter_actual -= 1
                self.test_stat_counter_incrementer(digit=self.tester_num_to_inject, stat_type='exposed')

                # self.test_stats_report()

                if self.tester_utf_flag:
                    self.tester_num_to_inject -= 1
                    print('#-#-# Current test UTF counter is ', self.tester_utf_counter_actual)
                    print("#-#-# Current number to inject is :", self.tester_num_to_inject)

                    print(".... .. .. .. ... .... .. .. . ... ... ... .. .. ")
                    print(".... .. .. .. ... .... .. .. . ... ... ... .. .. ")
                    print(".... .. .. .. ... New UTF .. . ... ... ... .. .. ")
                    print(".... .. .. .. ... ... .. .. .  ... ... ... .. .. ")
                    print(".... .. .. .. ... .... .. .. . ... ... ... .. .. ")

                if self.tester_utf_counter_actual < 0:
                    runtime_data.variation_counter_actual -= 1

                    # Variation logic
                    if runtime_data.variation_counter_actual < 1:
                        print(">> Test exit condition has been met <<")
                        self.tester_exit_flag = True
                        self.test_exit_process()

                    print(".... .. .. .. ... .... .. .. . ... ... ... .. .. ")
                    print(".... .. .. .. ... New Variation... ... ... .. .. ")
                    print(".... .. .. .. ... ... .. .. .  ... ... ... .. .. ")

                    # Resetting counters
                    runtime_data.exposure_counter_actual = self.tester_exposure_default
                    self.tester_utf_counter_actual = self.tester_utf_default
                    self.tester_num_to_inject = self.tester_utf_default
                    self.tester_test_attempt_counter = 0
                    self.tester_comprehension_counter = 0
                    self.tester_no_response_counter = 0

                if self.tester_img_flag and not self.tester_exit_flag:
                    print('#-#-# Current number that is about to be tested is ', self.tester_num_to_inject)
                    # todo: temporarily changing test data set to training instead <<< CHANGE IT BACK!!! >>>
                    self.image_feeder2(num=self.tester_num_to_inject,
                                       seq=runtime_data.variation_counter_actual,
                                       mnist_type='test')

    # def update_test_stats(self):
    #     # Initialize parameters
    #     utf_exposed = str(self.tester_num_to_inject) + '_exposed'
    #     utf_comprehended = str(self.tester_num_to_inject) + '_comprehended'
    #     utf_no_response = str(self.tester_num_to_inject) + '_no_response'
    #     if utf_exposed not in self.tester_test_stats:
    #         self.tester_test_stats[utf_exposed] = runtime_data.parameters["Auto_tester"]["utf_default"]
    #     if utf_comprehended not in self.tester_test_stats:
    #         self.tester_test_stats[utf_comprehended] = 0
    #     if utf_no_response not in self.tester_test_stats:
    #         self.tester_test_stats[utf_no_response] = 0
    #
    #     # Add current stats to the list
    #     self.tester_test_stats[utf_exposed] = self.tester_test_attempt_counter
    #     self.tester_test_stats[utf_comprehended] = self.tester_comprehension_counter
    #     self.tester_test_stats[utf_no_response] = self.tester_no_response_counter
    #     print('no_response_counter: ', self.tester_no_response_counter)
    #     print('comprehension_counter: ', self.tester_comprehension_counter)
    #     print('attempted_counter: ', self.tester_test_attempt_counter)

    def test_comprehension_logic(self):
        # Comprehension logic
        print("\n****************************************")
        print("Comprehended char> ", runtime_data.parameters["Input"]["comprehended_char"], "  Injected char> ",
              self.tester_num_to_inject)
        print("****************************************\n")
        if runtime_data.parameters["Input"]["comprehended_char"] in ['', '-']:
            self.tester_no_response_counter += 1
            self.test_stat_counter_incrementer(digit=self.tester_num_to_inject, stat_type='no_response')
            print("() () () No response was logged () () () > Currently no-response counter is",
                  self.tester_no_response_counter)
            runtime_data.parameters["Input"]["comprehended_char"] = ''
        elif runtime_data.parameters["Input"]["comprehended_char"] == str(self.tester_num_to_inject):
            self.test_stat_counter_incrementer(digit=self.tester_num_to_inject, stat_type='comprehended')
            print(settings.Bcolors.HEADER +
                  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                  + settings.Bcolors.ENDC)
            print(settings.Bcolors.HEADER +
                  ">> >> >>                                                   << << <<"
                  + settings.Bcolors.ENDC)
            print(settings.Bcolors.HEADER +
                  ">> >> >> The Brain successfully identified the image as > %s < !!!!"
                  % runtime_data.parameters["Input"]["comprehended_char"] + settings.Bcolors.ENDC)
            print(settings.Bcolors.HEADER +
                  ">> >> >>                                                   << << <<"
                  + settings.Bcolors.ENDC)
            print(settings.Bcolors.HEADER +
                  "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
                  + settings.Bcolors.ENDC)
            self.tester_comprehension_counter += 1
            runtime_data.parameters["Input"]["comprehended_char"] = ''

    @staticmethod
    def test_stats_report():
        # print(runtime_data.tester_test_stats)
        print("\n-----------------------------------------------------------------------------------------------")
        print("Test statistics:")
        print("-----------------------------------------------------------------------------------------------")

        print(settings.Bcolors.OKGREEN + '               ', end='')
        for _ in range(1 + runtime_data.parameters["Auto_tester"]["utf_default"]):
            print(_, '    ', end='')

        print(settings.Bcolors.ENDC + '\nExposed:       ', end='')
        for _ in range(10):
            print(runtime_data.tester_test_stats[_]['exposed'], '    ', end='')

        print('\nNo Response:   ', end='')
        for _ in range(10):
            print(runtime_data.tester_test_stats[_]['no_response'], '    ', end='')

        print('\nComprehended:  ', end='')
        for _ in range(10):
            print(runtime_data.tester_test_stats[_]['comprehended'], '    ', end='')

        print("\n-----------------------------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------------------------")

    def test_exit_process(self):
        runtime_data.parameters["Auto_tester"]["tester_status"] = False
        # runtime_data.exposure_counter_actual = runtime_data.parameters["Auto_tester"]["exposure_default"]
        # runtime_data.variation_counter_actual = runtime_data.parameters["Auto_tester"]["variation_default"]
        # self.tester_utf_counter_actual = runtime_data.parameters["Auto_tester"]["utf_default"]
        test_duration = datetime.now() - self.tester_test_start_time
        print("----------------------------All testing rounds has been completed-----------------------------")
        print("Total test duration was: ", test_duration)
        print("-----------------------------------------------------------------------------------------------")

        self.test_stats_report()

        print("test_stats:\n", runtime_data.tester_test_stats)

        self.tester_test_attempt_counter = 0
        self.tester_comprehension_counter = 0
        self.tester_no_response_counter = 0
        # logging stats into Genome
        runtime_data.genome_test_stats.append(runtime_data.tester_test_stats.copy())
        runtime_data.tester_test_stats = self.create_test_stat_template()
        runtime_data.live_mode_status = 'idle'
        print(settings.Bcolors.RED + "Burst exit triggered by the automated workflow >< >< >< >< >< " +
              settings.Bcolors.ENDC)
        burst_exit_process()

    def user_input_processing(self, user_input, user_input_param):
        while not user_input.empty():
            try:
                user_input_value = user_input.get()
                user_input_value_param = user_input_param.get()

                print("User input value is ", user_input_value)
                print("User input param is ", user_input_value_param)

                if user_input_value == 'x':
                    burst_exit_process()

                elif user_input_value == 'v':
                    toggle_verbose_mode()

                # elif user_input_value == 'g':
                #     toggle_visualization_mode()

                elif user_input_value in ['l1', 'l2', 'r', 'c']:
                    self.injection_manager(injection_mode=user_input_value, injection_param=user_input_value_param)

                elif user_input_value in ['t1', 't2']:
                    self.test_manager(test_mode=user_input_value, test_param=user_input_value_param)

                elif user_input_value == 'd':
                    print('Dumping debug info...')
                    print_cortical_neuron_mappings('vision_memory', 'utf8_memory')

            finally:
                runtime_data.parameters["Input"]["user_input"] = ''
                runtime_data.parameters["Input"]["user_input_param"] = ''
                break


def form_memories(cfcl, pain_flag):
    """
    This function provides logics related to memory formation as follows:
    - Logic to wire memory neurons together when they fire together
    - Logic to reduce synaptic connectivity when one vision memory leads to activation of two UTF neurons
    """

    # todo: The following section to be generalized

    # print("+++++++++cfcl_utf8_memory_neurons:", cfcl_utf8_memory_neurons)
    utf8_memory_count = len(cfcl['utf8_memory'])
    if cfcl['vision_memory'] and runtime_data.parameters["Auto_injector"]["injector_status"]:
        print("Number of vision memory neurons fired in this burst:", len(cfcl['vision_memory']))
        print("Number of UTF memory neurons fired in this burst:", utf8_memory_count)
        tmp_plasticity_list = []
        # Wiring visual memory neurons who are firing together
        for source_neuron in cfcl['vision_memory']:

            # Every visual memory neuron in CFCL is going to wire to evey other vision memory neuron
            # for destination_neuron in cfcl_vision_memory_neurons:
            #     if destination_neuron != source_neuron and destination_neuron not in tmp_plasticity_list:
            #         apply_plasticity(cortical_area='vision_memory',
            #                          src_neuron=source_neuron,
            #                          dst_neuron=destination_neuron)

            # Wiring visual memory neurons to the utf_memory ones
            for destination_neuron in cfcl['utf8_memory']:
                if not pain_flag:
                    apply_plasticity_ext(src_cortical_area='vision_memory', src_neuron_id=source_neuron,
                                         dst_cortical_area='utf8_memory', dst_neuron_id=destination_neuron)
                    # print("wiring visual to utf:", source_neuron, destination_neuron)
                if pain_flag:
                    apply_plasticity_ext(src_cortical_area='vision_memory', src_neuron_id=source_neuron,
                                         dst_cortical_area='utf8_memory', dst_neuron_id=destination_neuron,
                                         long_term_depression=True, impact_multiplier=4)
                    # print("un-wiring visual to utf:", source_neuron, destination_neuron)

            # Reducing synaptic connectivity when a single memory neuron is associated with more than one utf_memory one
            if utf8_memory_count >= 2:
                synapse_to_utf = 0
                runtime_data.temp_neuron_list = []
                neighbor_list = dict(runtime_data.brain['vision_memory'][source_neuron]['neighbors'])
                # print("<><><>")
                for synapse_ in neighbor_list:
                    if runtime_data.brain['vision_memory'][source_neuron]['neighbors'][synapse_]['cortical_area'] \
                            == 'utf8_memory':
                        synapse_to_utf += 1
                        runtime_data.temp_neuron_list.append(synapse_)
                    if synapse_to_utf >= 2:
                        for dst_neuron in runtime_data.temp_neuron_list:
                            apply_plasticity_ext(src_cortical_area='vision_memory', src_neuron_id=source_neuron,
                                                 dst_cortical_area='utf8_memory', dst_neuron_id=dst_neuron,
                                                 long_term_depression=True, impact_multiplier=4)
            tmp_plasticity_list.append(source_neuron)


def burst_exit_process():
    print(settings.Bcolors.YELLOW + '>>>Burst Exit criteria has been met!   <<<' + settings.Bcolors.ENDC)
    runtime_data.live_mode_status = 'idle'
    runtime_data.burst_count = 0
    runtime_data.parameters["Switches"]["ready_to_exit_burst"] = True
    runtime_data.parameters["Auto_injector"]["injector_status"] = False
    if runtime_data.parameters["Switches"]["capture_brain_activities"]:
        save_fcl_to_disk()


def print_cortical_neuron_mappings(src_cortical_area, dst_cortical_area):
    print('Listing neuron mappings between %s and %s' % (src_cortical_area, dst_cortical_area))
    for neuron in runtime_data.brain[src_cortical_area]:
        for neighbor in runtime_data.brain[src_cortical_area][neuron]['neighbors']:
            if runtime_data.brain[src_cortical_area][neuron]['neighbors'][neighbor]['cortical_area'] == \
                    dst_cortical_area:
                print(settings.Bcolors.OKGREEN + '# ', neuron[27:], neighbor[27:],
                      str(runtime_data.brain[src_cortical_area][neuron]
                      ['neighbors'][neighbor]['postsynaptic_current']) + settings.Bcolors.ENDC)


#  >>>>>> Review this function against what we had in past
def fire_candidate_locations(fire_cnd_list):
    """Extracts Neuron locations from the fire_candidate_list"""

    # print('***')
    # print(fire_cnd_list)

    neuron_locations = {}
    # Generate a dictionary of cortical areas in the fire_candidate_list
    for item in runtime_data.cortical_list:
        neuron_locations[item] = []

    # Add neuron locations under each cortical area
    for cortical_area in fire_cnd_list:
        for neuron in fire_cnd_list[cortical_area]:
            neuron_locations[cortical_area].append([runtime_data.brain[cortical_area][neuron]["location"][0],
                                                    runtime_data.brain[cortical_area][neuron]["location"][1],
                                                    runtime_data.brain[cortical_area][neuron]["location"][2]])

    return neuron_locations


def update_upstream_db(src_cortical_area, src_neuron_id, dst_cortical_area, dst_neuron_id):
    # if dst_cortical_area not in runtime_data.upstream_neurons:
    #     runtime_data.upstream_neurons[dst_cortical_area] = {}
    if dst_neuron_id not in runtime_data.upstream_neurons[dst_cortical_area]:
        runtime_data.upstream_neurons[dst_cortical_area][dst_neuron_id] = {}
    if src_cortical_area not in runtime_data.upstream_neurons[dst_cortical_area][dst_neuron_id]:
        runtime_data.upstream_neurons[dst_cortical_area][dst_neuron_id][src_cortical_area] = set()
    if src_neuron_id not in runtime_data.upstream_neurons[dst_cortical_area][dst_neuron_id][src_cortical_area]:
        runtime_data.upstream_neurons[dst_cortical_area][dst_neuron_id][src_cortical_area].add(src_neuron_id)


def activation_function(postsynaptic_current):
    # print("PSC: ", postsynaptic_current)
    return postsynaptic_current


def neuron_fire(cortical_area, neuron_id):
    """This function initiate the firing of Neuron in a given cortical area"""

    # if runtime_data.parameters["Switches"]["logging_fire"]:
    #     print(datetime.now(), " Firing...", cortical_area, neuron_id, file=open("./logs/fire.log", "a"))
    neighbor_list = list()

    # if cortical_area == 'utf8_memory':
    #     print(">>> *** ... Firing...", neuron_id)

    # Setting Destination to the list of Neurons connected to the firing Neuron
    try:
        neighbor_list = runtime_data.brain[cortical_area][neuron_id]["neighbors"]

    except KeyError:
        print(settings.Bcolors.RED + "KeyError on accessing neighbor_list while firing a neuron" +
              settings.Bcolors.ENDC)

    # Condition to update neuron activity history currently only targeted for UTF-OPU
    # todo: move activity_history_span to genome
    activity_history_span = runtime_data.parameters["InitData"]["activity_history_span"]
    if cortical_area == 'utf8_memory':
        if not runtime_data.brain[cortical_area][neuron_id]["activity_history"]:
            zeros = deque([0] * activity_history_span)
            tmp_burst_list = []
            tmp_burst_count = runtime_data.burst_count
            for _ in range(activity_history_span):
                tmp_burst_list.append(tmp_burst_count)
                tmp_burst_count -= 1
            runtime_data.brain[cortical_area][neuron_id]["activity_history"] = deque(list(zip(tmp_burst_list, zeros)))
        else:
            runtime_data.brain[cortical_area][neuron_id]["activity_history"].append([runtime_data.burst_count,
                                                                                     runtime_data.brain[cortical_area]
                                                                                    [neuron_id]["membrane_potential"]])
            runtime_data.brain[cortical_area][neuron_id]["activity_history"].popleft()

    # After neuron fires all cumulative counters on Source gets reset
    runtime_data.brain[cortical_area][neuron_id]["membrane_potential"] = 0
    runtime_data.brain[cortical_area][neuron_id]["last_membrane_potential_reset_burst"] = runtime_data.burst_count
    runtime_data.brain[cortical_area][neuron_id]["cumulative_fire_count"] += 1
    runtime_data.brain[cortical_area][neuron_id]["cumulative_fire_count_inst"] += 1

    # Transferring the signal from firing Neuron's Axon to all connected Neuron Dendrites
    # todo: Firing pattern to be accommodated here     <<<<<<<<<<  *****
    # neuron_update_list = []

    # if cortical_area == 'vision_memory':
    #     runtime_data.cumulative_neighbor_count += neighbor_count
    neighbor_count = len(neighbor_list)

    # Updating downstream neurons
    for dst_neuron_id in neighbor_list:

        # Timing the update function
        # update_start_time = datetime.now()

        dst_cortical_area = \
            runtime_data.brain[cortical_area][neuron_id]["neighbors"][dst_neuron_id]["cortical_area"]
        postsynaptic_current = \
            runtime_data.brain[cortical_area][neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"]
        # if cortical_area == 'vision_memory':
        #    print("< %i >" %postsynaptic_current)

        neuron_output = activation_function(postsynaptic_current)

        # Update function
        # todo: (neuron_output/neighbor_count) needs to be moved outside the loop for efficiency
        dst_neuron_obj = runtime_data.brain[dst_cortical_area][dst_neuron_id]
        dst_neuron_obj["membrane_potential"] = \
            cy.neuron_update((neuron_output/neighbor_count),
                             runtime_data.burst_count,
                             max(dst_neuron_obj["last_membrane_potential_reset_burst"],
                             dst_neuron_obj["last_burst_num"]),
                             runtime_data.genome["blueprint"][dst_cortical_area]["neuron_params"]["leak_coefficient"],
                             dst_neuron_obj["membrane_potential"])

        # todo: Need to figure how to deal with activation function and firing threshold (belongs to fire func)
        # After destination neurons are updated, the following checks are performed to assess if the neuron should fire
        if dst_neuron_obj["membrane_potential"] > dst_neuron_obj["firing_threshold"]:
            # if dst_cortical_area == 'utf8_memory':
            # print('++++++ The membrane potential passed the firing threshold')
            # Refractory period check
            if dst_neuron_obj["last_burst_num"] + \
                    runtime_data.genome["blueprint"][dst_cortical_area]["neuron_params"]["refractory_period"] <= \
                    runtime_data.burst_count:
                # Inhibitory effect check
                if dst_neuron_obj["snooze_till_burst_num"] <= runtime_data.burst_count:
                    # Adding neuron to fire candidate list for firing in the next round
                    runtime_data.future_fcl[dst_cortical_area].add(dst_neuron_id)

                    # todo: not sure what's being done here. Why this is too generic on all cortical layers? !!
                    # todo: Why this needs to happen on each synapse update?? !! VERY EXPENSIVE OPERATION!!!!
                    # todo: Based on the initial test results, removing the following section can make the code run
                    # todo: 10 times faster but result in 1/2 fitness
                    # todo: add a condition to only LTP when cortical area source is upstream of cortical area dest.
                    # todo: adding an impact multiplier here could be beneficial
                    # This is an alternative approach to plasticity with hopefully less overhead
                    # LTP or Long Term Potentiation occurs here
                    upstream_data = list_upstream_neurons(dst_cortical_area, dst_neuron_id)

                    ltp_targets = ['vision_memory', 'utf8_memory']

                    if upstream_data and dst_cortical_area in ltp_targets:
                        for src_cortical_area in upstream_data:
                            for src_neuron in upstream_data[src_cortical_area]:
                                if src_cortical_area != dst_cortical_area and \
                                        src_neuron in runtime_data.previous_fcl[src_cortical_area]:
                                    apply_plasticity_ext(src_cortical_area=src_cortical_area,
                                                         src_neuron_id=src_neuron,
                                                         dst_cortical_area=dst_cortical_area,
                                                         dst_neuron_id=dst_neuron_id, impact_multiplier=1)

        # Resetting last time neuron was updated to the current burst id
        runtime_data.brain[dst_cortical_area][dst_neuron_id]["last_burst_num"] = runtime_data.burst_count

        # Time overhead for the following function is about 2ms per each burst cycle
        update_upstream_db(cortical_area, neuron_id, dst_cortical_area, dst_neuron_id)

        # Partial implementation of neuro-plasticity associated with LTD or Long Term Depression
        if cortical_area not in ['vision_memory']:
            if dst_neuron_id in runtime_data.previous_fcl[dst_cortical_area] and dst_cortical_area in ['vision_memory']:
                apply_plasticity_ext(src_cortical_area=cortical_area, src_neuron_id=neuron_id,
                                     dst_cortical_area=dst_cortical_area, dst_neuron_id=dst_neuron_id,
                                     long_term_depression=True)

                if runtime_data.parameters["Logs"]["print_plasticity_info"]:
                    print(settings.Bcolors.RED + "--------- Neuron Fire ---------"
                                                 "...........LTD between %s and %s occurred"
                          % (dst_cortical_area, dst_cortical_area)
                          + settings.Bcolors.ENDC)

        # Adding up all update times within a burst span
        # total_update_time = datetime.now() - update_start_time
        # runtime_data.time_neuron_update = total_update_time + runtime_data.time_neuron_update

    # todo: not sure what's being done here. Why this is too generic on all cortical layers? !!
    # todo: Why this needs to happen on each synapse update?? !! VERY EXPENSIVE OPERATION!!!!
    # todo: Based on the initial test results, removing the following section can make the code run
    # todo: 10 times faster but result in 1/2 fitness
    # todo: add a condition to only LTP when cortical area source is upstream of cortical area dest.
    # todo: adding an impact multiplier here could be beneficial
    # This is an alternative approach to plasticity with hopefully less overhead
    # LTP or Long Term Potentiation occurs here
    upstream_data = list_upstream_neurons(cortical_area, neuron_id)

    if upstream_data:
        for src_cortical_area in upstream_data:
            for src_neuron in upstream_data[src_cortical_area]:
                if src_cortical_area != cortical_area and \
                        src_neuron in runtime_data.previous_fcl[src_cortical_area]:
                    apply_plasticity_ext(src_cortical_area=src_cortical_area,
                                         src_neuron_id=src_neuron,
                                         dst_cortical_area=cortical_area,
                                         dst_neuron_id=neuron_id, impact_multiplier=1)

    # Condition to snooze the neuron if consecutive fire count reaches threshold
    if runtime_data.brain[cortical_area][neuron_id]["consecutive_fire_cnt"] > \
            runtime_data.genome["blueprint"][cortical_area]["neuron_params"]["consecutive_fire_cnt_max"]:
        snooze_till(cortical_area, neuron_id, runtime_data.burst_count +
                    runtime_data.genome["blueprint"][cortical_area]["neuron_params"]["snooze_length"])

    # Condition to increase the consecutive fire count
    if runtime_data.burst_count == runtime_data.brain[cortical_area][neuron_id]["last_burst_num"] + 1:
        runtime_data.brain[cortical_area][neuron_id]["consecutive_fire_cnt"] += 1

    # todo: rename last_burst_num to last_firing_burst
    runtime_data.brain[cortical_area][neuron_id]["last_burst_num"] = runtime_data.burst_count

    # Condition to translate activity in utf8_out region as a character comprehension
    if cortical_area == 'utf8_memory':
        detected_item, activity_rank = OPU_utf8.convert_neuron_activity_to_utf8_char(cortical_area, neuron_id)
        # todo: burst detection list could be a set instead
        if detected_item not in runtime_data.burst_detection_list:
            runtime_data.burst_detection_list[detected_item] = {}
            runtime_data.burst_detection_list[detected_item]['count'] = 1
        else:
            runtime_data.burst_detection_list[detected_item]['count'] += 1
        runtime_data.burst_detection_list[detected_item]['rank'] = activity_rank

    # # Removing the fired neuron from the FCL
    # runtime_data.fire_candidate_list[cortical_area].remove(neuron_id)

    # todo: add a check that if the firing neuron is part of OPU to perform an action

    return


def list_upstream_neurons(cortical_area, neuron_id):
    if cortical_area in runtime_data.upstream_neurons:
        if neuron_id in runtime_data.upstream_neurons[cortical_area]:
            return runtime_data.upstream_neurons[cortical_area][neuron_id]
    return {}


def list_top_n_utf_memory_neurons(cortical_area, n):
    neuron_list = []
    counter = ord('0')
    the_other_counter = 0
    for neuron_id in runtime_data.brain[cortical_area]:
        if int(runtime_data.brain[cortical_area][neuron_id]['soma_location'][0][2]) == counter:
            neuron_list.append([int(runtime_data.brain[cortical_area][neuron_id]['soma_location'][0][2])-48, neuron_id])
            counter += 1
            the_other_counter += 1
            if the_other_counter == n:
                return neuron_list
    print("ERROR: Something went wrong in list_top_n_utf_memory_neurons")


def list_upstream_neuron_count_for_digits(digit='all', mode=0):
    # function_start_time = datetime.now()
    results = []
    fcl_results = []

    if digit == 'all':
        for _ in range(10):
            # results.append([_, len(list_
            #                        upstream_neurons('utf8_memory', runtime_data.top_10_utf_memory_neurons[_][1]))])
            neuron_id = runtime_data.top_10_utf_memory_neurons[_][1]
            if 'utf8_memory' in runtime_data.upstream_neurons:
                if neuron_id in runtime_data.upstream_neurons['utf8_memory']:
                    if 'vision_memory' in runtime_data.upstream_neurons['utf8_memory'][neuron_id]:
                        results.append([_,
                                        len(runtime_data.upstream_neurons['utf8_memory'][neuron_id]['vision_memory'])])
                        if runtime_data.upstream_neurons['utf8_memory'][neuron_id]['vision_memory']:
                            counter = 0
                            for neuron in runtime_data.upstream_neurons['utf8_memory'][neuron_id]['vision_memory']:
                                if neuron in runtime_data.fire_candidate_list['vision_memory']:
                                    counter += 1
                            fcl_results.append([_, counter])
                        else:
                            fcl_results.append([_, 0])
                    else:
                        results.append([_, 0])
                        fcl_results.append([_, 0])
                else:
                    results.append([_, 0])
                    fcl_results.append([_, 0])
            else:
                results.append([_, 0])
                fcl_results.append([_, 0])
    else:
        neuron_id = runtime_data.top_10_utf_memory_neurons[digit][1]
        if 'utf8_memory' in runtime_data.upstream_neurons:
            if neuron_id in runtime_data.upstream_neurons['utf8_memory']:
                if 'vision_memory' in runtime_data.upstream_neurons['utf8_memory'][neuron_id]:
                    results.append([digit,
                                    len(runtime_data.upstream_neurons['utf8_memory'][neuron_id]['vision_memory'])])
                else:
                    results.append([digit, 0])
            else:
                results.append([digit, 0])
        else:
            results.append([digit, 0])
    # print("Timing : list_upstream_neuron_count_for_digits:", datetime.now()-function_start_time)

    if mode == 0:
        print("&& && & &&& && && & : The mode is == 0")
        return results
    else:
        print("&& && & &&& && && & : The mode is != 0")
        return results, fcl_results


def list_common_upstream_neurons(neuron_a, neuron_b):
    common_neuron_list = []

    try:
        neuron_a_upstream_neurons = runtime_data.upstream_neurons['utf8_memory'][neuron_a]['vision_memory']
        neuron_b_upstream_neurons = runtime_data.upstream_neurons['utf8_memory'][neuron_b]['vision_memory']
        for neuron in neuron_a_upstream_neurons:
            if neuron in neuron_b_upstream_neurons:
                common_neuron_list.append(neuron)
        return common_neuron_list

    except:
        pass


def utf_neuron_id(n):
    # Returns the neuron id associated with a particular digit
    for neuron_id in runtime_data.brain['utf8_memory']:
        if int(runtime_data.brain['utf8_memory'][neuron_id]["soma_location"][0][2]) == n+ord('0'):
            return neuron_id


def utf_neuron_position(neuron_id):
    return int(runtime_data.brain['utf8_memory'][neuron_id]["soma_location"][0][2]) - ord('0')


def common_neuron_report():
    digits = range(10)
    number_matrix = []
    for _ in digits:
        for __ in digits:
            if _ != __ and [_, __] not in number_matrix and [__, _] not in number_matrix:
                number_matrix.append([_, __])
    for item in number_matrix:
        neuron_a = utf_neuron_id(item[0])
        neuron_b = utf_neuron_id(item[1])
        common_neuron_list = list_common_upstream_neurons(neuron_a, neuron_b)

        if common_neuron_list:
            overlap_amount = len(common_neuron_list)
            # print(item, '> ', overlap_amount)

            if overlap_amount > runtime_data.parameters["InitData"]["overlap_prevention_constant"]:
                # The following action is taken to eliminate the overlap
                for neuron in common_neuron_list:
                    runtime_data.prunning_candidates.add(('vision_memory', neuron, 'utf8_memory', neuron_a))
                    runtime_data.prunning_candidates.add(('vision_memory', neuron, 'utf8_memory', neuron_b))


def neuron_prop(cortical_area, neuron_id):
    """This function accepts neuron id and returns neuron properties"""

    data = runtime_data.brain[cortical_area]

    if runtime_data.parameters["Switches"]["verbose"]:
        print('Listing Neuron Properties for %s:' % neuron_id)
        print(json.dumps(data[neuron_id], indent=3))
    return data[neuron_id]


def neuron_neighbors(cortical_area, neuron_id):
    """This function accepts neuron id and returns the list of Neuron neighbors"""

    data = runtime_data.brain[cortical_area]

    if runtime_data.parameters["Switches"]["verbose"]:
        print('Listing Neuron Neighbors for %s:' % neuron_id)
        print(json.dumps(data[neuron_id]["neighbors"], indent=3))
    return data[neuron_id]["neighbors"]


def apply_plasticity(cortical_area, src_neuron, dst_neuron):
    """
    This function simulates neuron plasticity in a sense that when neurons in a given cortical area fire in the 
     same burst they wire together. This is done by increasing the postsynaptic_current associated with a link between
     two neuron. Additionally an event id is associated to the neurons who have fired together.
    """

    if runtime_data.parameters["Auto_injector"]["injector_status"]:
        genome = runtime_data.genome

        # Since this function only targets Memory regions and neurons in mem regions do not have neighbor relationship
        # by default hence here we first need to synapse the source and destination together
        # Build neighbor relationship between the source and destination if its not already in place

        neighbor_count = len(runtime_data.brain[cortical_area][src_neuron]["neighbors"])
        if neighbor_count < runtime_data.parameters["InitData"]["max_neighbor_count"]:
            # Check if source and destination have an existing synapse if not create one here
            if dst_neuron not in runtime_data.brain[cortical_area][src_neuron]["neighbors"]:
                synapse(cortical_area, src_neuron, cortical_area, dst_neuron,
                        genome["blueprint"][cortical_area]["postsynaptic_current"])
                update_upstream_db(cortical_area, src_neuron, cortical_area, dst_neuron)

            # Every time source and destination neuron is fired at the same time which in case of the code architecture
            # reside in the same burst, the postsynaptic_current will be increased simulating the fire together,
            # wire together. This phenomenon is also considered as long term potentiation or LTP
            runtime_data.brain[cortical_area][src_neuron]["neighbors"][dst_neuron]["postsynaptic_current"] += \
                genome["blueprint"][cortical_area]["plasticity_constant"]

            # Condition to cap the postsynaptic_current and provide prohibitory reaction
            if runtime_data.brain[cortical_area][src_neuron]["neighbors"][dst_neuron]["postsynaptic_current"] > \
                    genome["blueprint"][cortical_area]["postsynaptic_current_max"]:
                runtime_data.brain[cortical_area][src_neuron]["neighbors"][dst_neuron]["postsynaptic_current"] = \
                    genome["blueprint"][cortical_area]["postsynaptic_current_max"]

            # print('<*> ', cortical_area, src_neuron[27:], dst_neuron[27:], 'PSC=',
            #       runtime_data.brain[cortical_area][src_neuron]["neighbors"][dst_neuron]["postsynaptic_current"])

            # Append a Group ID so Memory clusters can be uniquely identified
            if runtime_data.event_id:
                if runtime_data.event_id in runtime_data.brain[cortical_area][src_neuron]["event_id"]:
                    runtime_data.brain[cortical_area][src_neuron]["event_id"][runtime_data.event_id] += 1
                else:
                    runtime_data.brain[cortical_area][src_neuron]["event_id"][runtime_data.event_id] = 1

    return


def apply_plasticity_ext(src_cortical_area, src_neuron_id, dst_cortical_area,
                         dst_neuron_id, long_term_depression=False, impact_multiplier=1):

    if runtime_data.parameters["Auto_injector"]["injector_status"]:
        plasticity_constant = runtime_data.genome["blueprint"][src_cortical_area]["plasticity_constant"]

        if long_term_depression:
            # When long term depression flag is set, there will be negative synaptic influence caused
            plasticity_constant = runtime_data.genome["blueprint"][src_cortical_area]["plasticity_constant"] * (-1) * impact_multiplier

        try:
            runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] += \
                plasticity_constant

            # Condition to cap the postsynaptic_current and provide prohibitory reaction
            if runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] > \
                    runtime_data.genome["blueprint"][src_cortical_area]["postsynaptic_current_max"]:
                runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] = \
                    runtime_data.genome["blueprint"][src_cortical_area]["postsynaptic_current_max"]

            # Condition to prevent postsynaptic current to become negative
            # todo: consider setting a postsynaptic_min in genome to be used instead of 0
            # Condition to prune a synapse if its postsynaptic_current is zero
            if runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] < 0:
                runtime_data.prunning_candidates.add((src_cortical_area, src_neuron_id, dst_cortical_area, dst_neuron_id))

        except KeyError:
            synapse(src_cortical_area,
                    src_neuron_id,
                    dst_cortical_area,
                    dst_neuron_id,
                    max(plasticity_constant, 0))
            update_upstream_db(src_cortical_area, src_neuron_id, dst_cortical_area, dst_neuron_id)

            runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] += \
                plasticity_constant

            # Condition to cap the postsynaptic_current and provide prohibitory reaction
            if runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] > \
                    runtime_data.genome["blueprint"][src_cortical_area]["postsynaptic_current_max"]:
                runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] = \
                    runtime_data.genome["blueprint"][src_cortical_area]["postsynaptic_current_max"]

            # Condition to prevent postsynaptic current to become negative
            # todo: consider setting a postsynaptic_min in genome to be used instead of 0
            # Condition to prune a synapse if its postsynaptic_current is zero
            if runtime_data.brain[src_cortical_area][src_neuron_id]["neighbors"][dst_neuron_id]["postsynaptic_current"] < 0:
                runtime_data.prunning_candidates.add((src_cortical_area, src_neuron_id, dst_cortical_area, dst_neuron_id))


def snooze_till(cortical_area, neuron_id, burst_id):
    """ Acting as an inhibitory neurotransmitter to suppress firing of neuron till a later burst

    *** This function instead of inhibitory behavior is more inline with Neuron Refractory period

    """
    runtime_data.brain[cortical_area][neuron_id]["snooze_till_burst_num"] \
        = burst_id + runtime_data.genome["blueprint"][cortical_area]["neuron_params"]["snooze_length"]
    # print("%s : %s has been snoozed!" % (cortical_area, neuron_id))
    return


def save_fcl_to_disk():
    with open("./fcl_repo/fcl-" + runtime_data.brain_run_id + ".json", 'w') as fcl_file:
        # Saving changes to the connectome
        fcl_file.seek(0)  # rewind
        fcl_file.write(json.dumps(runtime_data.fcl_history, indent=3))
        fcl_file.truncate()

    print("Brain activities has been preserved!")


def load_fcl_in_memory(file_name):
    with open(file_name, 'r') as fcl_file:
        fcl_data = json.load(fcl_file)
    return fcl_data


def latest_fcl_file():
    list_of_files = glob.glob('./fcl_repo/*.json')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def pickler(data):
    
    id_ = runtime_data.brain_run_id
    with open("./pickle_jar/fcl-" + id_ + ".pkl", 'wb') as output:
        pickle.dump(data, output)


def unpickler(data_type, id_):
    if data_type == 'fcl':
        with open("./pickle_jar/fcl-" + id_ + ".pkl", 'rb') as input_data:
            data = pickle.load(input_data)
            return data
    else:
        print("Error: Type not found!")


def toggle_verbose_mode():
    if runtime_data.parameters["Switches"]["verbose"]:
        runtime_data.parameters["Switches"]["verbose"] = False
        print("Verbose mode is Turned OFF!")
    else:
        runtime_data.parameters["Switches"]["verbose"] = True
        print("Verbose mode is Turned On!")


def toggle_injection_mode():
    if runtime_data.parameters["Auto_injector"]["injector_status"]:
        runtime_data.parameters["Auto_injector"]["injector_status"] = False
        print("Auto_train mode is Turned OFF!")
    else:
        runtime_data.parameters["Auto_injector"]["injector_status"] = True
        print("Auto_train mode is Turned On!")


def toggle_test_mode():
    if runtime_data.parameters["Auto_tester"]["tester_status"]:
        runtime_data.parameters["Auto_tester"]["tester_status"] = False
        print("Auto_test mode is Turned OFF!")
    else:
        runtime_data.parameters["Auto_tester"]["tester_status"] = True
        print("Auto_test mode is Turned On!")


def toggle_brain_status():
    
    if runtime_data.brain_is_running:
        runtime_data.brain_is_running = False
        print("Brain is not running!")
    else:
        runtime_data.brain_is_running = True
        print("Brain is now running!!!")


def cortical_group_members(group):
    # members = []
    # for item in runtime_data.cortical_list:
    #     if runtime_data.genome['blueprint'][item]['group_id'] == group:
    #         members.append(item)
    return [item for item in runtime_data.cortical_list if runtime_data.genome['blueprint'][item]['group_id'] == group]


def reset_cumulative_counter_instances():
    """
    To reset the cumulative counter instances
    """
    for cortical_area in runtime_data.brain:
        for neuron in runtime_data.brain[cortical_area]:
            runtime_data.brain[cortical_area][neuron]['cumulative_fire_count_inst'] = 0
    return


def exhibit_pain():
    print("*******************************************************************")
    print("*******************************************************************")
    print("*********************                                 *************")
    print("*******************    Pain -- Pain -- Pain -- Pain     ***********")
    print("*********************                                 *************")
    print("*******************************************************************")
    print("*******************************************************************")


def trigger_pain():
    exhibit_pain()
    for neuron in runtime_data.brain['pain']:
        runtime_data.future_fcl['pain'].add(neuron)


def pruner(pruning_data):
    """
    Responsible for pruning unused connections between neurons
    """
    cortical_area_src, src_neuron_id, cortical_area_dst, dst_neuron_id = pruning_data
    runtime_data.brain[cortical_area_src][src_neuron_id]['neighbors'].pop(dst_neuron_id, None)

    runtime_data.upstream_neurons[cortical_area_dst][dst_neuron_id][cortical_area_src].remove(src_neuron_id)
    if dst_neuron_id in runtime_data.temp_neuron_list:
        runtime_data.temp_neuron_list.remove(dst_neuron_id)


# todo: performance bottleneck; cythonize
def average_postsynaptic_current(cortical_area):
    count = 0
    total = 0
    for neuron in runtime_data.brain[cortical_area]:
        for neighbor in runtime_data.brain[cortical_area][neuron]['neighbors']:
            count += 1
            total += runtime_data.brain[cortical_area][neuron]['neighbors'][neighbor]['postsynaptic_current']
    if count > 0:
        avg_postsynaptic_current = total / count
    else:
        avg_postsynaptic_current = 0
    return avg_postsynaptic_current


def prune_all_candidates():
    while runtime_data.prunning_candidates:
        prune_candidate = runtime_data.prunning_candidates.pop()
        pruner(prune_candidate)


def stats_utf_memory_membrane_potentials():
    if runtime_data.top_10_utf_memory_neurons and runtime_data.top_10_utf_neurons:
        utf_neurons = []
        for neuron in runtime_data.top_10_utf_neurons:
            utf_neurons.append((neuron[0], neuron[1]))
        print('\n')
        for neuron in runtime_data.top_10_utf_memory_neurons:
            if runtime_data.brain['utf8_memory'][neuron[1]]['membrane_potential'] > \
                    runtime_data.genome['blueprint']['utf8_memory']['neuron_params']['firing_threshold']:
                print(settings.Bcolors.RED + '>>> ', neuron[0], '   >>> ',
                      str(runtime_data.brain['utf8'][utf_neurons[int(neuron[0])][1]]['membrane_potential']), '   >>> ',
                      str(runtime_data.brain['utf8_memory'][neuron[1]]['membrane_potential']),
                      '   >>>',
                      str(runtime_data.genome['blueprint']['utf8_memory']['neuron_params']['firing_threshold']) +
                      settings.Bcolors.ENDC)
            else:
                print('>>> ', neuron[0], '   >>> ',
                      str(runtime_data.brain['utf8'][utf_neurons[int(neuron[0])][1]]['membrane_potential']), '   >>> ',
                      runtime_data.brain['utf8_memory'][neuron[1]]['membrane_potential'],
                      '   >>>',
                      runtime_data.genome['blueprint']['utf8_memory']['neuron_params']['firing_threshold'])
        print('\n')
