#!/usr/bin/env python3

import sys
from .fetch import ld_matrix

def main(argc, argv):

    if argc < 5:
        print("usage: ld endpoint summary-statistics.tsv population output-directory [snp_field] [batch_size]", file = sys.stderr)
        return 1
    
    field = int(argv[5]) if argc >= 5 else 0
    batch_size = int(argv[6]) if argc >= 6 else 100
    with open(argv[2], 'r') as f:
        lines = [ x for x in f if not x.startswith("#") ]
    snps = group(
        lines,
        lambda x: x.strip().split()[0],
        lambda x: x.strip().split()[field]
    )

    os.system("mkdir -p %s" % argv[4])
    for k, v in snps.items():
        print("\nworking on chromosome %s" % k, file = sys.stderr)
        with open(os.path.join(argv[4], k + ".ld.txt"), 'w') as o:
            for percentage, batch in ld_matrix(argv[1], v, argv[3], batch_size):
                print("%.3f%% complete\r" % percentage, file = sys.stderr)
                o.write("\t".join([ str(x) for x in batch ]) + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
