#!/usr/bin/env python

import sys
import os
import math
import tempfile

class LDBlocks:

    def __init__(self, sf, threshold):
        self.sf = sf
        self.threshold = threshold

    def __enter__(self):
        self.tempfile = tempfile.NamedTemporaryFile()
        count = 0
        with open(self.sf, 'r') as f:
            with tempfile.NamedTemporaryFile('wt') as o:
                for line in f:
                    if line[0] == '#': continue
                    if -math.log10(float(line.strip().split()[-2])) < self.threshold: continue
                    count += 1
                    s = int(line.strip().split()[2]) - 1000000
                    o.write("chr%s\t%d\t%d\n" % (line.strip().split()[0], s if s > 0 else 0, int(line.strip().split()[2]) + 1000000))
                o.flush()
                with tempfile.NamedTemporaryFile('rt') as b:
                    os.system("sort -k1,1 -k2,2n %s | bedtools merge -i - > %s" % (o.name, b.name))
                    i = 0
                    with open(self.tempfile.name, 'wt') as oo:
                        for line in b:
                            oo.write("%s\t%d\n" % (line.strip(), i))
                            i += 1
                        oo.flush()
        return self.tempfile

    def __exit__(self, *args):
        self.tempfile.close()
