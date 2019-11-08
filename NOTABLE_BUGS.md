# ARM HPC compiler and binutils: #
 
Currently, due to the order of loaded modules with the armhpc toolchain, the binutils from ARM's GCC module are used. This leads to a compilation failure for easyconfigs which require -fPIC (and maybe others). Most notable example being OpenMPI.

A proper fix may be possible by more tightly integrating the ARM HPC compiler (full custom module instead of a proxy module for ARM's TCL modules)

## Workaround: ##

Simply do `module load armhpc/<version> binutils` and then build the software package with --detect-loaded-modules=ignore, i.e:

```
module load armhpc/19.2 binutils
eb OpenMPI-4.0.1-armhpc-19.2.eb --detect-loaded-modules=ignore
```


