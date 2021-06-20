#!/usr/bin/env python3

import os
import sys
import math

from .fetch import ld_matrix
from .group import group
from .block import LDBlocks
from .intersect import IntersectedSummaryStatistics

def main(argc, argv):

    if argc < 5:
        print("usage: ld endpoint summary-statistics.tsv population output-directory [threshold] [snp_field] [batch_size]", file = sys.stderr)
        return 1

    threshold = float(argv[5]) if argc >= 6 else 7.3
    field = int(argv[6]) if argc >= 7 else 1
    batch_size = int(argv[7]) if argc >= 8 else 100
    with LDBlocks(argv[2], threshold) as l:
        with IntersectedSummaryStatistics(argv[2], l.name) as f:
            lines = [ x for x in f if len(x.strip().split()) >= 11 ]
    linemap = { x.strip().split()[field]: x.strip().split() for x in lines }
    snps = group(
        lines,
        lambda x: x.strip().split()[-1],
        lambda x: x.strip().split()[field]
    )

    print("found %d LD blocks" % len(snps), file = sys.stderr)
    os.system("mkdir -p %s" % argv[4])
    for k, v in snps.items():
        print("\nworking on LD block %s (%d SNPs)" % (k, len(v)), file = sys.stderr)
        with open(os.path.join(argv[4], k + ".z"), 'w') as o:
            o.write("rsid chromosome position allele1 allele2 maf beta se\n")
            for snp in v:
                x = linemap[snp]
                if float(x[5]) > 0.5: x[5] = str(1 - float(x[5]))
                x[9] = str(math.log(float(x[9])))
                o.write("%s %s %s %s %s %s %s %s\n" % (x[1], x[0], x[2], x[3], x[4], x[5], x[9], x[10]))
        with open(os.path.join(argv[4], k + ".ld"), 'w') as o:
            for percentage, batch in ld_matrix(argv[1], v, argv[3], batch_size):
                print("%.4f%% complete\r" % (percentage * 100), end = "", file = sys.stderr)
                o.write("\n".join([ " ".join([ str(xx) for xx in x ]) for x in batch ]) + "\n")
            print("100% complete\n", file = sys.stderr)
    
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
