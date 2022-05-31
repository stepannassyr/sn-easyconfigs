

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
~: ./deploy.sh
```
and follow the instructions
