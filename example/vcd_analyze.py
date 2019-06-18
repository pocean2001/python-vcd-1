#!/usr/bin/python3

import sys

sys.path.append("..")
sys.path.append(".")

import verilog_vcd
import json

number_sets = 64
number_ways = 4

DEBUG_MODE = True

def main():
        if not DEBUG_MODE:
            if len(sys.argv) != 5:
                raise Exception("give inputs like python3 vcd_analyze.py import_signals inst.txt xx.vcd trace-dump.json")

        inst_stat_list = []
        if not DEBUG_MODE:
            signal_list = verilog_vcd.import_signals(sys.argv[1])
            insts, seed = verilog_vcd.parse_commit_log(sys.argv[2])
            vcd_json = verilog_vcd.parse_vcd(sys.argv[3], siglist=signal_list)
        else:
            signal_list = verilog_vcd.import_signals("/home/wyanzhao/Workspace/python-vcd/example/boom_signals")
            insts, seed = verilog_vcd.parse_commit_log("/home/wyanzhao/Workspace/boom-template/verisim/void.txt")
            try:
                with open("void.vcd", "r") as f:
                    vcd_json = json.load(f)
            except FileNotFoundError:
                vcd_json = verilog_vcd.parse_vcd('/home/wyanzhao/Workspace/boom-template/verisim/void.vcd', siglist=signal_list)
                with open("void.vcd", "w") as f:
                    json.dump(vcd_json ,f)

        if not DEBUG_MODE:
            for inst in insts:
                tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_json)
                signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_json)
                inst_stat_list.append((int(tsc, 2), signal_stat))
        else:
            try:
                with open("inst_stat_list.json", "r") as f:
                    inst_stat_list = json.load(f)
            except FileNotFoundError:
                for inst in insts:
                    tick, tsc = verilog_vcd.search_time(inst.get("count"), vcd_json)
                    signal_stat = verilog_vcd.search_stat(tick, signal_list, vcd_json)
                    inst_stat_list.append((int(tsc, 2), signal_stat))
                    with open("inst_stat_list.json", "w") as f:
                        json.dump(inst_stat_list, f)
        

        
        cache_statuses = []
        for i in inst_stat_list:
                cache_status = {}
                tsc = i[0]
                for j in i[1]:
                    if j != "TOP.TestHarness.dut.tile.dcache.s1_load_retry" and  j != "TOP.TestHarness.dut.tile.dcache.s1_dc_bypass" and j != "TOP.TestHarness.dut.tile.core.debug_tsc_reg[63:0]":
                        _, _, _, cache_set, cache_way, *_ = j.split("_")
                        if cache_set not in cache_status:
                            cache_status[cache_set] = {}
                        cache_status[cache_set][cache_way] = i[1].get(j)
                    else:
                        cache_status[j] = i[1].get(j)

                cache_statuses.append((tsc, cache_status))

        if len(inst_stat_list) != len(cache_statuses):
                raise Exception("trace_status != cache_statuses, len prior:{}, len aftr{}"\
                        .format(len(inst_stat_list), len(cache_statuses)))

        if not DEBUG_MODE:
            with open(sys.argv[4], "w") as f:
                json.dump(cache_statuses, f)
                print("Dump trace status succeed")
        else:
            with open("dump-vcd.json", "w") as f:
                json.dump(cache_statuses, f)
                print("Dump trace status succeed")

if __name__ == "__main__":
        main()