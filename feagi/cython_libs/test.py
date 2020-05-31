

import random

a = {
          "growth_path" : "",
          "direction_sensitivity" : "/",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 1,
          "layer_index" : 1,
          "total_layer_count" : 7,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1597,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_1"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.633575495825,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 2.89235403072,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.659231437448,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      32
                  ],
                  "y" : [
                      0,
                      32
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      }

b = {
  "firing_patterns" : {
      "A" : {
          "frequency" : "100",
          "magnitude" : "80"
      },
      "B" : {
          "frequency" : "20",
          "magnitude" : "100"
      }
  },
  "neighbor_locator_rule" : {
      "rule_0" : {
          "param_1" : 0,
          "param_2" : 0
      },
      "rule_1" : {
          "param_1" : 1,
          "param_2" : 1
      },
      "rule_2" : {
          "param_1" : 5,
          "param_2" : 5,
          "param_3" : 10
      },
      "rule_3" : {
          "param_1" : 0,
          "param_2" : 0
      },
      "rule_4" : {
          "param_1" : 25,
          "param_2" : 77
      },
      "rule_5" : {
          "param_1" : 700,
          "param_2" : 700,
          "param_3" : 700,
          "param_4" : 700,
          "param_5" : 700,
          "param_6" : 700,
          "param_7" : 700
      },
      "rule_6" : {
          "param_1" : 1,
          "param_2" : 1
      }
  },
  "IPU_vision_filters" : {
      "3" : {
          "-" : [
              [
                  -1,
                  -1,
                  -1
              ],
              [
                  1,
                  1,
                  1
              ],
              [
                  -1,
                  -1,
                  -1
              ]
          ],
          "|" : [
              [
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1
              ]
          ],
          " " : [
              [
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0
              ]
          ],
          "o" : [
              [
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  8,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1
              ]
          ],
          "/" : [
              [
                  -1,
                  -1,
                  1
              ],
              [
                  -1,
                  1,
                  -1
              ],
              [
                  1,
                  -1,
                  -1
              ]
          ],
          "\\" : [
              [
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1
              ]
          ]
      },
      "5" : {
          "-" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  1,
                  1,
                  1,
                  1,
                  1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          " " : [
              [
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0
              ]
          ],
          "|" : [
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ]
          ],
          "o" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "/" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "\\" : [
              [
                  1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  1
              ]
          ]
      },
      "7" : {
          "-" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  1,
                  1,
                  1,
                  1,
                  1,
                  1,
                  1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          " " : [
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ],
              [
                  0,
                  0,
                  0,
                  0,
                  0,
                  0,
                  0
              ]
          ],
          "I" : [
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "i" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "o" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "/" : [
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ]
          ],
          "\\" : [
              [
                  1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  1,
                  -1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  1,
                  -1
              ],
              [
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  -1,
                  1
              ]
          ]
      }
  },
  "location_tolerance" : 2,
  "image_color_intensity_tolerance" : 100,
  "max_burst_count" : 3,
  "evolution_burst_count" : 50,
  "performance_stats" : {
      "mnist_view_cnt" : 0,
      "mnist_correct_detection_cnt" : 0
  },
  "blueprint" : {
      "vision_v1-1" : {
          "growth_path" : "",
          "direction_sensitivity" : "/",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 1,
          "layer_index" : 1,
          "total_layer_count" : 7,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1597,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_1"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.633575495825,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 2.89235403072,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.659231437448,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      32
                  ],
                  "y" : [
                      0,
                      32
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-2" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 4,
          "layer_index" : 2,
          "total_layer_count" : 7,
          "direction_sensitivity" : "\\",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1403,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_2"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-3" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 7,
          "layer_index" : 3,
          "total_layer_count" : 7,
          "direction_sensitivity" : "|",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1403,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_3"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-4" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 10,
          "layer_index" : 4,
          "total_layer_count" : 7,
          "direction_sensitivity" : "-",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1403,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1100,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_4"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-5" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 13,
          "layer_index" : 5,
          "total_layer_count" : 7,
          "direction_sensitivity" : "I",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 3,
          "cortical_neuron_count" : 1403,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_5"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-6" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 16,
          "layer_index" : 6,
          "total_layer_count" : 7,
          "direction_sensitivity" : "o",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 3,
          "cortical_neuron_count" : 1404,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_6"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v1-7" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v1",
          "plot_index" : 19,
          "layer_index" : 7,
          "total_layer_count" : 7,
          "direction_sensitivity" : " ",
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 5,
          "cortical_neuron_count" : 1403,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 20,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 1000,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "vision_v2" : {
                  "neighbor_locator_rule_id" : "rule_5",
                  "neighbor_locator_rule_param_id" : "param_7"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "orientation_selectivity_id" : "",
              "firing_threshold" : 3.4898094,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.83787266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      29
                  ],
                  "y" : [
                      0,
                      29
                  ],
                  "z" : [
                      0,
                      10
                  ]
              }
          }
      },
      "vision_v2" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_v2",
          "plot_index" : 2,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 3,
          "cortical_neuron_count" : 14321,
          "location_generation_type" : "random",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 150,
          "plasticity_constant" : 0,
          "postsynaptic_current_max" : 200,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_2",
          "cortical_mapping_dst" : {
              "vision_memory" : {
                  "neighbor_locator_rule_id" : "rule_6",
                  "neighbor_locator_rule_param_id" : "param_2"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "depolarization_threshold" : 1.574682375,
              "firing_threshold" : 1.1632698,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "orientation_selectivity_id" : "",
              "axon_avg_length" : "",
              "leak_coefficient" : 5,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 0.0,
              "block_boundaries" : [
                  28,
                  28,
                  7
              ],
              "geometric_boundaries"  : {
                  "x" : [
                      0,
                      74
                  ],
                  "y" : [
                      0,
                      74
                  ],
                  "z" : [
                      0,
                      74
                  ]
              }
          }
      },
      "vision_IT" : {
          "growth_path" : "",
          "group_id" : "vision",
          "sub_group_id" : "vision_IT",
          "plot_index" : 3,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 16836,
          "location_generation_type" : "random",
          "synapse_attractivity" : 80,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 100,
          "plasticity_constant" : 0.5,
          "postsynaptic_current_max" : 300,
          "neighbor_locator_rule_id" : "rule_1",
          "neighbor_locator_rule_param_id" : "param_2",
          "cortical_mapping_dst" : {
              "vision_memory" : {
                  "neighbor_locator_rule_id" : "rule_6",
                  "neighbor_locator_rule_param_id" : "param_2"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 1.574682375,
              "firing_threshold" : 0.882,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 5,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 0,
              "snooze_length" : 1.02467266,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      74
                  ],
                  "y" : [
                      0,
                      74
                  ],
                  "z" : [
                      0,
                      74
                  ]
              }
          }
      },
      "vision_memory" : {
          "growth_path" : "",
          "group_id" : "Memory",
          "sub_group_id" : "vision",
          "plot_index" : 1,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 50001,
          "location_generation_type" : "random",
          "synapse_attractivity" : 10,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 0.9,
          "plasticity_constant" : 1,
          "postsynaptic_current_max" : 60,
          "neighbor_locator_rule_id" : "rule_0",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {},
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 5,
              "firing_threshold" : 1.5,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 5,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 2,
              "snooze_length" : 8,
              "block_boundaries" : [
                  28,
                  28,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      201
                  ],
                  "y" : [
                      0,
                      201
                  ],
                  "z" : [
                      0,
                      201
                  ]
              }
          }
      },
      "utf8" : {
          "growth_path" : "",
          "group_id" : "IPU",
          "sub_group_id" : "IPU_utf8",
          "plot_index" : 1,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 300,
          "location_generation_type" : "sequential",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 501,
          "plasticity_constant" : 0.05,
          "postsynaptic_current_max" : 501,
          "neighbor_locator_rule_id" : "rule_0",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "utf8_memory" : {
                  "neighbor_locator_rule_id" : "rule_3",
                  "neighbor_locator_rule_param_id" : "param_2"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 5,
              "firing_threshold" : 1,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 10,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 3,
              "snooze_length" : 0,
              "block_boundaries" : [
                  1,
                  1,
                  300
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      1
                  ],
                  "y" : [
                      0,
                      1
                  ],
                  "z" : [
                      0,
                      300
                  ]
              }
          }
      },
      "utf8_memory" : {
          "growth_path" : "",
          "group_id" : "Memory",
          "sub_group_id" : "utf8",
          "plot_index" : 2,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 300,
          "location_generation_type" : "sequential",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 11.2,
          "plasticity_constant" : 1,
          "postsynaptic_current_max" : 11.2,
          "neighbor_locator_rule_id" : "rule_0",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {
              "utf8_out" : {
                  "neighbor_locator_rule_id" : "rule_3",
                  "neighbor_locator_rule_param_id" : "param_2"
              }
          },
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 20,
              "firing_threshold" : 20,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 5,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 100000,
              "snooze_length" : 2,
              "block_boundaries" : [
                  1,
                  1,
                  300
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      1
                  ],
                  "y" : [
                      0,
                      1
                  ],
                  "z" : [
                      0,
                      300
                  ]
              }
          }
      },
      "utf8_out" : {
          "growth_path" : "",
          "group_id" : "OPU",
          "sub_group_id" : "OPU_utf8",
          "plot_index" : 1,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 300,
          "location_generation_type" : "sequential",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 0.51,
          "plasticity_constant" : 0.05,
          "postsynaptic_current_max" : 1,
          "neighbor_locator_rule_id" : "rule_0",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {},
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 20,
              "firing_threshold" : 10,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 1,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 1,
              "snooze_length" : 0,
              "block_boundaries" : [
                  1,
                  1,
                  300
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      1
                  ],
                  "y" : [
                      0,
                      1
                  ],
                  "z" : [
                      0,
                      300
                  ]
              }
          }
      },
      "pain" : {
          "growth_path" : "",
          "group_id" : "PAIN",
          "sub_group_id" : "pain",
          "plot_index" : 1,
          "orientation_selectivity_pattern" : "",
          "location" : "",
          "kernel_size" : 7,
          "cortical_neuron_count" : 5,
          "location_generation_type" : "sequential",
          "synapse_attractivity" : 100,
          "init_synapse_needed" : False,
          "postsynaptic_current" : 0.51,
          "plasticity_constant" : 0.05,
          "postsynaptic_current_max" : 1,
          "neighbor_locator_rule_id" : "rule_0",
          "neighbor_locator_rule_param_id" : "param_1",
          "cortical_mapping_dst" : {},
          "neuron_params" : {
              "activation_function_id" : "",
              "orientation_selectivity_id" : "",
              "depolarization_threshold" : 20,
              "firing_threshold" : 10,
              "firing_pattern_id" : "",
              "refractory_period" : 0,
              "axon_avg_length" : "",
              "leak_coefficient" : 1,
              "axon_avg_connections" : "",
              "axon_orientation function" : "",
              "consecutive_fire_cnt_max" : 1,
              "snooze_length" : 0,
              "block_boundaries" : [
                  1,
                  1,
                  1
              ],
              "geometric_boundaries" : {
                  "x" : [
                      0,
                      1
                  ],
                  "y" : [
                      0,
                      1
                  ],
                  "z" : [
                      0,
                      5
                  ]
              }
          }
      }
  }
}


gene_list = [['blueprint'][''], True]


def pick_a_key(dictionary):
    return random.choice(list(dictionary))


# for _ in range(20):
#
#     chosen_key = pick_a_key(a)
#     print("..", chosen_key)
#     path =
#     while type(a[chosen_key]) == dict:
#         print(">", chosen_key)
#         chosen_key = pick_a_key(a[chosen_key])
#         print(">", chosen_key)
#
#     print(">>>", chosen_key)
