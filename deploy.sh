#!/bin/bash

cat << EOF
This script will deploy an EasyBuild-based software stack
on this machine
EOF

printf "\n"

if [ "$EUID" -eq 0 ]
  then echo "Please don't run this script as root"
  exit -1
fi


echo -n "Checking if your OS has lsb_release: "
if ! command -v lsb_release &> /dev/null
then
	echo "not found"
	nolsb=1
else
	echo "found"
	nolsb=0
fi

printf "\n"

if [ "$nolsb" -eq "0" ]
then
	echo "Detecting your operating system with lsb_release:"
	OS=$(lsb_release -i | sed 's/\s\+/ /g' | cut -d' ' -f3-)
	OSVER=$(lsb_release -r | sed 's/\s\+/ /g' | cut -d' ' -f2-)
	OSARCH=$(uname -m)
        if [ "$OSVER" == "rolling" ]
	then
		OSVER="(rolling release)"
	fi

	echo "You are running $OS $OSVER on the $OSARCH architecture"
else
	echo "Proceeding without OS detection"
fi

sitecontact="unknown@unknown"
read -p "Please enter the email of the site contact: " sitecontact
if [[ $sitecontact == "" ]]
then
	echo "Can't proceed without a site contact!"
	exit 1
fi

default_swgroup=software
read -p "Please enter the name of the group that will manage software (default: $default_swgroup )" swgroup
if [[ $swgroup == "" ]]
then
	swgroup=$default_swgroup
fi

echo -n "Checking if $USER is part of group $swgroup... "

if id -nG "$USER" | grep -qw "$swgroup"
then
	echo "yes"
else
	echo "no. Please add the user to the group and try again."
	exit 1
fi

default_installpath=/software
read -p "Where would you like to install software? (default: $default_installpath )" installpath
if [[ $installpath == "" ]]
then
	installpath=$default_installpath
fi

echo -n "Checking if $installpath is writable... "

if [ -w "$installpath" ]
then
	echo "yes"
else
	echo no. aborting...
	exit 1
fi

env_scriptname=zz_eb_sw_stack.sh
default_scriptpath=/etc/profile.d/$env_scriptname
read -p "Where would you like to install the environment script? (Full path to the script, default: $default_scriptpath)" scriptpath
if [[ $scriptpath == "" ]]
then
	scriptpath=$default_scriptpath
fi

script_use_sudo=N
scriptdir=$(dirname $default_scriptpath)
echo -n "Checking if $scriptdir is writable... "

if [ -w "$scriptdir" ]
then
	echo "yes"
else
	read -p "no. use sudo? (Y/n)" script_use_sudo
	[[ $script_use_sudo == "" ]] && script_use_sudo=Y
	case $script_use_sudo in
		[Yy]* ) echo "will use sudo to write the environment script";;
		[Nn]* ) echo "aborting"; exit 1;;
		* ) echo "Invalid answer, aborting"; exit 1;;
	esac
fi

# Check if the repo is where the script is
repodir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -d $repodir/Golden_Repo ] && [ -d $repodir/templates ] && [ -d $repodir/dev_modules ] && [ -d $repodir/Custom_Toolchains ] && [ -d $repodir/Custom_EasyBlocks ] && [ -d $repodir/Custom_MNS ]
then
	echo Will use $repodir as the directory of the easyconfig repository
else
	echo $repodir is not the easyconfig repository. Did you move this script? Why would you do that?!
fi

printf "\n\n"

cat <<EOF
The software stack can be deployed for multiple platforms (at least one).
We will need a platform name, an architecture and a way to detect what platform 
a node belongs to for each (for now only a pattern to match HOSTNAME 
to in a bash case statement is supported).

Software will be installed in $installpath/\$platform_name.

The architecture in this context means the optimization flags and possibly a custom
environment that needs to be loaded. You must choose an architecture that is
supported. If you want to add a new architecture, you should add it by modifying
dev_modules/Developer/InstallSoftware.lua.in and this script.

EOF

platforms=()
defined_archs=(SandyBridge Haswell Piledriver Zen Zen2 Cortex-A72 Kunpeng920 ThunderX2)
declare -A platform_archs
declare -A platform_patterns
declare -A basearchs
archs_to_symlink=()

basearchs[SandyBridge]=x86_64
basearchs[Haswell]=x86_64
basearchs[Piledriver]=x86_64
basearchs[Zen]=x86_64
basearchs[Zen2]=x86_64
basearchs[Cortex-A72]=aarch64
basearchs[Kunpeng920]=aarch64
basearchs[ThunderX2]=aarch64
  
