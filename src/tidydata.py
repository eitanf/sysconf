#!/usr/bin/env python3
#
# The TidyData class allows building a documented CSV file with tidy data.
# The data+doc set consists of a Tidy CSV data file (with headers) and an
# accompanying .md file that documents each field in order (both files reside
# in the same directory), as well as a general preamble for the file.
#
# Usage:
#   1) Create a TidyData object with a base filename and short description of the file's contents
#   2) For every new row of data, call start_record()
#   3) For every column, call add(), including column name, type, and description
#   4) Continue adding new rows, one per sample.
#   5) When finished, call save(), with an optional rounding factor for numbers.

import csv
import json
import os
import sys
from shared_utils import round_values

class TidyData:
    def __init__(self, basename, contains):
        '''
        Initialize TidyData with the base filename and the preamble text
        describing its content.
        '''
        self.__base = basename
        self.__preamble = contains
        self.__fields = []
        self.__fieldnames = []
        self.__records = []


    ##########################################################################
    ### Move on to a new record (row), to which we add one field at a time:
    def start_record(self):
        self.__records.append({})


    ##########################################################################
    ### Print all internal values, for debugging:
    def print_records(self):
        for row in self.__records:
            for k, v in row.items():
                print(k,"\t",v)


    ##########################################################################
    ### Add one field to the current record. The field has a name and a value,
    # as well as a field type and description, that are saved on the first time
    # this field name is encountered.
    # Fields (columns) will be written out to CSV file in the order they were
    # first added using add(). Rows are written in the order they're added.
    def add(self, name, ftype, value, description):
        if not self.__records:
            raise Exception("Can't add a field without starting a new record")

        if name not in self.__fieldnames:
            self.__fields.append({ "name": name, "type": ftype, "desc": description })
            self.__fieldnames.append(name)

        self.__records[-1][name] = value


    ##########################################################################
    ### When you're done adding records, call save() to create the CSV file
    # and the accompanying .md description file.
    def save(self, rounding_digits = 3):
        dir = "features/"
        round_values(self.__records, rounding_digits)

        with open(dir + self.__base + ".md", "w", encoding='utf-8') as f:
            f.write("The file `" + self.__base + ".csv` contains ")
            f.write(self.__preamble)
            f.write("\nThe data was generated by `" + sys.argv[0])
            f.write("` from git hash " + os.popen("git rev-parse --short HEAD").read())
            f.write("\n\n### Field description\n\n")

            for field in self.__fields:
                f.write("  * `" + field["name"] + "` ")
                f.write("(" + field["type"] + "): ")
                f.write(field["desc"] + ".\n")

        with open(dir + self.__base + ".csv", "w", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = self.__fieldnames)
            writer.writeheader()
            writer.writerows(self.__records)
