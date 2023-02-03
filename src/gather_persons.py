#!/usr/bin/env python3
#
# This script reads in a conference file, author profile file, and an
# all-authors files. It looks up the authors from the profiles in the all-
# author file to try to find duplicates, and adds any missing records. It also
# aggregates some author statistics across new and existing author records.
# Note that each author is only counted once, even if they coauthor several papers.
# The additional roles.csv output file maps from people to their different (plural)
# roles in the conferences. It also outputs a mapping of people to interests (interests.csv).
# Another feature it outputs to the persons file is the Semantic Scholar author
# ID of each person, if found. For this, it reads in a JSON file with the S2
# paper records and compares it to its own records to identify each person.

import editdistance
import sys
import tidydata
from shared_utils import *

### initialize_static_data before dealing with specific conference:

author_fn = "persons"
role_fn = "roles"
interest_fn = "interests"
email_fn = "survey/authors-for-survey.csv"

s2data = load_json_file("data/s2papers.json")
s2authors = load_csv_file("data/s2authors.csv")
s2counts = { a['name'] + a['gs_email'].lower() : a['s2npubs'] for a in s2authors }

idata = load_csv_file("data/interest_mapping.csv")
interest_mapping = { i['interest'] : { 'canonical': i['canonical'], 'topic': i['topic'] } for i in idata }

verified = load_csv_file("data/verified_gender_mapping.csv")
inferred = load_csv_file("data/inferred_gender_mapping.csv")
genderdata = { row['name'] : row['gender'] for row in inferred }
genderdata.update({ row['name'] : row['gender'] for row in verified })

email_regex = load_csv_file("data/domain_mapping.csv")
unis = [ u["domain"] for u in load_csv_file("data/top_universities.csv") ]
coms = [ c["domain"] for c in load_csv_file("data/top_companies.csv") ]

paper_emails = {}
if os.path.isfile(email_fn):
    paper_emails = { r["name"] : r["email"] for r in load_csv_file(email_fn) }
elif not os.path.isfile(feature_fn(author_fn)):
    print("*************************************************************")
    print("Warning: can't find file with author emails, using only GS affiliations")
    print("New persons.csv data may differ on country and sector fields")
    print("*************************************************************")

# List of authors that have been verified to be two different people at two
# different affiliations:
repeated_names = [ \
        "Kumar, Rakesh", "Xu, Jian", "Dai, Wei", "Zhang, Nan", "Chen, Kai", \
        "Wang, Xiao", "Azimi, Reza", "Wang, Di", "Yang, Jun", "Wang, Hao", \
        "Li, Zhenhua", "Huang, Wei", "Wang, Kai", "Song, Shuang", "Zhang, Ying", \
        "Li, Jian", "Yang, Lei", "Huang, Jian", "Hu, Yang", "Cao, Qiang", \
        "Zhang, Haoyu", "Lo, David", "Li, Jinyang", "Yu, Lei", "Chen, Shuang", \
        "Roy, Abhishek", "Zhang, Lu", "Wang, Xi", "Wang, Zhe", "Zhang, Jie", \
        "Wang, Chao", "Li, Yan", "Chen, Cheng", "Ding, Wei", "Chen, Feng", \
        "Chen, Ping", "Li, Hui", "Zheng, Wei", "Wang, Jia", "Liu, Rui", \
        "Chen, Wei", "Li, Cheng", "Li, Kai", "Ma, Hao", "Pan, Rong", \
        "Tang, Jian", "tao, Yufei", "Zhang, Rui", "Zhang, Chao", "Wang, Jie", \
        "Wang, Fei", "Xu, Jun", "Liu, Chang", "Wang, Yue", "Wu, Wei", \
        "Li, Yong", "Qin, Zheng", "Zhang, Fan", "Zhang, Yan", "Zhang, Heng", \
        "Wang, Xin", "Wang, Qing", "Zhang, Heng", "Xu, Cong", "Zhang, Hao", \
        "Zhang, Zheng", "Li, Xi", "Li, Bo", "Chen, Yi", "Zhang, Xiao", \
        "Zhang, Li", "Zhang, Hui", "He, Yuan", "Wang, Wei", "Li, Xin", \
        "Wang, Peng", "Zhang, Kun", "Wang, Jun", "Ren, Xiang", \
        "Wang, Xiang", "Liu, Fang", "Zhang, Peng", "Yang, Yang", "Zhang, Yu", \
        "Cheng, Peng", "Wang, Yang", "Li, Lei", "Zhang, Hong", "Li, Yang", \
        "Wang, Hui", "Wu, Fei", "Chen, Bo", "Zhang, Qian", "Wang, Chen", \
        "Li, Song", "Oliveira, Tiago", "Yang, Fan" \
        ]

