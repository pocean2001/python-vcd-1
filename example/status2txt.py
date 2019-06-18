#!/usr/bin/python3

import json
import sys

sys.path.append("..")
sys.path.append(".")

def main():
    if len(sys.argv) != 3:
        raise Exception("give inputs like python3 status2txt.py trace-dump.json trace-dump.txt")

    with open(sys.argv[1], "r") as f:
        signal_status = json.load(f)
    """ with open("./example/void-trace.json", "r") as f:
        signal_status = json.load(f) """
    
    inst_list = []

    for i in signal_status:
        for j in i[1]:
            a = j
            b = i[1].get(j)
            tmp = int(b, 2)
            if (tmp >= 0x80000 and tmp <= 0x80003):
                inst_list.append(a + str(b))

    with open(sys.argv[2], "w'") as f:
        f.write(str(inst_list))



if __name__ == "__main__":
    main()