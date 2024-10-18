#!/usr/bin/env python

import csv
import gzip
import json
import requests
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} genes_to_get.txt")
    print("Reads a list of genes from a file, one gene per line, and fetches data about them")
    sys.exit(0)

with gzip.open('gene_info.csv.gz', 'wt') as outfile:
    writer = csv.writer(outfile)
    header_written = False

    # Read in a list of genes to get information about
    for line in open(sys.argv[1]):
        # Make a request to get info about that gene from the API
        gene_name = line.strip()
        response = requests.get(f"https://bioindex.hugeamp.org/api/bio/query/gene-associations", params={'q': gene_name})
        gene_data = response.json()
        for record in gene_data['data']:
            if not header_written:
                writer.writerow(record.keys())
                header_written = True

            writer.writerow(record.values())