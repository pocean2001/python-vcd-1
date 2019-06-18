#!/usr/bin/python3

import json
import sys


sys.path.append("..")
sys.path.append(".")

from verilog_vcd import verilog_vcd
import bitarray
import json

number_sets = 64
number_ways = 4

def main():
    trace_status = {}

    if len(sys.argv) != 3:
        raise Exception("give inputs like python3 hit_status.py 0x800000 trace-dump.json")
    
    with open(sys.argv[2], "r") as f:
        trace_status = json.load(f)

    inst_addr = sys.argv[1]
    #inst_addr = "80002678"
    inst_addr = int(inst_addr, 16)
    
    if inst_addr.bit_length() != 32:
       raise Exception("Length of inst addr is wrong, needs 32 bit, you gave{}".format(inst_addr.bit_length()))
    inst_bin = bitarray.bitarray(bin(inst_addr).lstrip("-0b"))
    meta_idx = inst_bin[-12:-6]
    tag = bin(inst_addr >> 12).lstrip("-0b")

    meta_idx = int(meta_idx.to01(), 2)

    hit_status = []
    for i in trace_status:
        tsc = i[0]
        cache_status = i[1]
        hit_set = cache_status[str(meta_idx)]
        for way in hit_set:
            if tag == hit_set.get(way):
                hit_status.append("tsc: {} ways: {}".format(tsc, way))
    print(hit_status)

if __name__ == "__main__":
    main()