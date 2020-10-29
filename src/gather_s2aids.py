#!/usr/bin/env python3
#
# This script reads in a conference JSON file and author profile file. It adds
# or updates author profile files with their S2 author ID.

import sys
from shared_utils import *
import editdistance


##############################################################################
# Find or create an author entry in s2 author data for a given name and email
def author_entry(s2authors, name, gs_email):
    for r in s2authors:
        if r['name'] == name and r['gs_email'] == gs_email:
            return r

    s2authors.append(dict({
        'name': name,
        'gs_email': gs_email,
        's2aid': '',
        's2npubs': ''}))
    return s2authors[-1]

##############################################################################
# Find the best matching author ID for a given name out of the S2 paper record
def find_aid(name, paper, prev):
    min_dist = 10000
    best_id = ""
    best_name = ""
    DIST_THRESHOLD = 3

    for a in paper['authors']:
        dst = editdistance.eval(a['name'], name)
        if dst < min_dist and len(a['ids']) > 0:
            min_dist = dst
            best_id = a['ids'][0]
            best_name = a['name']

    print("Found best", best_name, "with distance", min_dist, "id:", best_id, "Previously:", prev)
    if min_dist == 10000:
        if prev != "":
            best_id = prev
        else:
            acc = input("Couldn't find any authors, enter ID:")
            best_id = acc

    elif min_dist > DIST_THRESHOLD and best_id != prev and prev == "":
        acc = input("\n*** Accept (y/new-id/newline)?")
        if acc != "y" and acc != "Y":
            best_id = acc
        else:
            best_id == ""

    if prev != "" and prev != best_id:
        print("@@@ Found mismatched author ID:", best_id, "previously: ", prev)
        acc = input("@@@ Please acknowledge (old value will not be overwritten)")

    return best_id

def save_data(data):
    with open("data/s2authors.csv", "w", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = ["name", "gs_email", "s2aid", "s2npubs"])
        writer.writeheader()
        writer.writerows(data)

##############################################################################
######### main

if len(sys.argv) != 2:
    print("Required argument: conference name")
    exit(1)

conf = sys.argv[1]
confdata = load_json_file(data_fn('conf', conf))
authordata = load_json_file(data_fn('authors', conf), False)
s2papers = load_json_file("data/s2papers.json")
s2authors = load_csv_file("data/s2authors.csv", False)


for paper in confdata['papers']:
    print(">>> Working on paper:\t", paper["title"])
    for a in paper['authors']:
        author, _ = author_name(a)

        if author not in authordata or authordata[author] == "" or 'email' not in authordata[author]:
            gs_email = ""
        else:
            gs_email = authordata[author]['email']

        s2_entry = author_entry(s2authors, author, gs_email)
#        if s2_entry['s2aid'] != "":
#            continue

        print("Working on author", author)
        if paper['s2pid'] not in s2papers:
            print("Can't find paper", paper["title"], "in s2pids")
            aid = input("Enter S2 ID:")
        else:
            aid = find_aid(author, s2papers[paper['s2pid']], s2_entry['s2aid'])

        if s2_entry['s2aid'] == "":
            s2_entry['s2aid'] = aid

        save_data(s2authors)
