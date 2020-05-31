# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
# library to read a character from keyboard and have it converted to neuron firing

from configuration import runtime_data


def convert_char_to_fire_list(char):
    utf_value = ord(char)
    fire_set = set()
    for key in runtime_data.brain["utf8"]:
        if utf_value == runtime_data.brain["utf8"][key]['soma_location'][0][2]:
            fire_set.add(key)
    return fire_set
