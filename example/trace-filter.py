#!/usr/bin/python3

import sys
import os

""" 
Used to strip instruction address that below 0x8000000
"""

def main(filename):
    with open(filename, "r") as f:
        trace = f.readlines()
        del trace[0]
        del trace[-1]

    trace_new = []
    for i in trace:
        mode, priv, tick, addr, inst = i.split()
        addr_tmp = int(addr, 16)
        if addr_tmp >= 0x0000000080000000:
            trace_new.append("{} {} {} {} {}\n".format(mode, priv, tick, addr, inst))
            
    
    with open(os.path.basename(filename) + "-filtered", "w") as f:
        f.writelines(trace_new)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("give inputs like python3 trace.txt")
    main(sys.argv[1])