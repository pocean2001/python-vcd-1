#!/usr/bin/python3

import sys

sys.path.append("..")

from verilog_vcd import vcd_analyzer

signal_list = ["tag_array_0_s1_meta_addr[5:0]",
"tag_array_0_s1_meta_data[22:0]",
"tag_array_1_s1_meta_addr[5:0]",
"tag_array_1_s1_meta_data[22:0]",
"tag_array_2_s1_meta_addr[5:0]",
"tag_array_2_s1_meta_data[22:0]",
"tag_array_3_s1_meta_addr[5:0]",
"tag_array_3_s1_meta_data[22:0]",
"tag_array_4_s1_meta_addr[5:0]",
"tag_array_4_s1_meta_data[22:0]",
"tag_array_5_s1_meta_addr[5:0]",
"tag_array_5_s1_meta_data[22:0]",
"tag_array_6_s1_meta_addr[5:0]",
"tag_array_6_s1_meta_data[22:0]",
"tag_array_7_s1_meta_addr[5:0]",
"tag_array_7_s1_meta_data[22:0]"
]


def main():
        if len(sys.argv) != 3:
                raise Exception("give inputs like python3 vcd_analyzer.py boom-inst.txt boom-signal.json")
        else:
                inst_stat_list = []
                insts, seed = vcd_analyzer.parse_commit_log(sys.argv[1])
                signal_json = vcd_analyzer.import_json(sys.argv[2])

                for inst in insts:
                        tick = vcd_analyzer.search_time(inst.get("count"), signal_json)
                        signal_stat = vcd_analyzer.search_stat(tick, signal_list, signal_json)
                        inst_stat_list.append((tick, signal_stat))
                print(inst_stat_list)

if __name__ == "__main__":
        main()