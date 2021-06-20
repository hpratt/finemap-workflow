#!/usr/bin/env python3

def group(x, k, t):
    r = {}
    for x in r:
        kk = k(x)
        if kk not in r: r[kk] = []
        r[kk].append(t(x))
    return r
