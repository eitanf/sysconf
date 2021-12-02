#!/usr/bin/env python3
#
# This script reads in roles data (roles.csv), groups all authors by paper,
# and then outputs a new file (coauthors.csv) where each row represents
# one pair of authors (each pair shows once per paper).
# The odering of authors in a row is arbitrarily alphabetical.
# Every author is automatically their own "coauthor" as well, so every paper
# would have at least one row for it (for a single-author paper). In the
# general case, a paper would have (n+1)n/2 rows (where n=# of unique authors).

import tidydata
from shared_utils import *

roles = load_csv_file(feature_fn("roles"))
coauthors = []

##############################################################################
# For a given pair of authors and a paper key, append pair to coauthors list.
def append_pair(name1, email1, name2, email2, paper_key):
    global coauthors

    pair = { 'name1' : name1, 'gs_email1' : email1,
             'name2' : name2, 'gs_email2' : email2,
             'paper_key' : key }
    coauthors.append(pair)

##############################################################################
 # Create a tidy data file with all coauthor pairs
def save_all_coauthors():
    global coauthors

    tidy = tidydata.TidyData("coauthors",
        "Lists of co-author pairs. For a given paper with n distinct authors, all n*(n-1)/2 pairs will show up in distinct rows. The ordering of the pair is alphabetical, and each pair only appears once per paper. All authors are also paired with themselves.")

    for pair in sorted(coauthors, key=lambda x: x['paper_key']):
        tidy.start_record()
        tidy.add("paper", "string", pair['paper_key'],
                "The key of the coauthored paper")
        tidy.add("name1", "string", pair['name1'],
                "Full person name for author 1, normalized and quoted")
        tidy.add("gs_email1", "string", pair['gs_email1'],
                "The email affiliation of author 1 as reported by GS")
        tidy.add("name2", "string", pair['name2'],
                "Full person name for author 2, normalized and quoted")
        tidy.add("gs_email2", "string", pair['gs_email2'],
                "The email affiliation of author 2 as reported by GS")

    tidy.save()

##############################################################################
######### main

# First, collect all author names and emails indexed by paper id
authors = {}

for r in roles:
    if r['role'] == "author":
        if r['key'] not in authors:
            authors[r['key']] = []
        authors[r['key']].append(( r['name'], r['gs_email'] ))

# Then, find all distinct pairs of authors for every paper:
for key, alist in authors.items():
    for i in range(0, len(alist)):
        for j in range(0, len(alist)):
            if i != j:
                append_pair(alist[i][0], alist[i][1], alist[j][0], alist[j][1], key)


### Done, save outputs
save_all_coauthors()
