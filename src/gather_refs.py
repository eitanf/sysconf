#!/usr/bin/env python3
#
# This script reads in all the data for a given conference from data/, then
# iterates over all papers and tries to read in the references section for the
# paper out of data/fulltext/refs. Then, it heuristically estimates how many
# of these references are self-citations by grepping for all the authors'
# last names in the references file.
# It saves this as a tidy data file called features/refcounts.csv

import re
import tidydata
import sys
from shared_utils import *

tidy_refs = tidydata.TidyData("ref_counts",
        "A mapping from papers to the estimated number of self-citations in its bibliography")


#########################################################################
# Compute all self-references for a given paper key and author list
# Returns also the total number of references found.
def compute_self_refs(key, authors):
    total = 0
    refs = -1  # First "line" is always empty
    pattern = "\\[\\d{1,3}\\]"

    last_names = [normalized_author_name(a).split(',')[0].lower() for a in authors]
    with open(f"fulltext/refs/{key}.txt") as file:
        bib = file.read()
        indices = [0] + [ int(s[1:-1]) for s in re.findall(pattern, bib) ]
        for line in re.split(pattern, bib):
            refs += 1
            assert indices[refs] == refs, f"Read reference {indices[refs]} but expected {refs} in paper {key}!"
            total += any([re.search("\\b"+last+"\\b", line.lower()) is not None for last in last_names])
#            print(f"[[{refs}]], {line}: total: {total}, last_names: {last_names}")

    assert refs == indices[-1], f"Last reference {indices[-1]} doesn't match number of reference lines {refs} for paper {key}"
    return total, refs

#########################################################################
# Compute all self-references for all papers in a given conference.
def add_refs(conf):
    for p in conf['papers']:
        key = p['key']
        tidy_refs.start_record()
        tidy_refs.add("key", "string", key, "Paper ID")

        self_refs, total_refs = compute_self_refs(key, p['authors'])
        tidy_refs.add("self_refs", "int", self_refs, "Total self-references to authors in bibliography")
        tidy_refs.add("total_refs", "int", total_refs, "Total references found in bibliography")


#########################################################################
# main

if len(sys.argv) < 2:
    print("Arguments: conference name(s)")
    exit(-1)


for conf in sys.argv[1:]:
    print("Processing:", conf)
    confdata = load_json_file(data_fn('conf', conf))
    add_refs(confdata)

tidy_refs.save()
