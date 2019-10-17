#!/usr/bin/env python3
#
# Parse a JSON file with paper data, and for each paper whose text isn't
# already downloaded in the fulltext directory, and a URL exists in the
# paper records, download the paper.
# The fulltext filenames conform to the convention 'fulltext/KEY.pdf',
# where KEY is the key of the record in the paper file.

import os
import sys
from shared_utils import *

if len(sys.argv) != 2:
    print("Missing argument: conference name")
    exit(1)

conf = sys.argv[1]
papers = load_json_file(data_fn('papers', conf))

print ("Downloading fulltext for",  conf)
for key in sorted(papers.keys()):
    fn = 'fulltext/' + key + '.pdf'
    if os.path.isfile(fn):
        pass
    elif papers[key]['url'] == '':
        print("No url found for paper:", key, papers[key]['title'])
    else:
        print("Downloading file " + fn + "... ")
        os.system('/usr/bin/curl -o ' + fn + " '" + papers[key]['url'] + "'")

