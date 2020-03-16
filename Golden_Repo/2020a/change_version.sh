#!/bin/bash

display_usage() {
	echo "EasyConfig version update:"
	echo "Generates new .eb file for the new version and upgrades"
	echo "other easyconfigs to depend on the new version"
	echo "(Only works if the dependency is written explicitly, i.e"
	echo "('Library', '0.1.2'), won't work if variables is used)"
	echo "\n"
	echo "Usage: $0 software_name old_version new_version"
	echo "\n"
}

if [ $# -le 2 ] || [ $# -ge 4 ]
then
	display_usage
	exit 1
fi
# Update easyconfig
find . -name "*$1-$2*.eb" -exec sh -c "fname={};sed \"s/version\s*=\s*'$2'/version = '$3'/g\" \$fname > \${fname/$1-$2/$1-$3}" \;

# Update dependencies
for i in $(grep -lr "'$1',\s*'$2'"); do
	sed -i "s/'$1',\s*'$2'/'$1', '$3'/g" $i;
done

for i in $(grep -lr "\-$1-$2"); do
	sed -i "s/\-$1\-$2/\-$1\-$3/g" $i;
done