aarch64_exists=0
while true
do
	read -p "Enter the next platform (empty to stop): " nextplatform
	[[ "$nextplatform" != "" ]] || break;
	echo Following Architectures are already defined:
	for a in ${defined_archs[@]}
	do
		echo "  "$a
	done
	read -p "Enter the architecture name for $nextplatform: " nextarch
	if [[ "$nextarch" == "" ]]
	then
		echo "Can't add platform without an architecture!"
		continue
	fi
	read -p "Enter the pattern to match \$HOSTNAME against for $nextplatform: " nextpattern
	if [[ "$nextpattern" == "" ]]
	then
		echo "Can't add platform without a pattern!"
		continue
	fi
	platforms+=("$nextplatform")
	platform_archs["$nextplatform"]=$nextarch
	archs_to_symlink+=$nextarch
	if [[ "${basearchs["$nextarch"]}" == "aarch64" ]]
	then
		aarch64_exists=1
	fi
	platform_patterns["$nextplatform"]=$nextpattern
done

#remove duplicate architectures
IFS=" " read -r -a archs_to_symlink <<< "$(echo "${archs_to_symlink[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"

if [[ "${#platforms[@]}" == "0" ]]
then
	echo "Can't proceed without at least one platform"
	exit 1
fi

if [ "$aarch64_exists" -ne "0" ]
then
	defaultpath=$installpath/arm-tools.sh
	read -p "At least one platform is aarch64-based. Where to install the script loading aarch64-tools? (default: $defaultpath)" arm_tools_env_scriptpath
	[[ "$arm_tools_env_scriptpath" == "" ]] && arm_tools_env_scriptpath=$defaultpath

	#TODO: arm tools script
	touch $arm_tools_env_scriptpath
fi


echo "Creating a temporary directory to work in"
tmpdir=$(mktemp -d)

echo "Created $tmpdir"

echo "Writing environment script to $tmpdir/$env_scriptname"

cat << EOF > $tmpdir/$env_scriptname
#!/bin/bash

# LMOD SitePackage.lua location and style
export LMOD_PACKAGE_PATH=$installpath
export LMOD_AVAIL_STYLE="system:<en_grouped>"

# System modules (Architecture, etc...)
export MODULEPATH=\$MODULEPATH:$installpath/system/modulefiles

# Load sw stack
if [ -z \${EBSWSTAGE+x} ]; then
    . $installpath/switch_stage.sh -q
else
    . $installpath/switch_stage.sh -q -s \$EBSWSTAGE
fi

EOF

echo "Moving environment script to $scriptpath and setting permissions"
case $script_use_sudo in
	[Yy]* )
		sudo cp $tmpdir/$env_scriptname $scriptpath
		sudo chmod 755 $scriptpath
		;;
	[Nn]* )
		cp $tmpdir/$env_scriptname $scriptpath
		chmod 755 $scriptpath
		;;
esac


echo "Generating SitePackage.lua from $repodir/templates/SitePackage.lua.in"

declare -A sp_parameters
sp_parameters["SOFTWAREPREFIX"]="$installpath"
sp_parameters["SITECONTACT"]="$sitecontact"
sp_parameters["PLATFORMS"]="\"$(printf "%s," ${platforms[@]} | sed 's/.$//')\""

echo "Will perform the following substitutions: "
for key in "${!sp_parameters[@]}";
do
	echo "%$key% -> ${sp_parameters[$key]}"
done

cp $repodir/templates/SitePackage.lua.in $tmpdir/SitePackage.lua

for key in "${!sp_parameters[@]}";
do
	sed -i "s#%$key%#${sp_parameters[$key]}#g" $tmpdir/SitePackage.lua
done

echo moving SitePackage.lua to $installpath/SitePackage.lua
cp $tmpdir/SitePackage.lua $installpath/SitePackage.lua


develdir=$installpath/modules/devel/Developers
echo "Creating $develdir directory"
mkdir -p $develdir

echo "Generating InstallSoftware.lua from $repodir/dev_modules/InstallSoftware.lua.in"

declare -A is_parameters
is_parameters["SWGROUP"]="$swgroup"
is_parameters["SITECONTACT"]="$sitecontact"

echo "Will perform the following substitutions: "
for key in "${!is_parameters[@]}";
do
	echo "%$key% -> ${is_parameters[$key]}"
done

cp $repodir/dev_modules/Developers/InstallSoftware.lua.in $tmpdir/InstallSoftware.lua

