#! /usr/bin/python
import sys

source_file = str(sys.argv[1])
print 'File name:', source_file

output_file = source_file.replace('.','-clean.',1)

# This program opens file bar.txt and removes duplicate lines and writes the
# contents to foo.txt file.
lines_seen = set()  # holds lines already seen
outfile = open(output_file, "w")
infile = open(source_file, "r")

for line in infile:
    # print line
    if line not in lines_seen:  # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

print "The source file = " + source_file
print "The clean  file = " + output_file