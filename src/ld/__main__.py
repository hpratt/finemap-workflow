#!/usr/bin/env python3

import sys
from .fetch import ld_matrix

def main(argc, argv):

    if argc < 4:
        print("usage: ld endpoint summary-statistics.tsv population [snp_field] [batch_size] > output.ld.txt", file = sys.stderr)
        return 1
    
    field = int(argv[4]) if argc >= 5 else 0
    batch_size = int(argv[5]) if argc >= 6 else 100
    with open(argv[2], 'r') as f:
        snps = list({ line.strip().split()[field] for line in f if not line.startswith("#") })
    
    for percentage, batch in ld_matrix(argv[1], snps, argv[3], batch_size):
        print("%.3f%% complete\r" % percentage, file = sys.stderr)
        print("\t".join([ str(x) for x in batch ]))
    
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
