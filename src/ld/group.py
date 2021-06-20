#!/usr/bin/env python3

def group(xx, k, t):
    r = {}
    for x in xx:
        kk = k(x)
        if kk not in r: r[kk] = []
        r[kk].append(t(x))
    return r
