#!/usr/bin/env python3

import backoff
import requests
from typing import List, Dict

QUERY = """
  query batchQuery($snpids: [String], $population: Population!) {
      snpQuery(assembly: "GRCh38", snpids: $snpids) {
          id
          linkageDisequilibrium(population: $population) {
              id
              rSquared
          }
      }
  }
"""

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries = 64)
def fetch_ld(endpoint: str, batch: List[str], population: str) -> List[Dict[str, float]]:
    r = {

        # fetch a map of linked SNPs to correlation coefficients...
        x["id"]: {
            xx["id"]: xx["rSquared"]
            for xx in x["linkageDisequilibrium"]
        }

        # ...for each SNP that matched the query.
        for x in requests.post(endpoint, json = {
            "query": QUERY,
            "variables": { "snpids": batch, "population": population }
        }).json()["data"]["snpQuery"]

    }
    ordermap = { i: x for i, x in enumerate(batch) }
    return [ r[ordermap[i]] if ordermap[i] in r else {} for i in range(len(batch)) ]

def ld_matrix(endpoint: str, snps: List[str], population: str, batch_size: int = 100) -> List[List[float]]:
    for i in range(int(len(snps) / float(batch_size)) + 1):
        r = fetch_ld(endpoint, snps[i * batch_size : (i + 1) * batch_size], population)
        yield i * float(batch_size) / len(snps), [ [ x[xx] if xx in x else 0.0 for xx in snps ] for x in r ]
