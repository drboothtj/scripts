#!/usr/bin/env python3
'''
download a file from anti-smash-db using the URL
	argv[1]: the url of an antismash-db accession
'''
import json
import requests
import os
import sys

REGION_GBK_URL = "https://antismash-db.secondarymetabolites.org/output/{assembly_id}/{acc}.{version}.region{region_number:03d}.gbk"

def download_from_go_url(url):
    # reformat to get the actual JSON from the (presumably non-functional) /go/ URL
    url = url.replace("/go/", "/api/v1.0/area/")
    response = requests.get(url)
    data = json.loads(response.content)["clusters"]
    if len(data) > 1:
        raise ValueError("multiple results exist for ", " ".join(url.rsplit()[-2:]))
    gbk_url = REGION_GBK_URL.format(**data[0])
    response = requests.get(gbk_url)
    if response.status_code == 404:
        gbk_url = gbk_url.replace(".{version}.region".format(**data[0]), ".region")
        response = requests.get(gbk_url)
        if response.status_code == 404:
            raise ValueError("couldn't access: {assembly_id} {acc}[.{version}] region {region_number}".format(**data[0]))
                
    data = response.content
    with open(gbk_url.rsplit("/", 1)[-1], "w") as handle:
        handle.write(data.decode())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"USAGE: {os.basename(sys.argv[0])} download_url")
        sys.exit(1)
    download_from_go_url(sys.argv[1])
