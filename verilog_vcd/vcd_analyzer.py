#!/usr/bin/python3

import json
import logging

signal_name_cache = {}

def parse_commit_log(file):
    with open(file, "r") as f:
        seed = 0
        inst_list = []
        lines = f.readlines()
        for line in lines:
                items = [i for i in line.rstrip("\n").split()]

                """ get the ramdom seed"""
                if line == lines[0]:
                        seed =  int(items[3])
                else:
                        if items[0] == "i":
                                inst = {}
                                inst["type"] = "int"
                                inst["count"] = int(items[1])
                                inst["priv"] = int(items[2])
                                inst["addr"] = int(items[3], 16)
                                inst["inst"] = int(items[4], 16)
                                inst_list.append(inst)
                        elif items[0] == "o":
                                inst = {}
                                inst["type"] = "others"
                                inst["count"] = int(items[1])
                                inst["priv"] = int(items[2])
                                inst["addr"] = int(items[3], 16)
                                inst["inst"] = int(items[4], 16)
                                inst_list.append(inst)
        logging.info("seed:{}".format(seed))
        logging.info("first inst:{}".format(inst_list[0]))
    return inst_list, seed

def import_json(file_name):
    with open(file_name, "r") as f:
        signal_txt = f.read()
        signal_json = json.loads(signal_txt)
        return signal_json

def search_time(debug_tsc, signal_json):
    tsc_key = find_signal_key("debug_tsc_reg[63:0]", signal_json)
    tv_list = signal_json.get(tsc_key).get("tv")
    tick = tv_list[debug_tsc+1][0]
    return tick

def find_signal_key(signal_name, signal_json:dict):
    global signal_name_cache
    if signal_name_cache.get(signal_name, None) == None:
        for key, value in zip(signal_json.keys(), signal_json.values()):
            for i in range(len(value["nets"])):
                if value["nets"][i]["name"] == signal_name:
                    signal_name_cache[signal_name] = key
                    return key
    else:
        return signal_name_cache.get(signal_name)

def search_stat(time, signal_list, signal_json):
    def find_cache_stat(signal_vcd_name):
        tmp = signal_json.get(signal_vcd_name)
        tv_list = tmp.get("tv")
        low, high = 0, len(tv_list) - 1
        while low <= high:
                mid = int((low + high) / 2)
                if mid != len(tv_list) - 1:
                        if time < tv_list[mid][0]:
                                high = mid - 1
                        elif time >= tv_list[mid+1][0]:
                                low = mid + 1
                        else:
                                return tv_list[mid][1]
                else:
                        return tv_list[mid][1]
        return None

    signal_stat = {}
    for i in signal_list:
        signal_vcd_name = find_signal_key(i, signal_json)
        if signal_vcd_name == None:
            raise Exception("Can't find signal_name: {}".format(i))
        else:
            signal_stat[i] = find_cache_stat(signal_vcd_name)

    return signal_stat