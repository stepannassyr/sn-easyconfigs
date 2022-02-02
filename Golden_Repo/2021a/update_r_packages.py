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
    pkg_md5s     = {}
    pkg_depends  = {}

    package_regex = re.compile("^Package: (.*)$")
    version_regex = re.compile("^Version: (.*)$")
    md5_regex = re.compile("^MD5sum: (.*)$")
    path_regex = re.compile("^Path: ([\d.]*)/(.*)$")
    depends_regex = re.compile("^Depends:\s*(.*)$")
    imports_regex = re.compile("^Imports:\s*(.*)$")

    cur_pkg = ""
    cur_ver = ""
    cur_md5 = ""
    cur_depends = ""

    # "read in" the EasyConfig
    exec(open(args.filename[0]).read(), globals(), globals())
    cur_path = version[:3]
    print(f"current path: {cur_path}")


    gathering_deps=False
    for line in pkg_lines:
        if gathering_deps:
            if ' ' != line[0]:
                cur_depends+=','
                gathering_deps=False
        line = line.strip()
        pmatch = package_regex.match(line)
        if pmatch:
            if (version[:3] == cur_path[:3]):
                pkg_versions[cur_pkg] = cur_ver
                pkg_md5s[cur_pkg] = cur_md5
                pkg_depends[cur_pkg] = cur_depends.split(',')
            cur_pkg = pmatch.group(1)
            cur_path = version[:3]
            cur_depends = ""
            continue
        vmatch = version_regex.match(line)
        if vmatch:
            cur_ver = vmatch.group(1)
            continue
        md5match = md5_regex.match(line)
        if md5match:
            cur_md5 = md5match.group(1)
            continue
        pathmatch = path_regex.match(line)
        if pathmatch:
            cur_path = pathmatch.group(1)[:3]
            print(f"matched path, switching path to {cur_path}")
            continue
        dependsmatch = depends_regex.match(line)
        if dependsmatch:
            gathering_deps=True
            cur_depends += ' '+dependsmatch.group(1)+' '
            continue
        importsmatch = imports_regex.match(line)
        if importsmatch:
            gathering_deps=True
            cur_depends += ' '+importsmatch.group(1)+' '
            continue
        if gathering_deps:
            cur_depends += ' '+line+' '

    # Straighten out dependencies:

    ordered_list = []
    # Whatever is provided by base R
    gathered_deps = ['R','parallel','tcltk','compiler']
    resolve_list = exts_list
    naughty_count = 0
    while resolve_list:
        naughty_list = []
        # iterate over all packages in list
        missing_deps = []
        for package in resolve_list:
            if package in ordered_list:
                if tuple != type(package):
                    print(f"{package} already in list, skipping")
                else:
                    print(f"{package[0]} already in list, skipping")
                continue
            if tuple != type(package):
                ordered_list.append(package)
                gathered_deps.append(package)
                continue
            name = package[0]
            if not name in pkg_versions:
                ordered_list.append(package)
                gathered_deps.append(name)
                continue
            # Check if it has any dependencies
            if pkg_depends[name]:
                naughty = False
                # for each dependency check if it has already been seen
                for dep in pkg_depends[name]:
                    dep = dep.replace(' ','')
                    # spaces get in sometimes
                    if not dep:
                        continue
                    dep = dep.partition('(')[0]
                    if not dep in gathered_deps:
                        print(f"{name} depends on {dep}, but {dep} has not been seen yet, adding {name} to naughty list")
                        # If not add to naughty list
                        if not dep in missing_deps:
                            missing_deps.append(dep)
                        if not naughty:
                            naughty_list.append(package)
                        naughty_count += 1
                        naughty = True
                if naughty:
                    continue
            ordered_list.append(package)
            gathered_deps.append(name)
            if name in missing_deps:
                missing_deps.remove(name)
        dep_pkg_list = []
        naughty_names = [p[0] for p in naughty_list]
        if missing_deps:
            for dep in missing_deps:
                if dep in naughty_names:
                    # Already in the naughty list, no need to add
                    print(f"{dep} already in naughty list, no need to add to dep list")
                    continue
                if not dep in pkg_versions:
                    # optimistically just ignore it
                    print(f"Can't find {dep} in PACKAGES, optimistically assuming it's provided by base R")
                    gathered_deps.append(dep)
                    continue
                dep_pkg_list.append((dep,pkg_versions[dep], {'checksums': [pkg_md5s[dep]]}))
        resolve_list = dep_pkg_list
        resolve_list.extend(naughty_list)

    print(f"Naughty check triggered {naughty_count} times (if this number gets too big, rework the algorithm)")


    remove_list = []
    update_list = []
    for i,package in enumerate(ordered_list):
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
        current_md5  = package[2]['checksums'][0]
        print(f"Checking if {name} has a version newer than {current_version}")

        latest_version = pkg_versions[name]
        latest_md5     = pkg_md5s[name]

        if ((latest_version == current_version) or ('undef' == latest_version)) and (latest_md5 == current_md5):
            print(f"{name} seems up to date")
        elif latest_version != current_version and not ('undef' == latest_version):
            package[2]['checksums'][0] = latest_md5
            ordered_list[i] = (name, latest_version, package[2])
            update_list.append((name,latest_version))
            print(f"{name} has a newer version: {latest_version}")
        else:
            package[2]['checksums'][0] = latest_md5
            ordered_list[i] = (name, latest_version, package[2])
            update_list.append((name,latest_version))
            print(f"{name} has a different md5sum. Current: {current_md5}")
            print(f"                               latest:  {latest_md5}")
            
    new_list = [ordered_list[i] for i in range(len(ordered_list)) if i not in remove_list]

    if sys.version_info >= (3,8):
        pprint.pprint(new_list,indent=4,sort_dicts=False)
    else:
        pprint.pprint(new_list,indent=4)

    print("Only updates:")
    if sys.version_info >= (3,8):
        pprint.pprint(update_list,indent=4,sort_dicts=False)
    else:
        pprint.pprint(update_list,indent=4)

if __name__ == "__main__":
    main(sys.argv)