# List of very common last names that are filtered out (raises risk of
# false negatives but reduces false positives significantly)
ignore_list = [ \
        "Wang", "Zhang", "Liu", "Li", "Lu", "Chen", "Yang", "Wu", "Xu",  \
        "Yan", "Feng", "Guo", "Ma", "Cao", "Hu", "Yu", "Zhao", "Tian", \
        "Sun", "Shen", "Nguyen", "Kim", "Jiang", "Huang", "Han", \
        "Ding", "Dong", "Deng", "Lee", "Zheng", "Park", "Gong", "Zou", \
        "Song", "Xia", "He", "Jung", "Lin", "Tang", "Ji", "Zhou", "Jia",
        "Cheng", "Ren", "Cho", "Yin", "Xiao", "Gan", "Gupta", "Meng", \
        "Cui", "Choi", "Gu", "Singh", "Zeng", "Ye", "Shi", "Liang", "Xie", \
        "Jin", "Wei", "Luo", "Du", "Zhu", "Yoo", "Xue" \
        ]

# List of names that have been manually verified against their "dopplegangers"
# to be unique and therefore should be skipped
verified_list = [ \
        "Jiang, Song", "Hu, Jiang", "Hu, Ben", "Choi, Wonik", \
        "Xu, Qiang", "Song, Yunpeng", "Wei, Lei", "Ma, Xiaolong", \
        "Cui, Weilong", "Xiong, Jie", "Lin, Feng", "Nguyen, Tam", \
        "Ji, Yan", "Han, Yi", "Liang, Bin", "Ramasubramanian, Rama",
        "Rahman, Md. Shaifur", "Kumar, Mohit", "Kumar, Akash", \
        "Gupta, Vishal", "Gupta, Vishakha", "Ibrahim, Khaled", \
        "Kumar, Jitendra", "Misra, Sachet", "Meng, Xin", "Jia, Yichen", \
        "Jian, Li", "Baker, Gavin", "Wei, Hao", "Das, Sanjoy", "Ni, Ray", \
        "Ren, Shaolei", "Peng, Bo", "Xue, Xun", "Gan, Ze", "Tang, Xueyan", \
        "Jung, Minyoung", "Ni, Peng", "Du, Min", "Fu, Bo", "Gu, Yu", \
        "Jing, Jiwu", "Jin, Meng", "Yin, Xia", "You, Jie", "Yuan, Lihua", \
        "Zhou, Dong", "Smith, Lauren L.", "Cheng, Xueqi", "Cui, Peng", \
        "Fu, Hao", "Zhou, Yucan", "Liang, Jiye", "Su, Lu", "Yoo, Jaemin", \
        "Du, Lan", "Zhou, Ziting", "Ye, Li", "Xie, Hong", "Cui, Limeng", \
        "Fang, Chen", "Gu, Qilong", "Qian, Buyue", "Choi, Jinho", \
        "Singh, Ambuj", "Jin, Wen", "Yin, Hao", "Ye, Wei", "Jain, Anil", \
        "Gu, Bin", "Zhou, Chong", "Fang, Yuan", "Luo, Cheng", "Zeng, Wei", \
        "Yao, Jianguo", "Leong, Ben", "Gupta, Rishab", "Gupta, Ajay", \
        "Cho, Young Im", "Baker, Sonia", "Liang, Hao", "Du, Lian", \
        "Xiao, Limin", "Gu, Fei", "Tan, Zhipeng", "Qin, Jian", "Zhou, Ke", \
        "Ahmad, Maaz Bin Safeer", "Bergman, Aran", "Shah, Miral", \
        "Jain, Akash", "Ni, Karl", "Liang, Yun", "Luo, Liang", "Du, Jiang",
        "Baker, Tobin", "Jain, Akanksha", "Ibrahim, Mohamed", "Bergman, Shai", \
        "Ramasubramanian, Kamala", "Misra, Sanchit", "Shah, Mehul", \
        "Das, Sanjib", "Hill, Mason", "Rahman, Joy", "Rahman, Md Shafayat" \
        ]


##############################################################################
# Open a CSV file (if it exists) and returns a list of its elements
def read_if_exists(fn):
    try:
        return load_csv_file(feature_fn(fn))
    except OSError:
        return []

