

* This is an easybuild/easyconfig repository for JSC's JUAWEI,JUMAX,CTX2 systems and on FIAS/GUF's HAICGU cluster.
* The repository was forked in 2019 from https://github.com/easybuilders/JSC but has diverged since.
* Includes patches and fixes, mostly focusing on ARM/AArch64
* The work here is heavily WIP and contains some ugly hacks
* Also the same disclaimers apply as with the public JSC repository: no compatibility guarantees, provided as-is, etc...

# Available Software

* Available Stages:
    * 2022a
* Available Compilers: armlinux (ACfL), GCC, Clang
* Available MPI: OpenMPI
* Available BLAS/LAPACK/FFT: Arm PL, OpenBLAS 
* For available versions/combinations see Golden\_Repo/README.md

# Setting up the software stack

run 
```
./deploy.sh
```
and follow the instructions

After the script ran through you can set up the environment for installation with:

```
module use /<installation dir>/modules/devel
module load EasyBuild Stages/<stage> Developers Architecture/<Architecture>
```
i.e for the default installation directory, stage `2022a` and the Haswell architecture:
```
module use /software/modules/devel
module load EasyBuild Stages/2022a Developers Architecture/Haswell
```
Then `cd` into the `Golden_Repo` subdirectory and install packages with the `eb` command:
```
cd Golden_Repo
eb o/OpenMPI/OpenMPI-4.1.3-GCC-12.1.0.eb
```