for key in "${!is_parameters[@]}";
do
	sed -i "s#%$key%#${is_parameters[$key]}#g" $tmpdir/InstallSoftware.lua
done

echo Moving InstallSoftware.lua to $develdir/InstallSoftware.lua
cp $tmpdir/InstallSoftware.lua $develdir/InstallSoftware.lua

rm -rf $tmpdir

echo "Copying $repodir/dev_modules/Stages directory to $installpath/modules/devel/"
cp -r $repodir/dev_modules/Stages $installpath/modules/devel/


function platform_case() {
	platform=$1
	arch=$2
	basearch=$3
	pattern=$4
	cat <<EOF
    $pattern)
        platform="$platform"
        LOADARCH="$arch"
        BASEARCH="$basearch"
        ;;

EOF
}

platform_cases=""
for platform in ${platforms[@]}
do
	basearch=${basearchs[${platform_archs["$platform"]}]}
	platform_cases="$platform_cases $(platform_case $platform ${platform_archs["$platform"]} $basearch ${platform_patterns["$platform"]})"
done


currentstage=2021a
echo "Writing sw stack loading script to $installpath/switch_stage.sh"

cat << EOF > $installpath/switch_stage.sh
#!/bin/bash
quiet=0
stage="$currentstage"


OPTIND=1
while getopts "qs:" opt; do
    case \${opt} in
    q )
        quiet=1
        ;;
    s )
        stage=\$OPTARG
        quiet=1
        ;;
    \? )
        echo "Usage: \$0 [-s]"
        exit 0
        ;;
    esac
done
shift \$((OPTIND-1))

if [[ 0 == \$quiet ]]; then
    echo "Unloading all modules"
fi

if [[ -z \${EBSWSTAGE} ]];
then
    true
else
if [[ 0 == \$quiet ]]; then
    echo "\$EBSWSTAGE is set to \$EBSWSTAGE. Will use this stage"
fi
stage=\${EBSWSTAGE}
fi

case "\$HOSTNAME" in
    $platform_cases
    *) platform="unknown" ;;
esac
export ARCHITECTURE=\$LOADARCH

module --force purge
export SOFTWAREPREFIX=$installpath
export SOFTWAREPLATFORM=\$platform
export SOFTWAREROOT=$installpath/\$platform
export MODULEPATH=$installpath/\$platform/Stages/\$stage/UI/Compilers:$installpath/\$platform/Stages/\$stage/UI/Tools:$installpath/modules/system:$installpath/modules/custom

if [[ \$BASEARCH == "aarch64" ]]; then
    . $arm_tools_env_scriptpath
fi

if [[ -z \${EASYCONFIGREPO} ]];
then
    export EASYCONFIGREPO="$repodir"
fi

if [[ 0 == \$quiet ]]; then
    module load Architecture/\$LOADARCH
else
    module load Architecture/.\$LOADARCH
fi

if [[ 0 == \$quiet ]]; then
    echo "Switched to EasyBuild-based software-stack"
fi
EOF

archdir=$installpath/modules/system/Architecture
echo "Creating $archdir directory"
mkdir -p $archdir

echo "Platforms with the following architectures are present: "
for arch in ${archs_to_symlink[@]}
do
	echo $arch
done

tmpdir=$(mktemp -d)
echo "Creating somearch.lua from $repodir/templates/Architecture/somearch.lua.in"

declare -A arch_parameters
arch_parameters["PLATFORMS"]="$(printf "\"%s\"," ${platforms[@]} | sed 's/.$//')"

echo "Will perform the following substitutions: "
for key in "${!arch_parameters[@]}";
do
	echo "%$key% -> ${arch_parameters[$key]}"
done

cp $repodir/templates/Architecture/somearch.lua.in $tmpdir/somearch.lua

for key in "${!arch_parameters[@]}";
do
	sed -i "s#%$key%#${arch_parameters[$key]}#g" $tmpdir/somearch.lua
done

echo moving somearch.lua to $archdir/somearch.lua
cp $tmpdir/somearch.lua $archdir/somearch.lua

rm -rf $tmpdir

echo "Creating module symlinks for all Architectures."

archmaster=$archdir/somearch.lua
for arch in ${archs_to_symlink[@]}
do
	echo "Symlinking $archdir/$arch.lua -> $archmaster"
	ln -fs $archmaster $archdir/$arch.lua
	echo "Symlinking $archdir/.$arch.lua -> $archmaster"
	ln -fs $archmaster $archdir/.$arch.lua
done


