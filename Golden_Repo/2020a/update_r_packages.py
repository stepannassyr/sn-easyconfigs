#!/usr/bin/env python
import re
import argparse
import pprint
import gzip
import sys
import requests

SOURCE_TGZ=''
SOURCE_TAR_GZ=''
SOURCELOWER_TAR_GZ=''

def main(argv):
    parser = argparse.ArgumentParser("Checks R packages in easyconfig for updates and prints a list to be replace exts_list with")
    parser.add_argument('filename', metavar='easyconfig', nargs=1, help='EasyConfig file to be updated')

    args = parser.parse_args()

    print(args.filename[0])

    pkg_url = "https://cran.r-project.org/src/contrib/PACKAGES.gz"

    # Yay no error handling at all
    pkg_archive = requests.get(pkg_url).content
    pkg_data = gzip.decompress(pkg_archive)
    pkg_lines = pkg_data.decode().splitlines()

    pkg_versions = {}

    package_regex = re.compile("^Package: (.*)$")
    version_regex = re.compile("^Version: (.*)$")

    cur_pkg = ""
    cur_ver = ""

    for line in pkg_lines:
        line = line.strip()
        pmatch = package_regex.match(line)
        if pmatch:
            cur_pkg = pmatch.group(1)
            continue
        vmatch = version_regex.match(line)
        if vmatch:
            cur_ver = vmatch.group(1)
            pkg_versions[cur_pkg] = cur_ver
            continue


    exec(open(args.filename[0]).read(), globals(), globals())

    remove_list = []
    update_list = []
    for i,package in enumerate(exts_list):
        if tuple != type(package):
            continue
        name = package[0]
        # remove packages that aren't on cran
        if not name in pkg_versions:
            remove_list.append(i)
            continue
        if 'modulename' in package[2]:
            name = package[2]['modulename']
        current_version = package[1]
        print(f"Checking if {name} has a version newer than {current_version}")

        latest_version = pkg_versions[name]

        if (latest_version == current_version) or ('undef' == latest_version):
            print(f"{name} seems up to date")
        else:
            exts_list[i] = (name, latest_version, package[2])
            update_list.append((name,latest_version))
            print(f"{name} has a newer version: {latest_version}")
    new_list = [exts_list[i] for i in range(len(exts_list)) if i not in remove_list]

    pprint.pprint(new_list,indent=4,sort_dicts=False)

    print("Only updates:")
    pprint.pprint(update_list,indent=4,sort_dicts=False)

if __name__ == "__main__":
    main(sys.argv)