##############################################################################
# matches_previous to check whether two records with the sane name but with
# different gs_email still refer to the same person. This can happen because
# three of the roles (keynote, session, and panel) don't get a record in the
# authors .json file, so may not have a GS email. We have to check both cases:
# either they're currently or previously in one of these three roles.
def matches_previous(gs_email, role, previous):
    # Is the current role one of those three?
    if gs_email == "" and \
            (role == "keynote" or role == "session" or role == "panel"):
        return True

    # Otherwise, if the previous email on record is empty, we must ensure
    # that all previous roles are one of these three:
    if previous['gs_email'] != '':
        return False
    for prole in all_roles:
        if prole['name'] == previous['name'] and prole['gs_email'] == '' and \
            (prole['role'] != "keynote" and prole['role'] != "session" and prole['role'] != "panel"):
                return False

    return True


##############################################################################
# find_author looks up an author name in the aggregated records and returns:
# - None if nothing of the same last name was found
# - A row record otherwise, corresponding to the author with the least edit
# distance to the given author, and if available, same email affiliation.
def find_author(name, gs_email):
    min_dist = 1000
    last = name.split(',')[0]
    best_match = None
    global ignore_list
    global verified_list
    global all_authors

    for a in all_authors:
        if a['name'].split(',')[0] == last:
            dist = editdistance.eval(a['name'], name)
            if dist < min_dist or (dist == min_dist and gs_email == a['gs_email']):
                min_dist = dist
                best_match = a

    return best_match


##############################################################################
# merge_gs_stats takes an author record from the current author file and an
# author row (dictionary) from previous records (files) and reconciles them
# so that the google scholar statistics in the row are updated if necessary
# with the new data in record. By default, the update is "find minimum value"
def merge_gs_stats(row, record):
    def combine_min(key):
        if key not in row or row[key] == '':
            row[key] = record[key]
        else:
            row[key] = min(int(row[key]), record[key])

    if record == "":
        row.update({'npubs': "", 'hindex' : "", 'hindex5y': "", 'i10index': "", 'i10index5y': "", 'citedby': "" })
        return

    combine_min('npubs')
    combine_min('hindex')
    combine_min('hindex5y')
    combine_min('i10index')
    combine_min('i10index5y')

    if 'citedby' in row and row['citedby'] != '':
       curmin = int(row['citedby'])
    else:
        curmin = 9999999
    row['citedby'] = min(curmin, max(record['citedby'].values()))


##############################################################################
# similar_names: Determine whether two names are similar enough to suspect
# that they're the same.
# We separately check how far apart are the last names and the first names.
def similar_names(name1, name2):
    # How far apart (edit distance) are two last-name considered possibly the same?
    # These values have been determined empirically to try to lower false
    # negatives first, then false positives.
    last_name_dist = 20
    first_name_dist = 3

    if name1 in verified_list:
        return False

    ns1 = remove_accents(name1).split(' ')
    ns2 = remove_accents(name2).split(' ')
    if ns1[0] == ns2[0] and ns1[0].split(',')[0] in ignore_list:
        return False

    return editdistance.eval(ns1[0], ns2[0]) <= last_name_dist \
       and editdistance.eval(ns1[1], ns2[1]) <= first_name_dist

##############################################################################
# For a given role (a string), append person's name, email, and a given key
# to the roles list.
def append_role(record, role, key):
    role = { 'name' : record['name'],
             'gs_email' : record['gs_email'],
             'role' : role,
             'key' : key
           }
    global all_roles
    all_roles.append(role)


##############################################################################
# For a given GS person record, append their interests to the interest data
# find if person already in interests. If not, add one row per interest

def append_interests(name, email, gs):
    global all_interests
    global interest_cache
    global interest_mapping

    if gs == "" or 'interests' not in gs:
        return

    if name+email in interest_cache:
        return

    interest_cache[name+email] = True

    for interest in gs['interests']:
        interest = interest.lower()
        if interest not in interest_mapping:
            print("#### Missing interest", interest, "in interest_mapping.csv! please add it") # Crash and burn
        canonical = interest_mapping[interest]['canonical']
        all_interests.append({'name': name,
            'gs_email': email,
            'interest': canonical if canonical != "" else interest,
            'topic': interest_mapping[interest]['topic'] })


##############################################################################
# merge_person takes an author record from the current author data, and tries
# reconcile it with the aggregated author data in all_authors. It needs to handle:
# - Never-before-merged record
# - Existing record (merge data)
# - Similar record: same last name and affiliation, different full name
# - Similar record: same full name, different gs email
# - Author role, which includes paper key
# Returns the current row in all_authors for this author

