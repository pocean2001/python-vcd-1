#!/usr/bin/python3

import json
import sys

sys.path.append("..")
sys.path.append(".")

from verilog_vcd import verilog_vcd

def main():
    if len(sys.argv) != 3:
        raise Exception("give inputs like python3 list_signals.py boom.vcd signal_dump.json")

    signals = verilog_vcd.list_sigs(sys.argv[1])
    signals_json = json.dumps(signals)
    with open(sys.argv[2], "w") as f:
        f.write(signals_json)   

if __name__ == "__main__":
    main()