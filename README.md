

* This is an easybuild/easyconfig repository for JSC's JUAWEI cluster.
* The repository is based on https://github.com/easybuilders/JSC but includes some updates and AArch64-specific modifications
* The work here is heavily WIP and contains some ugly hacks
* Also the same disclaimers apply as with the public JSC repository: no compatibility guarantees, provided as-is, etc...

# Available Software

* Not all software that is available in the public JSC repository is available here. Specifically:
    * There is only 1 Stage: 2019b
    * Golden\_Repo/2019b-unconfirmed  contains Software that did not compile for the system or which has not been tested to compile.
    * Fewer available toolchains

# Setting up the software stack

## ARM software ##

* The armhpc easyconfig relies on ARM HPC Compiler modulefiles already being installed
    * The modules also need to be modified to remove all "module load $variable" lines as this seems to break dependency resolution in EasyBuild

## ARM HPC compiler and libtool ##

There are some hardcoded paths pointing to /opt/arm/xyz in the ARM HPC compiler installation. Fortunately version 19.3 installs into $PREFIX instead of $PREFIX/opt/arm (like previous versions), so you can just:


```
(IFS='
'
for i in `grep -Irl "\/opt\/arm\/" /opt/software/arm/`; do sed -i "s#/opt/arm/#/opt/software/arm/#g" $i; done)
```

this assumes /opt/software/arm as the installation prefix you chose for the ARM HPC compiler.

## ARM HPC compiler and binutils: ##
 
Currently, due to the order of loaded modules with the armhpc toolchain, the binutils from ARM's GCC module are used. This leads to a compilation failure for easyconfigs which require -fPIC (and maybe others). Most notable example being OpenMPI.

As a workaround, `module load armhpc/<version> binutils` and then build the software package with --detect-loaded-modules=ignore, i.e:

```
module load armhpc/19.2 binutils
eb OpenMPI-4.0.1-armhpc-19.2.eb --detect-loaded-modules=ignore
```

A proper fix may be possible by more tightly integrating the ARM HPC compiler (full custom module instead of a proxy module for ARM's TCL modules)

## System dependencies ##

### Neovim ###

* libuv-devel
* unibilium-devel
* libtermkey-devel
* msgpack-devel

### lua ###

* lpeg
* mpack

### ccls ###

* rapidjson-devel

## WIP instructions ##

* Install lua and lmod
* install 'ansicolors' lua package
* Download and install arm hpc compiler (/opt/software/arm)
* Set ARMOSPREFIX='RHEL/7' somewhere in /etc/profile.d (or SUSE/12 or whatever the OS is, this is used to load arm modules)
* Create Architecture Module in /opt/software/modulefiles/system (use system\_modules/Architecture/default.lua as template)
  * change local prefix = "/opt/software" to the path where software will be installed to
  * change common\_eb\_path  = "/opt/juawei-easyconfigs" to where this repository is
  * change setenv("EASYBUILD\_JOB\_BACKEND\_CONFIG", "/opt/config/gc3pie.cfg") to where the gc3pie config resides
  * the template loads the module arm-optimized-routines automatically, this has to exist
    * build arm-optimized-routines from https://github.com/ARM-software/optimized-routines/ 
    * create arm-optmized-routines module in /opt/software/modulefiles/system/
  * Edit Developers/InstallSoftware-2017.lua to set custom optimization/environment variables
    * set ARMOPTPREFIX somewhere (determines which armpl modules are loaded)
* Install SLURM (OpenMPI is configured to compile with SLURM support)
* Install other dependencies
* module use /opt/software/easybuild/modules/all (for easybuild)
* module use /opt/software/system/ (Architecture and arm-optimized-routines are here)
* module use /opt/juawei-easyconfigs/dev\_modules (Stage and Developers modules)
* module use /opt/software/arm/modulefiles (ARM compiler + ArmPL)
* module load EasyBuild Stages/2019b Developers/InstallSoftware-2017 Architecture/_your-architecture_
* cd /opt/juawei-easyconfigs/Golden\_Repo/2019b
* eb e/EasyBuild/EasyBuild-4.0.1.eb
* module unload EasyBuild
* module unuse /opt/software/easybuild/modules/all
* module use module use /opt/software/tx2/Stages/2019b/modules/all/Core/
* module load EasyBuild
* (prepare for disappointment)
* eb . (will probably fail, but will tell you what dependencies are missing, install them and try again)
* (Fix probably a lot of easyconfigs (hardcoded --with=/some/path paths for system sw) and try again)
* create /opt/software/tx2/Stages/2019b/UI/{Compilers/Tools}
* cd /opt/software/tx2/Stages/2019b/UI/Tools
* ln -s ../../modules/all/Core/{everything that isn't a compiler} ./
* cd ../Compilers
* ln -s ../../modules/all/Core/{All compilers} ./

# Notable Bugs

## libunwind asm ##
asm statements in include/libunwind-aarch64.h should be changed to \_\_asm

TODO: write patch instead of fixing manually after the fact

## failing checks/tests ##

* GMP-6.1.2-Clang-9.0.0 1/46 tests fail, check disabled
* mpi-enabled h5py fails sanity check, check disabled
