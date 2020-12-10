This file is a simple mapping from author ID to the count of how many papers
this author appeared in, in the Semantic Scholar DB dump dated 2018-05-03.

### Field description {-}

  * `name` (string): Un-normalized author name (first, last).
  * `gs_email` (string): Author email suffix on Google Scholar.
  * `s2aid` (integer): Author ID on Semantic Scholar, based on our dataset.
  * `s2npubs` (integer): No. of times this author ID showed up in the DB dump.

### Provenance and methodology

The file was generated with the following sequence of python scripts:

#### Generate counts of all author IDs

```python
#!/usr/bin/env python3
#
# Read in a JSON data file with a mapping from Semantic Scholar (S2) author IDs
# to counts.
# Read in one or more S2 JSON DB files from the command line arguments,
# then increment the counts of all the author IDs that appear in the file(s)
# and save back the data file.

import sys
from shared_utils import *

counts_fn = "/data/sda/semanticscholar/s2authors-all.json";

counts = load_json_file(counts_fn, False)

for fn in sys.argv[1:]:
    print("Working on: ", fn)
    s2 = load_json_file(fn)
    for paper in s2:
        for author in paper["authors"]:
            if 'ids' in author and len(author['ids']) > 0:
                sid = author['ids'][0]
                if sid not in counts:
                    counts[sid] = 0
                counts[sid] += 1

    save_json_file(counts_fn, counts)
```

#### Find S2 author ID of our authors

The actual S2 author ID of each author can be discovered using this script:

```python
#!/usr/bin/env python3
#
# This script reads in a conference JSON file and author profile file. It adds
# or updates author profile files with their S2 author ID.
# total citation count.

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
        print("Working on author", author)

        if author not in authordata or authordata[author] == "" or 'email' not in authordata[author]:
            gs_email = ""
        else:
            gs_email = authordata[author]['email']

        s2_entry = author_entry(s2authors, author, gs_email)
        if paper['s2pid'] not in s2papers:
            print("Can't find paper", paper["title"], "in s2pids")
            aid = input("Enter S2 ID:")
        else:
            aid = find_aid(author, s2papers[paper['s2pid']], s2_entry['s2aid'])

        if s2_entry['s2aid'] == "":
            s2_entry['s2aid'] = aid

        save_data(s2authors)
```

#### Add publication counts to author ID data

The actual publication counts can then be added with the following code:

```python
from shared_utils import *

s2authors = load_csv_file("data/s2authors.csv")
counts = load_json_file("/tmp/s2authors-all.json")

for r in s2authors:
    if r['s2aid'] in counts:
        r['s2npubs'] = counts[r['s2aid']]

with open("data/s2authors.csv", "w", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = ["name", "gs_email", "s2aid", "s2npubs"])
        writer.writeheader()
        writer.writerows(s2authors)
```

#### Complement counts by names

Finally, there are still some missing counts, because of mistmatched names/IDs. To resolve these, the following script searches by exact name match only. It's very slow.

```python
#!/usr/bin/env python3
#
# Read in a JSON data file with a mapping from Semantic Scholar (S2) author IDs
# to counts.
# For any missing author count, look up the name in all S2 JSON files using
# grep, and count them.

import glob
import subprocess
from shared_utils import *

authors = load_csv_file("data/s2authors.csv")

for r in authors:
    if r['s2npubs'] == "":
        print("Working on", r['name'])
        r['s2npubs'] = subprocess.check_output(["/bin/fgrep", r['name']] +
               glob.glob("/data/sda/semanticscholar/*.json")). \
                       decode('utf-8'). \
                       count('\n')
        print("Found", r['s2npubs'], "entries")

        with open("data/s2authors.csv", "w", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = ["name", "gs_email", "s2aid", "s2npubs"])
            writer.writeheader()
            writer.writerows(authors)
```
