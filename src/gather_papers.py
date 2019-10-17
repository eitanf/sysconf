#!/usr/bin/env python3
#
# This script reads in all conference files, paper files, and auxiliary data,
# and produces a tidy output table with one row per paper.
# A separate file holds a table of citations, with multiple rows per paper.
# It also produces two mapping tables, one for topics and one for content_tags

import re
import tidydata
import sys
from shared_utils import *

today = dt.today().strftime("%Y-%m-%d")

tidy_papers = tidydata.TidyData("papers",
        "Features relating to each paper in the set.")
tidy_cites = tidydata.TidyData("citations",
        "A mapping from papers to GS citations over time.")
tidy_topics = tidydata.TidyData("topics",
        "A mapping from papers to systems subfields (topics).")
tidy_tags = tidydata.TidyData("content_tags",
        "A mapping from papers to content tags.")


#########################################################################
# Add features that arise from parsing the paper's title
def add_title_features(title):
    subtitle = re.search("(:\s)|(\s-\s)|(;\s)|(\?\s)|(!\s)", title) != None
    tidy_papers.add("subtitle", "bool", subtitle,
            "Whether the title composed of two parts, separated by punctuation such as colon or question mark")

    labeled_title = re.search("^\w+:\s", title) != None
    tidy_papers.add("labeled_title", "bool", labeled_title,
            "Whether the title consists of a single word, followed by a colon and a subtitle")

    title_len = len(re.findall("\w+", title))
    tidy_papers.add("title_length", "int", title_len,
            "Number of words in title")


#########################################################################
# Add statistics from the Semantic Scholar record for the paper
def add_s2_features(s2):
    if 'outCitations' in s2 and len(s2['outCitations']) > 0:
        oc = len(s2['outCitations'])
    else:
        oc = ''

    tidy_papers.add("references", "int", oc,
            "Number of papers cited in this one (underestimated by S2)")

    ents = ";".join(s2['entities']) if 'entities' in s2 else ''
    tidy_papers.add("entities", "list of strings", ents,
            "Terms extracted from Semantic Scholar's paper data")


#########################################################################
# Add GS statistics from the data/papers record
def add_gs_features(key, record, post):
    pf = record['paper_found']
    tidy_papers.add("months_to_gs", "int", month_diff(pf, post) if pf != "" else "",
            "Months from publication till GS showed a record for paper")

    ef = record['eprint_found']
    tidy_papers.add("months_to_eprint", "int", month_diff(ef, post) if ef != "" else "",
            "Months from publication till GS found an e-print")

    for date,cites in record['citedby'].items():
        tidy_cites.start_record()
        tidy_cites.add("key", "string", key, "Paper ID")
        tidy_cites.add("date", "date", date, "Dated this citation count was collected")
        tidy_cites.add("citations", "int", cites, "Total citations for this paper on this date")


#########################################################################
# output data from the conference's paper records
def add_paper_record(key, record):
    tidy_papers.add("words", "int", record['words'],
            "Approximate number of words")

    authors = [ normalized_author_name(author_name(p)[0]) for p in record['authors'] ]
    tidy_papers.add("alphabetized", "bool", authors == sorted(authors) and len(authors) > 1,
            "Whether author list sorted in alphabetical order for multi-author papers")

    if 'topics' in record:
        for topic in record['topics']:
            tidy_topics.start_record()
            tidy_topics.add("key", "string", key, "Paper ID")
            tidy_topics.add("topic", "categorical string", topic,
                    "A topic that the paper relates to")


    if 'content_tags' in record:
        for tag in record['content_tags']['manual']:
            tidy_tags.start_record()
            tidy_tags.add("key", "string", key, "Paper ID")
            tidy_tags.add("tag", "categorical string", tag,
                    "A content descriptor for the paper's research")


#########################################################################
# Extract all variables available from conference file.
# The fields are grouped (in the source-code only) based on the main
# variable in the data/conf/ file that is responsible to generate them.
def add_paper_vars(conf, s2data, papers):
    post = conf['postdate']

    for p in conf['papers']:
        key = p['key']
        tidy_papers.start_record()

        # Data from conf file:
        tidy_papers.add("key", "string", key, "Paper ID (unique)")
        add_paper_record(key, p)

        # GS record stats:
        add_gs_features(key, papers[key], post)

        # Features related to the title of the paper:
        add_title_features(p['title'])

        # Features related to the Semantic Scholar record of the paper:
        if p['s2pid'] in s2data:
            add_s2_features(s2data[p['s2pid']])


#########################################################################
# main

if len(sys.argv) < 2:
    print("Arguments: conference name(s)")
    exit(-1)


for conf in sys.argv[1:]:
    print("Processing:", conf)
    confdata = load_json_file(data_fn('conf', conf))
    s2data = load_json_file("data/s2papers.json")
    paperdata = load_json_file(data_fn('papers', conf))

    add_paper_vars(confdata, s2data, paperdata)

tidy_papers.save()
tidy_cites.save()
tidy_topics.save()
tidy_tags.save()
