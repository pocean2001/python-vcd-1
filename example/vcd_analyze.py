#!/usr/bin/python3

import sys

sys.path.append("..")
sys.path.append(".")

import verilog_vcd
import json
import pickle

number_sets = 64
number_ways = 4

DEBUG_MODE = True

def main():
    if not DEBUG_MODE:
        if len(sys.argv) != 5:
            raise Exception("give inputs like python3 vcd_analyze.py import_signals inst.txt xx.vcd trace-dump.pickle")

    inst_stat_list = []
    if not DEBUG_MODE:
        signal_list = verilog_vcd.import_signals(sys.argv[1])
        insts, seed = verilog_vcd.parse_commit_log(sys.argv[2])
        vcd_obj = verilog_vcd.parse_vcd(sys.argv[3], siglist=signal_list)
    else:
        signal_list = verilog_vcd.import_signals("/home/wyanzhao/Workspace/python-vcd/example/boom_signals.json")
        insts, seed = verilog_vcd.parse_commit_log("/home/wyanzhao/Workspace/boom-template/verisim/void-inst.txt")
        try:
            with open("void-vcd.pickle", "rb") as f:
                vcd_obj = pickle.load(f)
        except FileNotFoundError:
            vcd_obj = verilog_vcd.parse_vcd('/home/wyanzhao/Workspace/boom-template/verisim/void.vcd', siglist=signal_list)
            with open("void-vcd.pickle", "wb") as f:
                pickle.dump(vcd_obj ,f)

    if not DEBUG_MODE:
        for inst in insts:
            tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_obj)
            signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_obj)
            inst_stat_list.append((int(tsc, 2), signal_stat))
    else:
        try:
            with open("inst_stat_list.pickle", "rb") as f:
                inst_stat_list = pickle.load(f)
        except FileNotFoundError:
            for inst in insts:
                tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_obj)
                signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_obj)
                inst_stat_list.append((int(tsc, 2), signal_stat, int(inst.get('addr'))))
            with open("inst_stat_list.pickle", "wb") as f:
                pickle.dump(inst_stat_list, f)
        
    cache_statuses = []
    for i in inst_stat_list:
            cache_status = {}
            tsc = i[0]
            inst_addr = i[2]
            for j in i[1]:
                if j != "TOP.TestHarness.dut.tile.dcache.s1_load_retry" and  j != "TOP.TestHarness.dut.tile.dcache.s1_dc_bypass" and  j != "TOP.TestHarness.dut.tile.core.debug_tsc_reg[63:0]":
                    _, _, _, cache_set, cache_way, other, *_ = j.split("_")
                    if cache_set not in cache_status:
                        cache_status[cache_set] = {}
                    if cache_way not in cache_status[cache_set]:
                        cache_status[cache_set][cache_way] = {}
                    cache_status[cache_set][cache_way][other] = i[1].get(j)
                elif j == "TOP.TestHarness.dut.tile.dcache.s1_load_retry":
                    cache_status["s1_load_retry"] = i[1].get(j)
                elif j == "TOP.TestHarness.dut.tile.dcache.s1_dc_bypass":
                    cache_status["s1_dc_bypass"] = i[1].get(j)
                else:
                    continue

            cache_statuses.append((tsc, cache_status, inst_addr))

    if len(inst_stat_list) != len(cache_statuses):
            raise Exception("trace_status != cache_statuses, len prior:{}, len after{}"\
                .format(len(inst_stat_list), len(cache_statuses)))

    if not DEBUG_MODE:
        with open(sys.argv[4], "wb") as f:
            pickle.dump(cache_statuses, f)
    else:
        with open("dump-vcd.pickle", "wb") as f:
            pickle.dump(cache_statuses, f)
    print("Dump trace status succeed")

if __name__ == "__main__":
        main()