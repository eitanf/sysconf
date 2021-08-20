#!/usr/bin/env python3

import json
import sys
from collections import OrderedDict

def find_key(data, k):
    if k in data:
        return data[k]
    return []

if len(sys.argv) != 2:
    print("Required parameter: JSON filename to reformat")
    exit(1)

with open(sys.argv[1], mode='r', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

i = 0
# Reorder conference data:
conf = OrderedDict([ (k,find_key(data, k)) for k in [ \
        'key', 'conference', 'url', 'organization', 'country', \
        'postdate', 'last_deadline', 'review_days', 'mean_pages', \
        'submissions', 'min_reviews', 'total_reviews', 'double_blind', \
        'rebuttal', 'open_access', 'age', 'past_papers', \
        'past_citations', 'h5_index', 'h5_median', 'field', 'subfield', \
        'diversit_effort', 'notes', 'pc_chairs', 'pc_members', \
        'keynote_speakers', 'session_chairs', 'panelists', 'papers' \
        ] ])

# Next, reorder paper data:
new_papers = []
for p in conf['papers']:
    i = i + 1
    if 'topics' not in p:
        p['topics'] = []
    p['key'] = conf['key'] + '_' + str(i).zfill(3)
    newp = OrderedDict([ (k,p[k]) for k in [ \
            'key', 'title', 'authors', 'topics' \
            ] ])
    if 'award' in p:
        newp['award'] = p['award']
    if 'artifact' in p:
        newp['artifact'] = p['artifact']
    new_papers.append(newp)

conf['papers'] = new_papers
with open(sys.argv[1], mode='w', encoding='utf-8') as f:
    json.dump(conf, f, indent=4)
