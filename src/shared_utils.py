#!/usr/bin/env python3
#
# This script contains common utilities shared among the other scripts

import csv
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import json
import os
import re
import statistics
import sys
import unicodedata


##############################################################################
# remove_accents(): Remove unicode accents from a string. Copied from:
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


##############################################################################
# author_name(): break an author string to a name and (optionally) affiliation
def author_name(name):
    m = re.match("([^\(]*) \((.*)\)$", name)
    if m is None:
        orig = name
        affil = None
    else:
        orig = m.group(1)
        affil = m.group(2)

    orig = re.sub(r'"', '', orig)
    pattern = re.compile(r'["\(\),]', re.U)
    clean = re.sub(pattern, '_', orig)
    if clean != orig:
        print("~~~~~~~~~~~~\tPossibly malformed name:", name, "\tsanitized:", clean)
    clean = ' '.join(clean.split())

    return clean, affil


##############################################################################
# normalize_author_name(): break an author string to a name and (optional)
# affiliation, and return the name only, last first, title case, no honorifics
def normalized_author_name(name):
    recased = name.title().replace('Jr.', '').replace('Sr.', '').replace('Dr.', '').replace('Prof.', '')
    names = author_name(recased)[0].split()
    if len(names) == 1:
        return names[0]
    else:
        return names[-1] + ", " + " ".join(names[:-1])


##############################################################################
# load_csv_file(): Try to read a CSV file and return its contents.
# The file is assumed to have headers, and contents are returned as list of
# dictionaries (keys based on headers)
# If it's not there, either throw an error or ignore (depending on 'force').
def load_csv_file(fn, force=True):
    data = []
    try:
        with open(fn, mode="r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    except OSError:
        print("Couldn't read file ", fn);
        if force:
            raise

    return data


##############################################################################
# load_json_file(): Try to read a JSON file and return its contents.
# If it's not there, either throw an error or ignore (depending on 'force').
def load_json_file(fn, force=True):
    try:
        with open(fn, mode="r" ) as f:
            return json.load(f)
    except OSError:
        print("Couldn't read file ", fn);
        if force:
            raise
        else:
            return {}


##############################################################################
# save_json_file(): save 'data' into a JSON filename, sorted and formatted.
def save_json_file(fn, data):
     with open(fn, mode='w' ) as f:
            json.dump(data, f, indent=4, sort_keys=True)


##############################################################################
# persistent_json_update(): (re)load data from JSON, add a new value to it
# (indexed by new/old key) and re-save it to file.
def persistent_json_update(fn, key, newval):
    data = load_json_file(fn, False)
    data[key] = newval
    save_json_file(fn, data)


##############################################################################
# data_fn(): return the full relative pathname for a data file of a given
# category (one of "conf" / "authors" / "papers") and a short conf name.
def data_fn(category, conf):
    if category[0] == 'c':
        return "data/conf/" + conf + ".json"
    elif category[0] == 'a':
        return "data/authors/" + conf + ".json"
    elif category[0] == 'p':
        return "data/papers/" + conf + ".json"
    else:
        print("Unrecognized category", category)
        return None


##############################################################################
# feature_fn(): return the full relative pathname for a feature file of a
# given basename. Feature files are always in CSV format.
def feature_fn(basename):
    return "features/" + basename + ".csv"


#########################################################################
# Round all floating-point values to a given precision.
# Expects a list of dictionaries, and rounds the values (not keys) in
# every row of the dictionary.
def round_values(data, precision=3):
    for row in data:
        for k, v in row.items():
            if type(v) == type(0.1):
                row[k] = round(v, precision)


#########################################################################
# Given a mapping from dates to values, and a reference date (all strings),
# search the map for the closest date to the reference string, and return
# the value associated with that date.
# If there are no date values, or the closest date is too far from the
# reference date (exceeds max_gap days), return "NA".
def closest_date(values, reference, max_gap):
    if values == '':   # No GS record for this author
        return ''

    if len(values) == 0:
        return "NA"

    min_dist = 10000000
    closest_value = ''

    for d, v in values.items():
        dist = abs(day_diff(d, reference))
        if dist < min_dist:
            min_dist = dist
            closest_value = v

    return closest_value

#########################################################################
# Compute time difference between two date strings, in months, rounded down
def month_diff(first, second):
    return int(round(day_diff(first, second) / (365/12)))


#########################################################################
# Compute time difference between two date strings, in days
def day_diff(first, second):
    d1 = dt.strptime(first, "%Y-%m-%d")
    d2 = dt.strptime(second, "%Y-%m-%d")
    return (d1 - d2).days

#########################################################################
# Compute a date that is m months away from a give date.
def add_months(date, m):
    d = dt.strptime(date, "%Y-%m-%d")
    future = d + relativedelta(months = m)
    return future.strftime("%Y-%m-%d")

#########################################################################
# add_dummies: For each string in a list of variables, add a dummy variable
# to the given dictionary, in the form:
# is-{prefix}-{variable} = True
# (or False, if not there).
def add_dummies(dct, prefix, vars, all_vars):
    for v in all_vars:
        dct["is_" + prefix + "_" + v] = v in vars


#########################################################################
# Apply a statistical function on a 'cleaned' version of a list, meaning,
# excluding empty values and converting the rest to ints. If there are no
# clean values remaining, return the empty string ''.
def clean_stats(fun, values):
    clean = list(map(int, filter(lambda x : x != '', values)))
    if len(clean) == 0:
        return ''
    else:
        return fun(clean)


#########################################################################
# For a given list of author names and a function to access a value
# from an author record (given a name), fetch the list of all values for
# all names, and compute aggregate statistics on the list, such as min,
# max, mean, etc. Then, add fields to a 'record' dictionary to save these
# values, suffixed with a given property name string.
def set_author_stats(prop, record, names, accessor):
    values = [ accessor(a) for a in names ]

    record['mean_' + prop] = clean_stats(statistics.mean, values)
    record['median_' + prop] = clean_stats(statistics.median, values)
    record['min_' + prop] = clean_stats(min, values)
    record['max_' + prop] = clean_stats(max, values)

    if sum(1 for v in values if v != '') > 1:
        record['stdev_' + prop] = clean_stats(statistics.stdev, values)
    else:
        record['stdev_' + prop] = ''

    record['lead_' + prop] = values[0]
    record['last_' + prop] = values[-1]
