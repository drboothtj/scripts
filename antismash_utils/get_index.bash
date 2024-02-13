#!/bin/bash
### get index table from antismash .json
### Requires: jq (sudo apt install jq)
### Arguments: $1 : .json file path

jq -r '.records[].areas[] | [.start, .end, .products] | flatten | @tsv' $1

