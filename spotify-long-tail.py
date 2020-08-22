#!/usr/bin/env python
# encoding: utf-8
"""
This script takes a list of artists as input (one artist per line) and searches
for them on Spotify, determining how many of the given artists are available.

Code by Markus Amalthea Magnuson <markus@polyscopic.works>
"""

import sys
import time
import urllib2

import spotimeta

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    sys.exit("You must specify an input file as first argument.")

# open artist list, count lines and reset line pointer
f = open(path, "r")
no_lines = len(f.readlines())
if no_lines == 0:
    sys.exit("The input file seems to be empty.")
f.seek(0)

# run a cached spotify metadata instance
metacache = {}
metadata = spotimeta.Metadata(cache=metacache)

# let's search
no_found = 0.0  # use a float to enable true division when printing results
for counter, line in enumerate(f, start=1):
    line = line.strip()
    print "Searching for '%s' (%i of %i)" % (line, counter, no_lines),

    attempts = 0
    success = False
    while attempts < 5:
        try:
            data = metadata.search_artist(line.decode("utf-8"))
            success = True
            break
        except urllib2.HTTPError:
            attempts += 1

    if not success:
        continue

    if data["total_results"] > 0:
        print "\nFound:"
        for result in data["result"]:
            print "    %s" % (result["name"])
        no_found += 1
    else:
        print "[not found]"

    print "\n",
    time.sleep(0.1)  # avoid hammering the spotify server

# print results
print "Found %i out of %i artists (%.2f%%)" % (
    no_found,
    no_lines,
    (no_found / no_lines) * 100,
)
