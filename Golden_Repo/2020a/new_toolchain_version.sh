#!/bin/bash

display_usage() {
	echo "EasyConfig toolchain update:"
    echo "Generates new .eb file for the toolchain (if it" 
    echo "doesn't exist already), and creates new easyconfigs"
	echo "for all software that was built with the old"
    echo "version of the toolchain. The new easyconfigs"
    echo "will be built with the new version of the toolchain"
    echo "If an easyconfig explicitly depends on the toolchain"
    echo "the version of the dependency is also updated"
	echo "\n"
	echo "Usage: $0 toolchain_name old_version new_version"
	echo "\n"
}

if [ $# -le 2 ] || [ $# -ge 4 ]
then
	display_usage
	exit 1
fi
# Update easyconfig
find . -name "*-$1-$2*.eb" -exec sh -c "fname={};newfname=\${fname/-$1-$2/-$1-$3}; echo creating \$newfname; sed \"s/'$1'\s*,\s*'version'\s*:\s*'$2'/'$1', 'version': '$3'/g\" \$fname > \$newfname" \;

# Update dependencies
for i in $(grep -lr "'$1',\s*'$3'"); do
    echo updating $i
	sed -i "s/'$1',\s*'$2'/'$1', '$3'/g" $i;
done
