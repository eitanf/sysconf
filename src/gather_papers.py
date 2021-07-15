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
tidy_artifacts = tidydata.TidyData("artifacts",
        "A mapping from papers to artifact data.")

# Manually computed list of number of references per paper for those that
# don't have Semantic Scholar data.
refs_map = {
        'CIDR_17_004': 26, 'CIDR_17_029': 52,
        'HPCA_17_001': 38, 'HPCA_17_048': 75,
        'NDSS_17_002': 25, 'NDSS_17_005': 64, 'NDSS_17_013': 34,
        'NDSS_17_015': 45, 'NDSS_17_026': 25, 'NDSS_17_030': 57,
        'NDSS_17_033': 29, 'NDSS_17_034': 36, 'NDSS_17_040': 56,
        'NDSS_17_045': 57, 'NDSS_17_059': 30,
        'NSDI_17_009': 48,
        'ICPE_17_022': 41,
        'EuroSys_17_012': 53,
        'CCGrid_17_029': 49,
        'SIGMOD_17_010': 82,
        'PODS_17_006': 29,
        'IPDPS_17_092': 27,
        'SIGMETRICS_17_014': 34, 'SIGMETRICS_17_024': 45,
        'ISC_17_001': 46, 'ISC_17_003': 36, 'ISC_17_007': 27,
        'ISC_17_008': 26, 'ISC_17_011': 33, 'ISC_17_013': 13,
        'ISC_17_014': 33, 'ISC_17_015': 26, 'ISC_17_017': 20,
        'ISC_17_014': 33, 'ISC_17_015': 26, 'ISC_17_017': 20,
        'ISC_17_018': 28, 'ISC_17_020': 14,
        'CLOUD_17_016': 42,
        'HotStorage_17_006': 21,
        'PODC_17_020': 37, 'PODC_17_021': 15, 'PODC_17_022': 36,
        'PODC_17_024': 17, 'PODC_17_031': 14, 'PODC_17_034': 38,
        'ICPP_17_031': 22, 'ICPP_17_047': 26,
        'EuroPar_17_004': 12, 'EuroPar_17_006': 20, 'EuroPar_17_007': 19,
        'EuroPar_17_010': 20, 'EuroPar_17_011': 12, 'EuroPar_17_014': 24,
        'EuroPar_17_015': 12, 'EuroPar_17_016': 23, 'EuroPar_17_020': 14,
        'EuroPar_17_024': 24, 'EuroPar_17_028': 15, 'EuroPar_17_029': 21,
        'EuroPar_17_030': 17, 'EuroPar_17_031': 16, 'EuroPar_17_032': 11, 'EuroPar_17_033': 15,
        'EuroPar_17_034': 9,  'EuroPar_17_038': 12, 'EuroPar_17_039': 10,
        'EuroPar_17_041': 21, 'EuroPar_17_042': 22, 'EuroPar_17_043': 20,
        'EuroPar_17_044': 20, 'EuroPar_17_045': 20, 'EuroPar_17_046': 17,
        'EuroPar_17_047': 16, 'EuroPar_17_049': 15, 'EuroPar_17_050': 17,
        'Cluster_17_062': 23,
        'PACT_17_002': 33, 'PACT_17_013': 49, 'PACT_17_023': 42,
        'MASCOTS_17_020': 62,
        'IISWC_17_006': 35,
        'MobiCom_17_005': 42, 'MobiCom_17_024': 93,
        'IGSC_17_012': 24, 'IGSC_17_021': 35, 'IGSC_17_022': 27,
        'CCS_17_093': 78,
        'HiPC_17_029': 32,
        'HPCC_17_014': 18, 'HPCC_17_032': 17, 'HPCC_17_061': 9, 'HPCC_17_076': 24,
        'ICDM_17_025': 27,
        'OOPSLA_17_016': 43
        }


#########################################################################
# Select a category for the type of a location (URL) based on regex
def location_type(url):
    if url == "":
        return ""

    if url.find(".edu") > 0 or url.find(".ac.") > 0 or \
            url.find("camelab") > 0 or url.find("uni-") > 0 or \
            url.find(".ch") > 0 or url.find("kau.se") > 0 or \
            url.find("uwaterloo.ca") > 0 or url.find("tu-") > 0 or \
            url.find("tuel.nl") > 0 or url.find("muni.cz") > 0 or \
            url.find("kuleuven") > 0 or url.find("ens.fr") > 0 or \
            url.find("tum.de") > 0 or url.find("dcc.") > 0 or \
            url.find("uam.es") > 0 or url.find("iisc-seal") > 0:
                return "Academic"

    if url.find("github.") > 0 or url.find("bitbucket.") > 0 or \
            url.find("gitlab.") > 0 or url.find("sourceforge") > 0 or \
            url.find("zenodo") > 0 or url.find("doi.org") > 0:
                return "Repository"

    if url.find(".acm.org") > 0:
        return "ACM"

    if url.find(".dropbox.com") > 0 or url.find("drive.google") > 0 or \
            url.find("onedrive") > 0:
                return "Filesharing"

    return "Other"

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
# Add features that arise from parsing the paper's title
def add_artifact_features(key, artifact):
    tidy_artifacts.start_record()
    tidy_artifacts.add("key", "string", key, "Paper ID")
    tidy_artifacts.add("linked", "bool", artifact["linked"], "Artifact was linked to directly in paper")
    tidy_artifacts.add("unreleased", "bool", artifact["url"] == "", "Artifact was never linked or released")
    tidy_artifacts.add("expired", "bool", artifact["last_accessed"] == "", "Artifact is no longer available at linked location")
    tidy_artifacts.add("badge", "bool", artifact["badge"], "Paper received 'Artifact Available' badge")
    tidy_artifacts.add("evaluated", "bool", artifact["evaluated"], "Paper received 'Artifact Available' badge")
    tidy_artifacts.add("location", "string", location_type(artifact["url"]), "Location category for artifact link")


#########################################################################
# Add statistics from the Semantic Scholar record for the paper
def add_s2_features(key, s2):
    if 'outCitations' in s2 and len(s2['outCitations']) > 0:
        oc = len(s2['outCitations'])
    else:
        oc = refs_map[key]

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

    for date, cites in record['citedby'].items():
        tidy_cites.start_record()
        tidy_cites.add("key", "string", key, "Paper ID")
        tidy_cites.add("months", "int", month_diff(date, post), "Months since publiucation")
        tidy_cites.add("citations", "int", cites, "Total citations for this paper on this date")


#########################################################################
# output data from the conference's paper records
def add_paper_record(key, record):
    tidy_papers.add("words", "int", record['words'],
            "Approximate number of words")

    authors = [ normalized_author_name(author_name(p)[0]) for p in record['authors'] ]
    tidy_papers.add("alphabetized", "bool", authors == sorted(authors) and len(authors) > 1,
            "Whether author list sorted in alphabetical order for multi-author papers")
    tidy_papers.add("award", "bool", "award" in record and record["award"],
            "Award-winning (best paper, best student paper, etc.)")

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

    if 'artifact' in record:
        add_artifact_features(record['key'], record['artifact'])

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
            add_s2_features(key, s2data[p['s2pid']])


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
tidy_artifacts.save()