read -p "Does the current node belong to one of the platforms? (perform dependency check/install optional software) (Y/n)" cur_node_depcheck
[[ $cur_node_depcheck == "" ]] && cur_node_depcheck=Y

case $cur_node_depcheck in
	[Yy]* ) echo "Continuing with depcheck/software install";;
	[Nn]* ) echo "finished "; exit 1;;
	* ) echo "Invalid answer, aborting"; exit 1;;
esac

if [ $OSARCH == "aarch64" ]
then
	read -p "You are on $OSARCH. Would you like to install Arm Compiler for Linux (ACfL)? Answer \"yes\" only if you have an ACfL licence. (y/N) " install_acfl
	[[ $install_acfl == "" ]] && install_acfl=N
	case $install_acfl in
		[Yy]* ) echo "will install ACfL";;
		[Nn]* ) echo "will not install ACfL";;
		* ) echo "Invalid answer, aborting"; exit 1;;
	esac
	
	read -p "You are on $OSARCH. Would you like to install Arm Optimized Routines? (Y/n) " install_aor
	[[ $install_aor == "" ]] && install_aor=Y
	case $install_aor in
		[Yy]* ) echo "will install Arm Optimized Routines";;
		[Nn]* ) echo "will not install Arm Optimized Routines";;
		* ) echo "Invalid answer, aborting"; exit 1;;
	esac
fi

#TODO: Check GCC version for flag support/ add flags for old GCC
# (Also this is actually just for aarch64.. but maybe the definitions
# in the module can be generated with this somehow in the future)
declare -A arch_cflags
arch_cflags[SandyBridge]="-march=sandybridge -mtune=sandybridge"
arch_cflags[Haswell]="-march=haswell -mtune=haswell"
arch_cflags[Piledriver]="-march=bdver2 -mtune=bdver2"
arch_cflags[Zen]="-march=znver1 -mtune=znver1"
arch_cflags[Zen2]="-march=znver2 -mtune=znver2"
arch_cflags[Cortex-A72]="-march=armv8-a+fp+simd+crc -mtune=cortex-a72"
# gcc 8.5.0 for example doesn't know tsv110 processor
#arch_cflags[Kunpeng920]="-march=armv8.2-a+crypto+dotprod+fp16fml -mcpu=tsv110+dotprod+fp16fml"
arch_cflags[Kunpeng920]="-march=armv8.2-a+crypto+dotprod+fp16fml"
arch_cflags[ThunderX2]="-march=armv8.1-a+fp+simd+crc -mtune=thunderx2t99"

aor_ver="21.02"
case $install_aor in
	[Yy]* )
		echo "Installing arm optimized routines for all architectures"
		for arch in ${archs_to_symlink[@]}
		do
			if [[ "$(uname -m)" != "${basearchs[$arch]}" ]]
			then
				echo "Skipping Architecture $arch (\$\(uname -m\) != ${basearchs[$arch]})"
				continue
			fi
			aor_path=$installpath/libs/arm-optimized-routines/$aor_ver/$arch
			echo "Installing arm optimized routines version $aor_ver into $aor_path"
			tmpdir=$(mktemp -d)
			olddir=$(pwd)
			cd $tmpdir
			curl -LO https://github.com/ARM-software/optimized-routines/archive/refs/tags/v$aor_ver.tar.gz
			tar xaf v$aor_ver.tar.gz
			cd optimized-routines-$aor_ver
			cp config.mk.dist config.mk
			sed -i "/^#CFLAGS_SHARED = -fPIC -mcmodel=tiny$/a CFLAGS += ${arch_cflags[$arch]}" config.mk
			make -j$(($(nproc)+1)) || exit 1
			# wrong lib name in v21.02
			if [[ "$aor_ver" == "21.02" ]]
			then
				mv build/lib/libnetworking{lib,}.a
			fi
			make DESTDIR=$aor_path install || exit 1

			echo "Creating arm-optimized-routines/$aor_ver.lua from $repodir/templates/aor.lua.in"
			declare -A aor_parameters
			aor_parameters["AORVER"]="$aor_ver"
			aor_parameters["SOFTWAREPREFIX"]="$installpath"

			echo "Will perform the following substitutions: "
			for key in "${!aor_parameters[@]}";
			do
				echo "%$key% -> ${aor_parameters[$key]}"
			done

			cp $repodir/templates/aor.lua.in $tmpdir/aor.lua

			for key in "${!aor_parameters[@]}";
			do
				sed -i "s#%$key%#${aor_parameters[$key]}#g" $tmpdir/aor.lua
			done

			aor_mod_dir=$installpath/modules/custom/arm-optimized-routines/
			echo creating $aor_mod_dir directory
			mkdir -p $aor_mod_dir
			echo moving aor.lua to $aor_mod_dir/$aor_ver.lua
			cp $tmpdir/aor.lua $aor_mod_dir/$aor_ver.lua
			cd $olddir
			rm -rf $tmpdir
		done
        ;;
	[Nn]* )
	;;
