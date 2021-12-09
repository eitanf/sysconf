#!/usr/bin/env python3
#
# This script collects, aggregates, and computes a set of variables associated
# with conferences. It appends to a CSV file (confs) where each row corresponds
# to a conference, and the columns represent the variables. Each conference
# (row) is uniquely identified with a key string.
# The script takes conference names as input, and uses the corresponding
# data files from data/ for conference and author information.

from datetime import datetime as dt
import tidydata
import sys
from shared_utils import *

today = dt.today().strftime("%Y-%m-%d")

#########################################################################
# For a given conference data, if a certain variable is defined in it,
# then compute an arbitrary expression. Otherwise return default.
def verify(conf, var, expr, default = ""):
    if var in conf and conf[var] != "":
        return eval(expr)
    else:
        return default


#########################################################################
# Extract all variables available from conference file.
# The fields are grouped (in the source-code only) based on the main
# variable in the data/conf/ file that is responsible to generate them.
def add_conf_stats(tidy, conf):
    dow = [ 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN' ]
    rec = {}
    npapers = len(conf['papers'])
    pc_papers = 0


    # key
    tidy.add("conference", "string", conf['key'],
            "Short name of the conference (unique)")

    # organization
    orgs = [ "ACM", "IEEE", "USENIX" ]
    add_dummies(rec, 'org', conf['organization'], orgs)
    for o in orgs:
        tidy.add("is_org_" + o, "bool", rec['is_org_' + o],
                "Conference sponsored/organized by " + o)

    # Field and subfield:
    tidy.add("field", "category", conf['field'],
            "The top-level category of the conference's topic")
    tidy.add("subfield", "category", conf['subfield'],
            "The top-ocurring topic of interest for this conference")

    # URL
    tidy.add("url", "string", conf['url'],
            "The URL of the main web page for this conference")

    # country
    tidy.add("country", "category", conf['country'],
            "Two-letter name of country when conference took place")

    # postdate
    tidy.add("postdate", "date", conf['postdate'], "First day of conference")
    tidy.add("month_of_year", "int", int(conf['postdate'][5:7]),
            "Month of year (1-12) of the conference's postdate")
    tidy.add("months_since_published", "int", month_diff(today, conf['postdate']),
            "Months passed since the postdate to date of feature extraction")

    # Deadline day of the week
    tidy.add("deadline_day_of_week",
            "category",
            dow[dt.strptime(conf['last_deadline'], "%Y-%m-%d").weekday()],
            "The day of week of the last submission deadline (3-letter categorical abberviation)")

    # review_days
    tidy.add("review_days", "int", conf['review_days'],
            "The number of days between full paper submission due date and author notification")

    # mean_pages
    tidy.add("mean_pages", "numeric", conf['mean_pages'],
            "Average number of pages in PDF version of accepted papers.")

    # submissions
    tidy.add("submissions", "int", conf['submissions'],
            "Total number of papers submitted for review")

    # min_reviews
    tidy.add("min_reviews", "int", conf['min_reviews'],
            "The minimum number of reviews received by each paper")

    # total_reviews
    tidy.add("total_reviews", "int", conf['total_reviews'],
            "The total number of formal reviews written by the PC, overall")

    # Boolean properties:
    tidy.add("double_blind", "bool", conf['double_blind'],
            "Whether the review process was double-blind")
    tidy.add("rebuttal", "bool", conf['rebuttal'],
            "Were authors afforded an opportunity to answer the reviews before final acceptance decision was made?")
    tidy.add("open_access", "bool", conf['open_access'],
            "Whether conference is open access")
    tidy.add("diversity_effort", "bool", conf['diversity_effort'],
            "Did the conference explicitly attempt to increase diversity?")

    # age
    tidy.add("age", "int", conf['age'],
            "Approximate age (in years) of this conference series")

    # past_papers
    tidy.add("past_papers", "int", conf['past_papers'],
            "How many papers were published in this series prior to publication year")
    tidy.add("mean_historical_length",
            "number",
            verify(conf, 'past_papers', "conf['past_papers'] / conf['age']"),
            "Average number of papers per conference (in the series) for previous years")

    # past_citations
    tidy.add("past_citations", "int", conf['past_citations'],
            "How many total citations have papers in this series received, at approximately the postdate")
    tidy.add("mean_historical_citations",
            "number",
            verify(conf, 'past_citations', "conf['past_citations'] / conf['past_papers']"),
           "Average number of citations per paper in past conferences in the series")

    # h5_index
    tidy.add("h5_index", "int", conf['h5_index'],
            "The H-index of the conference in the 5 years preceding the postdate")

    # h5_median
    tidy.add("h5_median", "number", conf['h5_median'],
            "The median H-index per paper in the conference in the 5 years preceding the postdate")

    # pc_chairs
    tidy.add("chairs_num", "int", len(conf['pc_chairs']),
            "The number of program committee chairs")

    # pc_members
    # Find names of all PC chairs and members, without affiliation:
    pc_names = set([ name for name in \
            [ author_name(a)[0] for a in conf['pc_members'] + conf['pc_chairs'] ] ])
    # Find names of all authors, without affiliation (unique):
    author_names = set([ name for name in \
            [ author_name(a)[0] for p in conf['papers'] for a in p['authors'] ] ])

    tidy.add("pc_size", "int", len(conf['pc_members']),
            "Number of technical PC members")
    tidy.add("pc_author_ratio", "number", len(pc_names) / len(author_names),
            "Average number of PC members per unique author")

    # papers
    tidy.add("npapers", "int", npapers,
            "How many research papers were published in the proceedings")
    tidy.add("authors_num", "int", len(author_names),
            "Total number of unique authors")
    tidy.add("mean_authors_per_paper", "number", len(author_names) / npapers,
        "Average number of co-authors per paper")
    tidy.add('acceptance_rate',
            "number",
            verify(conf, 'submissions', str(npapers) + " / conf['submissions']"),
            "Ratio between number of accepted papers and number of submitted papers")

    # Compute ratio of papers with a PC author:
    pc_papers = 0
    for p in conf['papers']:
        if any([ author in pc_names for author in \
                [ author_name(a)[0] for a in p['authors'] ] ]):
            pc_papers += 1

    tidy.add("pc_paper_ratio", "number", pc_papers / npapers,
            "Ratio of papers (out of 100%) that have at least one author who is a PC member")


    # Full name
    tidy.add("full_name", "string", conf['conference'],
            "Long name of the conference")


#########################################################################
#########################################################################
# main

if len(sys.argv) < 2:
    print("Arguments: conference [--skip-header]")
    exit(-1)

tidy = tidydata.TidyData("confs",
        "features and aggregated statistics relating to each conference in the set.")

for conf in sys.argv[1:]:
    print("Processing:", conf)
    confdata = load_json_file(data_fn('conf', conf))
    tidy.start_record()
    add_conf_stats(tidy, confdata)

tidy.save()
