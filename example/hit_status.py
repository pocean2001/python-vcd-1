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

DEBUG_MODE = False

def find_cache_hit(meta_idx, tag, cache_trace_status, is_boom_orignal: bool):
    hit_status = []
    tag_hash = hash(tag)

    for i in cache_trace_status:
        (tsc, cache_status, commit_addr, s1_load_retry, s1_dc_bypass) = i
        hit_set = cache_status[meta_idx]
        for way in range(number_ways):
            if is_boom_orignal:   
                if tag_hash == hash(hit_set[way].get('tag[19:0]')):
                    hit_status.append("commit inst: {} tsc:{} hit set:{} way:{}".format(hex(commit_addr), hex(tsc), meta_idx, (way)))
            else:
                s_valid = True if hit_set[way].get('s') == '1' else False
                if tag_hash == hash(hit_set[way].get('tag[19:0]')) and (not s_valid or (s1_dc_bypass and s1_load_retry)):
                    hit_status.append("commit inst: {} tsc:{} hit set:{} way:{}".format(hex(commit_addr), hex(tsc), (meta_idx), (way)))
                
    return hit_status

def main():
    cache_trace = {}
    using_boom_raw = False

    if not DEBUG_MODE:
        if len(sys.argv) != 5:
            raise Exception("give inputs like python3 hit_status.py 80002c60 trace-input.pickle true cache-output.txt")

        print("input inst addr checked: {}".format(sys.argv[1]))
        print("input dump file: {}".format(sys.argv[2]))
        if sys.argv[3] == 'True':
            using_boom_raw = True
        else:
            using_boom_raw = False

        print("input if is_boom_orignal: {}".format(using_boom_raw))
        print("output trace dump file: {}".format(sys.argv[4]))
    
        with open(sys.argv[2], "rb") as f:
            cache_trace = pickle.load(f)
            f.close()

    else:
        with open("/home/wyanzhao/Workspace/python-vcd/dump-vcd.pickle", "rb") as f:
            cache_trace = pickle.load(f)
            f.close()

    if not DEBUG_MODE:
        inst_addr = sys.argv[1]
    else:
        inst_addr = "80002c60"
    #TODO: inst_addr

    inst_addr = int(inst_addr, 16)
    print("inst addr:{}".format(hex(inst_addr)))
    
    if inst_addr.bit_length() != 32:
       raise Exception("Length of inst addr is wrong, needs 32 bit, you gave {}".format(inst_addr.bit_length()))
    inst_bin = bitarray.bitarray(bin(inst_addr).lstrip("-0b"))
    meta_idx = inst_bin[-12:-6]
    tag = bin(inst_addr >> 12).lstrip("-0b")

    meta_idx = int(meta_idx.to01(), 2)

    if not DEBUG_MODE:
        hit_status = find_cache_hit(meta_idx, tag, cache_trace, using_boom_raw)
        with open(sys.argv[4], "w") as f:
            for i in hit_status:
                f.write(i + "\n")
            f.close()
    else:
        hit_status = find_cache_hit(meta_idx, tag, cache_trace, False)
        with open("void_cache-out.txt", "w") as f:
            for i in hit_status:
                f.write(i + "\n")
            f.close()

    print("cache hit status dump succeed")
    return 0

if __name__ == "__main__":
    main()