def merge_person(person, role, conf):
    global repeated_names
    global all_authors

    name = author_name(person)[0]
    normalized = normalized_author_name(name)
    record = record_of(authordata, name)

    if record == "" or 'email' not in record or record['email'] == '':
        gs_email = ""
    else:
        gs_email = record['email'].lower()

    found = False  # Have we found this exact author before?
    previous = find_author(normalized, gs_email)

    if previous == None:
        pass
    elif normalized == previous["name"]:
        if gs_email == previous['gs_email'] or matches_previous(gs_email, role, previous):
            found = True

        elif normalized not in repeated_names:
            print("Found two authors with same name (" + name + ") but different emails: ", gs_email, "and", previous['gs_email'], "currently", role)
    else:
        pname = previous["name"]
        if similar_names(normalized, pname) and gs_email == previous['gs_email']:
            print("Suspected two duplicate authors with same email (" + gs_email + ") but different names: ", normalized, "and", pname)

    if found:
        row = previous
        if previous['gs_email'] ==  "":
            row['gs_email'] = gs_email
    else:
        row = { 'name': normalized, 'gs_email': gs_email }
        all_authors.append(row)

    merge_gs_stats(row, record)
    key = name + gs_email.lower()
    if key in s2counts:
        row['s2npubs'] = s2counts[key]
    elif 's2npubs' not in row:
        row['s2npubs'] = ""

    append_role(row, role, conf)
    append_interests(normalized, gs_email, record)

    return row

##############################################################################
# Find regex patterns in an email address (based on a prioritized list) to
# figure out the country and sector corresponding to the email address.
domain_cache = {
        "": ( "", "", False, False ),
        "@acm.org": ( "", "", False, False ),
        "@gnu.org": ( "", "", False, False ),
        "@apache.org": ( "", "", False, False ),
        "@ieee.org": ( "", "", False, False ),
        "@theiet.org": ( "", "", False, False ),
        "@computer.org": ( "", "", False, False )
        }

##############################################################################
# For a given email address, try to extract the country code and type of
# sector that corresponds to the address, based on patterns in email_regex
# Also returns a boolean for whether the affiliation is one of the top
# universities, and another for top companies.
def parse_email(email):
    global email_regex

    if email in domain_cache:
        return domain_cache[email]

    topuni = False
    for u in unis:
        if email.find(u) >= 0:
            topuni = True
    topcom = False
    for c in coms:
        if email.find(c) >= 0:
            topcom = True

    for pat in email_regex:
        m = re.search(pat['regex'], email.lower())
        if m is None:
            continue

        country = pat['country']
        sector = pat['sector']
        for i in range(1, 1 + len(m.groups())):
            placeholder = "\$" + str(i)
            country = re.sub(placeholder, m.group(i), country)
            sector = re.sub(placeholder, m.group(i), sector)

    if country == "NA":
#        print("Couldn't identify country for", email)
        country = ""
    if sector == "NA":
#        print("Couldn't identify sector for", email)
        sector = ""

    domain_cache[email] = country.upper(), sector.upper(), topuni, topcom
    return country.upper(), sector.upper(), topuni, topcom


##############################################################################
# Create a tidy data file with all authors:
def  save_all_authors(genderdata):
    global paper_emails
    global all_authors

    tidy = tidydata.TidyData(author_fn,
        "aggregated information about all authors, TPC chairs, and other roles in the selected conference subset.")
    for row in sorted(all_authors, key=lambda x: x["name"]):
        tidy.start_record()
        tidy.add("name", "string", row['name'],
                "Full person name, normalized and quoted")
        tidy.add("gs_email", "string", row['gs_email'],
                "The email affiliation of the author as reported by GS (latest)")

        gender = genderdata[row['name']] if row['name'] in genderdata else ""
        tidy.add("gender", "categorical string", gender, "Verified or inferred gender")

        # Try to extract country and sector of author from email address.
        # First, try email address from paper, if available, because that's
        # more representative at the time of writing. Otherwise, try GS.
        # We also try GS first if the name is repeated, because GS addresses
        # are disambiguated, whereas author names in the email list aren't.
        country, sector = "", ""
        if row['name'] not in repeated_names and row['name'] in paper_emails:
            country, sector, uni, com = parse_email(paper_emails[row['name']])
        if country == "" and sector == "":
            country, sector, uni, com = parse_email(row['gs_email'])
        tidy.add("country", "categorical string", country, "Two-letter country code from email affiliation (either paper or GS)")
        tidy.add("sector", "categorical string", sector, "Employer sector from email affiliation (either paper or GS)")
        tidy.add("top_university", "bool", uni, "Author is affiliated with a top university")
        tidy.add("top_company", "bool", com, "Author is affiliated with a top company")


        tidy.add("npubs", "int", row['npubs'], "Author's total publications (minimum across all conferences)")
        tidy.add("hindex", "int", row['hindex'], "Author's H-index (minimum)")
        tidy.add("hindex5y", "int", row['hindex5y'], "Author's H-index for past 5 years (minimum)")
        tidy.add("i10index", "int", row['i10index'], "Author's i10 index (minimum)")
        tidy.add("i10index5y", "int", row['i10index5y'], "Author's i10 index for past 5 years (minimum)")
        tidy.add("citedby", "int", row['citedby'], "Author's total citations (minimum)")
        tidy.add("s2npubs", "int", row['s2npubs'], "Author's total publications in Semantic Scholar DB image")


    tidy.save()


