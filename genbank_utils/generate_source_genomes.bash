#!/bin/bash
# this is a janky script I made to search for protein IDs in the heads of genbank files
# probably not useful for any other application...
# agruments:
#   $1: file with list of protein IDs
#   $2 : location of directory containing headers
 
for line in `cat $1`; do echo $line | cut -c1-8 | xargs -I X grep X $2 -l | cut -c10-18; done
