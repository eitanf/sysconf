#!/usr/bin/env python3

import re
import sys

lines = sys.stdin.readlines()

counts = {}
section = ""

def count(section, line):
    if section not in counts:
        counts[section] = 0
    counts[section] += len(line.split())

skip = False

for i in range(len(lines)):
    line = lines[i].rstrip()

    if line.startswith("```"):
        if skip:
            skip = False
        else:
            skip = True
        continue

    if skip:
        continue

    if line.startswith("abstract: "):
        while True:
            i += 1
            line = lines[i].rstrip()
            if not line.startswith(" | "):
                break
            count("Abstract", line[2:])

    elif re.match("# [A-Z]", line):
        section = line.split()[1]

    elif section != "":
        count(section, line)

for sec,cnt in counts.items():
    print(sec, cnt)



