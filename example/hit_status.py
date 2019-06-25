#!/usr/bin/python3

import json
import sys


sys.path.append("..")
sys.path.append(".")

from verilog_vcd import verilog_vcd
import bitarray
import json
import pickle

number_sets = 64
number_ways = 4

DEBUG_MODE = True

def find_cache_hit(meta_idx, tag, cache_trace_status, is_boom_orignal: bool):
    hit_status = []
    if is_boom_orignal:

        #TODO: Implementate boom origin cache dump function.

        return
    else:
        for i in cache_trace_status:
            tsc = i[0]
            cache_status = i[1]
            commit_addr = i[2]
            hit_set = cache_status[str(meta_idx)]
            s1_dc_bypass = True if cache_status.get('s1_dc_bypass') == '1' else False
            s1_load_retry = True if cache_status.get('s1_load_retry') == '1' else False
            for way in hit_set:
                s_valid = True if hit_set.get(way).get('s') == '1' else False
                if tag == hit_set.get(way).get('tag[19:0]') and (not s_valid or (s1_dc_bypass and s1_load_retry)):
                    hit_status.append("commit inst: {} tsc:{} hit set:{} way:{}".format(hex(commit_addr), tsc, meta_idx, way))
        return hit_status

def main():
    cache_trace = {}
    if not DEBUG_MODE:
        if len(sys.argv) != 3:
            raise Exception("give inputs like python3 hit_status.py 0x800000 trace-dump.pickle")
    
        with open(sys.argv[2], "rb") as f:
            cache_trace = pickle.load(f)
    else:
        with open("/home/wyanzhao/Workspace/python-vcd/dump-vcd.pickle", "rb") as f:
            cache_trace = pickle.load(f)

    if not DEBUG_MODE:
        inst_addr = sys.argv[1]
    else:
        inst_addr = "80002678"
    inst_addr = int(inst_addr, 16)
    
    if inst_addr.bit_length() != 32:
       raise Exception("Length of inst addr is wrong, needs 32 bit, you gave{}".format(inst_addr.bit_length()))
    inst_bin = bitarray.bitarray(bin(inst_addr).lstrip("-0b"))
    meta_idx = inst_bin[-12:-6]
    tag = bin(inst_addr >> 12).lstrip("-0b")

    meta_idx = int(meta_idx.to01(), 2)

    hit_status = find_cache_hit(meta_idx, tag, cache_trace, False)
    with open("hit_status.txt", "w") as f:
        for i in hit_status:
            f.write(i + "'\n")

    return 0

if __name__ == "__main__":
    main()