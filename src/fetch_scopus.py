#!/usr/bin/env python3
#
# This script reads in a conference JSON file and paper data JSON file.
# It tries to match each conference paper to a best entry in Scopus
# then writes the entry data with current citations to the paper file.
# Alternatively, you could call `get_cites_for_conf` to get all year-end
# citations for a conference, with and without self citations

from datetime import datetime as dt
import sys
from shared_utils import *
from pybliometrics.scopus import *

today = dt.today()
today_year = today.year
todaystr = today.strftime("%Y-%m-%d")
scopus = {}

##############################################################################
# find_paper_record: search scopus for a record of a paper by title and year.
# Returns the EID of the first result if found.
# If more than one record is found, return None
def find_paper_record(title, year = 2017):
    global scopus

    query = 'TITLE("{}") AND DOCTYPE("cp") AND LIMIT-TO(PUBYEAR,{})'.format(title, year)
    res = ScopusSearch(query, subscriber=False)

    if res.get_results_size() != 1:
        print('For paper "', title, '" found', res.get_results_size(), 'results')
        print(res.get_eids())
        return None

    return res.get_eids()[0]


##############################################################################
# For a given paper ID and end year, look up all of its citations up to year,
# and return a pair of total citations and citations excluding self citations.
def get_cites_by_year(eid, year):
    sid = eid.split('-')[-1]
    total = CitationOverview([sid], start=2017, end=year)
    without_self = CitationOverview([sid], start=2017, end=year, citation="exclude-self", eid=None, refresh=True)
    return (total.cc[0], without_self.cc[0])


##############################################################################
# For a given conference, look up its existing records, and then for every
# paper that has an eid, fetch all citations (total and excluding self) for
# each year from 2017 to current.
# Record the data back to the JSON file.
def get_cites_for_conf(conf):
    confdata = load_json_file(data_fn('conf', conf))
    scopus = load_json_file("data/papers/scopus.json")

    for p in confdata['papers']:
        key = p['key']
        if key not in scopus:
            continue
        record = scopus[key]
        eid = record["eid"]

        (total, excluding_self) = get_cites_by_year(eid, today_year)
        record["total"] = { year: cites for (year, cites) in total }
        record["excluding_self"] = { year: cites for (year, cites) in excluding_self }
#        print(f"For paper {key} with ID {eid}, found {total} citations ({excluding_self} excluding self citations)")
        persistent_json_update("data/papers/scopus.json", key, record)


##############################################################################
######### main

# for conf in sys.argv[1:]:
#    get_cites_for_conf(conf)
#exit(1)

if len(sys.argv) != 2:
    print("Required parameter: conference name")
    exit(1)

conf = sys.argv[1]
confdata = load_json_file(data_fn('conf', conf))
scopus = load_json_file("data/papers/scopus.json")

# Main loop: gather paper info:
for p in confdata['papers']:
    key = p['key']
    print(key)
    ab = None

    if key not in scopus:         # No record for this key exists yet:
        eid = find_paper_record(p['title'])
        if eid == None:
            continue
        scopus[key] = { 'eid' : eid }

    record = scopus[key]
    eid = record['eid']

    if 'citedby' not in record:     # Record is empty, initialize:
        ab = AbstractRetrieval(eid)
        record = { \
            'eid'      : eid, \
            'title'    : ab.title, \
            'doi'      : ab.doi, \
            'citedby'  : {} \
        }
        scopus[key] = record

    if todaystr not in record['citedby']:
        if ab is None:
            ab = AbstractRetrieval(eid)
        record['citedby'][todaystr] = ab.citedby_count

    persistent_json_update("data/papers/scopus.json", key, record)
