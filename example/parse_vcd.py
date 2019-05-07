#!/usr/bin/python3

import json
import sys

sys.path.append("..")

from verilog_vcd import verilog_vcd

signal_name = [
    "tag_array_0_s1_meta_addr[5:0]",
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

signal_list = []
for i in signal_name:
    signal_list.append("TOP.TestHarness.dut.tile.dcache." + i)

signal_list.append("TOP.TestHarness.dut.tile.core.debug_tsc_reg[63:0]")


def main():
    if len(sys.argv) != 3:
        raise Exception("give inputs like python3 parse_vcd.py boom.vcd boom-signal.json")

    vcd = verilog_vcd.parse_vcd(sys.argv[1], siglist=signal_list)
    vcd_json = json.dumps(vcd)
    with open(sys.argv[2], "w") as f:
        f.write(vcd_json)


if __name__ == "__main__":
    main()