esac

echo "Checking for dependencies"

function ywn() {
	echo "You will need $1 for this, so install it please!"
}

function ywnlua() {
	echo "You will need lua module $1 for this. Please install it with your distros package manager or luarocks"
}

echo -n "Checking for GCC... "

if ! command -v gcc &> /dev/null
then
	echo "not found"
	echo $(ywn GCC)
	exit 1
else
	sysgccver=$(gcc --version | grep ^gcc | cut -d' ' -f3)
	sysgccmaj=$(echo $sysgccver | cut -d'.' -f1)
	sysgccmin=$(echo $sysgccver | cut -d'.' -f2)
	sysgccpatch=$(echo $sysgccver | cut -d'.' -f3)
	echo "found. version: $sysgccmaj.$sysgccmin.$sysgccpatch"
fi

echo -n "Checking for lua... "

if ! command -v lua &> /dev/null
then
	echo "not found"
	echo $(ywn lua)
	exit 1
else
	echo "found"
fi

echo -n "Checking for lzip... "

if ! command -v lzip &> /dev/null
then
	echo "not found"
	echo $(ywn lzip)
	exit 1
else
	echo "found"
fi

echo "Checking for required lua modules"

luareqs=(ansicolors posix)

for req in ${luareqs[@]}
do
	echo -n "Looking for lua module $req... "
	if echo "require(\"$req\")" | lua 2>&1 | grep "not found" > /dev/null
	then
		echo "not found"
		echo $(ywnlua "$req")
		exit 1
	else
		echo "found"
	fi
done

echo -n "Checking for Lmod... "

if [ -z $LMOD_CMD ]
then
	echo "not found. Please install Lmod and/or make sure LMOD_CMD is set"
	exit 1
else
	echo "found"
fi

echo -n "Checking for module() function... "

if [[ $(type -t module) == function ]]
then
	echo "found"
else
	echo "not found. Please fix your Lmod installation!"
	exit 1
fi

tmpdir=$(mktemp -d)
echo "Now installing EasyBuild into a temporary location ($tmpdir)"

pip3 install --prefix "$tmpdir" easybuild
pysuff=$(pip3 --version | sed "s/.*python\([0-9]\.[0-9].*\)\/.*/\1/g")

OLDPATH=$PATH
OLDPYTHONPATH=$PYTHONPATH
echo "Adding $tmpdir/bin to PATH"
export PATH=$tmpdir/bin:$PATH
echo "Adding $tmpdir/lib/python$pysuff/site-packages to PYTHONPATH (check if this is correct, Im not sure)"
export PYTHONPATH=$tmpdir/lib/python$pysuff/site-packages:$PYTHONPATH

echo -n "Checking if eb --version works... "

if eb --version >/dev/null
then
	echo "yes"
else
	echo "no. aborting"
	exit 1
fi


# installing repo EasyBuild 
stages=(2021a)
declare -A stage_eb_version
stage_eb_version[2021a]="4.3.4"

echo Installing EasyBuild from repo for all stages and architectures
for stage in ${stages[@]}
do
	for arch in ${archs_to_symlink[@]}
	do
		if [[ "$(uname -m)" != "${basearchs[$arch]}" ]]
		then
			echo "Skipping Architecture $arch (node has different basearch)"
			continue
		fi
		echo "Installing EasyBuild from stage $stage for $arch"
		olddir=$(pwd)
		cd $repodir/Golden_Repo/$stage/
		. $installpath/switch_stage.sh -q -s $stage
		module use $installpath/modules/system || exit 1
		module use $installpath/modules/devel || exit 1
		export NOEBMODULE=yes
		module load Stages/$stage Developers/InstallSoftware Architecture/$arch || exit 1
		eb e/EasyBuild/EasyBuild-${stage_eb_version[$stage]}.eb || exit 1
		cd $olddir
	done
done

echo resetting PATH to $OLDPATH
export PATH=$OLDPATH
echo resetting PYTHONPATH to $OLDPYTHONPATH
export PYTHONPATH=$OLDPYTHONPATH

rm -rf $tmpdir
