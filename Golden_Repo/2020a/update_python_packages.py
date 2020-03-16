#!/usr/bin/env python
import subprocess
import sys
import re
import argparse
import pprint

SOURCE_TGZ=''

def main(argv):
    parser = argparse.ArgumentParser("Checks python packages in easyconfig for updates and prints a list to be replace exts_list with")
    parser.add_argument('filename', metavar='easyconfig', nargs=1, help='EasyConfig file to be updated')

    args = parser.parse_args()

    print(args.filename[0])

    exec(open(args.filename[0]).read(), globals(), globals())
    for i,package in enumerate(exts_list):
        name = package[0]
        current_version = package[1]
        print(f"Checking if {name} has a version newer than {current_version}") 
        latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(name)], capture_output=True, text=True))
        latest_version = latest_version[latest_version.find('(from versions:')+15:]
        latest_version = latest_version[:latest_version.find(')')]
        latest_version = latest_version.replace(' ','').split(',')[-1]

        if latest_version == current_version:
            print(f"{name} seems up to date")
        else:
            exts_list[i] = (name, latest_version, package[2])
            print(f"{name} has a newer version: {latest_version}")

    pprint.pprint(exts_list,indent=4,sort_dicts=False)

if __name__ == "__main__":
    main(sys.argv)
