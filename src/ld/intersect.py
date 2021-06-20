#!/usr/bin/env python

import os
import tempfile

class IntersectedSummaryStatistics:

    def __init__(self, sf, b):
        self.sf = sf
        self.b = b

    def __enter__(self):
        self.tempfile = tempfile.NamedTemporaryFile('rt')
        with tempfile.NamedTemporaryFile('wt') as o:
            with open(self.sf, 'r') as f:
                for line in f:
                    if line[0] == '#': continue
                    o.write("chr%s\t%d\t%d\t%s\n" % (line.strip().split()[0], int(line.strip().split()[2]), int(line.strip().split()[2]) + 1, line.strip()))
            o.flush()
            with tempfile.NamedTemporaryFile('rt') as f:
                with open(self.tempfile.name, 'wt') as oo:
                    os.system("bedtools intersect -a %s -b %s -wa -wb | sort | uniq > %s" % (o.name, self.b, f.name))
                    for line in f:
                        oo.write("\t".join(line.strip().split()[3:]) + "\n")
                    oo.flush()
        return self.tempfile

    def __exit__(self, *args):
        self.tempfile.close()
