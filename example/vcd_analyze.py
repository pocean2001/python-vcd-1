#!/usr/bin/python3

import sys

sys.path.append("..")
sys.path.append(".")

import json
import pickle
import gc

import verilog_vcd

number_sets = 64
number_ways = 4

DEBUG_MODE = False

def main():
    if not DEBUG_MODE:
        if len(sys.argv) != 5:
            raise Exception("give inputs like python3 vcd_analyze.py import_signals inst.txt xx.vcd trace-dump.pickle")

    if not DEBUG_MODE:
        print("signal_list:{}".format(sys.argv[1]))
        print("commit sequences file:{}".format(sys.argv[2]))
        print("vcd file:{}".format(sys.argv[3]))
        print("dump file:{}".format(sys.argv[4]))
        signal_list = verilog_vcd.import_signals(sys.argv[1])
        insts, seed = verilog_vcd.parse_commit_log(sys.argv[2])
        vcd_obj = verilog_vcd.parse_vcd(sys.argv[3], siglist=signal_list)
    else:
        signal_list = verilog_vcd.import_signals("/home/wyanzhao/Workspace/python-vcd/example/boom_signals.json")
        insts, seed = verilog_vcd.parse_commit_log("/home/wyanzhao/Workspace/boom-template/verisim/void.txt")
        try:
            with open("void-vcd.pickle", "rb") as f:
                vcd_obj = pickle.load(f)
                f.close()
        except FileNotFoundError:
            vcd_obj = verilog_vcd.parse_vcd('/home/wyanzhao/Workspace/boom-template/verisim/void.vcd', siglist=signal_list)
            with open("void-vcd.pickle", "wb") as f:
                pickle.dump(vcd_obj ,f)
                f.close()

    print("Import files and parse vcd finished")
    gc.collect()

    inst_stat_list = []
    if not DEBUG_MODE:
        for inst in insts:
                tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_obj)
                signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_obj)
                inst_stat_list.append((int(tsc, 2), signal_stat, int(inst.get('addr'))))
    else:
        try:
            with open("void_stat_list.pickle", "rb") as f:
                inst_stat_list = pickle.load(f)
                f.close()
        except FileNotFoundError:
            for inst in insts:
                tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_obj)
                signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_obj)
                inst_stat_list.append((int(tsc, 2), signal_stat, int(inst.get('addr'))))
            with open("void_stat_list.pickle", "wb") as f:
                pickle.dump(inst_stat_list, f)
                f.close()
    
    print("parse signals status finished")
    del signal_list, insts, vcd_obj
    gc.collect()

    cache_trace = []
    s1_load_retry_hash = hash("TOP.TestHarness.dut.tile.dcache.s1_load_retry")
    s1_dc_bypass_hash = hash("TOP.TestHarness.dut.tile.dcache.s1_dc_bypass")
    tsc_hash = hash("TOP.TestHarness.dut.tile.core.debug_tsc_reg[63:0]")

    for i in inst_stat_list:
            tsc, signal_stat, inst_addr = i
            cache = [[{} for _ in range(number_ways)] for _ in range(number_sets)]
            
            s1_load_retry = None
            s1_dc_bypass = None

            for signal_name in signal_stat:
                j_hash = hash(signal_name)
                if j_hash == s1_load_retry_hash:
                    s1_load_retry = bool(signal_stat.get(signal_name))
                elif j_hash == s1_dc_bypass_hash:
                    s1_dc_bypass = bool(signal_stat.get(signal_name))
                elif j_hash != tsc_hash:
                    _, _, _, cache_set, cache_way, other, *_ = signal_name.split("_")
                    cache_set = int(cache_set)
                    cache_way = int(cache_way)
                    cache[cache_set][cache_way][other] = signal_stat.get(signal_name)
                else:
                    continue
            cache_trace.append((tsc, cache, inst_addr, s1_load_retry, s1_dc_bypass))

    if len(inst_stat_list) != len(cache_trace):
            raise Exception("trace_status != cache_statuses, len prior:{}, len after{}"\
                .format(len(inst_stat_list), len(cache_trace)))

    print("parse cache status finished")
    del inst_stat_list
    gc.collect()

    if not DEBUG_MODE:
        with open(sys.argv[4], "wb") as f:
            pickle.dump(cache_trace, f)
            f.close()
    else:
        with open("dump-vcd.pickle", "wb") as f:
            pickle.dump(cache_trace, f)
            f.close()
    print("dump trace status succeed")

if __name__ == "__main__":
        main()