##############################################################################
 # Create a tidy data file with all roles of all persons
def save_all_roles():
    global all_roles

    tidy = tidydata.TidyData(role_fn,
        "Detailed list of all the roles each person assumes in a conference. Multiple roles result in multiple rows. Authors are grouped by paper and ordered by authorship order.")

    for row in all_roles:
        tidy.start_record()
        tidy.add("name", "string", row['name'],
                "Full person name, normalized and quoted")
        tidy.add("gs_email", "string", row['gs_email'],
                "The email affiliation of the author as reported by GS (latest)")
        tidy.add("role", "categorical string", row['role'],
                "The role this person served in the conference")
        tidy.add("key", "string", row['key'],
                "The conference or paper key for this person/role")

    tidy.save()

##############################################################################
 # Create a tidy data file with all interests of all authors and PC members
def save_all_interests():
    global all_interests

    tidy = tidydata.TidyData(interest_fn,
        "Detailed list of all the interests each person listed in their Google Scholar profile. Multiple interests result in multiple rows.")

    for row in sorted(all_interests, key=lambda x: x["name"]):
        tidy.start_record()
        tidy.add("name", "string", row['name'],
                "Full person name, normalized and quoted")
        tidy.add("gs_email", "string", row['gs_email'],
                "The email affiliation of the author as reported by GS (latest)")
        tidy.add("interest", "string", row['interest'].lower(),
                "The listed interest (possibly spell-corrected or translated to English")
        tidy.add("topic", "categorical string", row['topic'],
                "The topic tag this interest best belongs to")

    tidy.save()


##############################################################################
# Some roles (keynote, session chair, panelist) don't necessarily have a GS
# profile extracted for them, so we have to make sure that if they haven't
# seen a GS email when they were first created, but one was found later, then
# it's copied back to this role.
def dedup_roles():

    roles = load_csv_file(feature_fn("roles"))
    for i in range(len(roles)):
        r = roles[i]
        if r['gs_email'] == "" and \
            (r['role'] == "keynote" or r['role'] == "session" or r['role'] == "panel"):
                for r2 in roles:
                    if r2['name'] == r['name'] and r2['gs_email'] != "":
                        roles[i]['gs_email'] = r2['gs_email']

    with open(feature_fn("roles"), "w", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = ["name", "gs_email", "role", "key"])
        writer.writeheader()
        writer.writerows(roles)


##############################################################################
##############################################################################
######### main

if len(sys.argv) != 2:
    print("Required argument: conference name")
    exit(1)

conf = sys.argv[1]
conf_id = conf + "_17"

### Read in conf and author data:
print(conf)
confdata = load_json_file(data_fn('conf', conf))
authordata = load_json_file(data_fn('authors', conf))


# Previously-computed outputs:
all_authors = read_if_exists(author_fn) # All author records
all_roles = read_if_exists(role_fn)  # A list of all persons and the roles they take
all_interests = read_if_exists(interest_fn) # A list of all persons and their GS interests
interest_cache = { i['name'] + i['gs_email'] : True for i in all_interests }

### Utility functions
def record_of(authordata, name):
    return authordata[name] if name in authordata else ""

########### Main loop: Iterate over all persons and create/merge their record
for person in confdata['pc_chairs']:
    merge_person(person, "chair", conf_id)

for person in confdata['pc_members']:
    merge_person(person, "pc", conf_id)

if 'panelists' in confdata:
    for person in confdata['panelists']:
        merge_person(person, "panel", conf_id)

if 'keynote_speakers' in confdata:
    for person in confdata['keynote_speakers']:
        merge_person(person, "keynote", conf_id)

if 'session_chairs' in confdata:
    for person in confdata['session_chairs']:
        merge_person(person, "session", conf_id)

for paper in confdata['papers']:
    for person in paper['authors']:
        row = merge_person(person, "author", paper['key'])


### Done, save outputs
save_all_authors(genderdata)
save_all_roles()
save_all_interests()
dedup_roles()
