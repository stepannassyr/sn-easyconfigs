#!/usr/bin/env python
import re
import argparse
import pprint
import gzip
import sys
import requests
import os

# We need to define these so the easyconfig doesn't complain
SOURCE_TGZ=''
SOURCELOWER_TAR_GZ=''

def main(argv):
    parser = argparse.ArgumentParser("Checks perl packages in easyconfig for updates and prints a list to be replace exts_list with")
    parser.add_argument('filename', metavar='easyconfig', nargs=1, help='EasyConfig file to be updated')

    args = parser.parse_args()

    print(args.filename[0])

    pkg_url = "https://www.cpan.org/modules/02packages.details.txt.gz"

    # TODO: Error handling
    pkg_archive = requests.get(pkg_url).content
    pkg_data = gzip.decompress(pkg_archive)
    pkg_lines = pkg_data.decode().splitlines()

    pkg_versions = {}
    pkg_source_urls = {}

    for line in pkg_lines: 
        line = line.strip() 
        linelist = line.split() 
        if len(linelist) == 3: 
            pkg_versions[linelist[0]] = linelist[1] 
            pkg_source_urls[linelist[0]] = 'https://cpan.metacpan.org/authors/id/'+os.path.dirname(linelist[2])


    # Run the easyconfig like a python script. Purpose: get exts_list from easyconfig
    exec(open(args.filename[0]).read(), globals(), globals())
    for i,package in enumerate(exts_list):
        name = package[0]
        if 'modulename' in package[2]:
            name = package[2]['modulename']
        current_version = package[1]
        print(f"Checking if {name} has a version newer than {current_version}") 

        latest_version = pkg_versions[name]
        source_url = pkg_source_urls[name]

        if (latest_version == current_version) or ('undef' == latest_version):
            print(f"{name} seems up to date")
        else:
            exts_list[i] = (name, latest_version, package[2])
            print(f"{name} has a newer version: {latest_version}")
        if(  package[2]['source_urls'][0] != source_url):
            package[2]['source_urls'] = [source_url]
            print(f"{name} has a new source_url: {source_url}")

    pprint.pprint(exts_list,indent=4,sort_dicts=False)

if __name__ == "__main__":
    main(sys.argv)
