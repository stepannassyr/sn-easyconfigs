The table below shows the details of the toolchains in the 2019b stage:

| Toolchain name |     Toolchain version     | Underlying GCC |         Compiler          |          MPI           | Math libraries |  Includes software from   |                          Notes                           |
|----------------|---------------------------|----------------|---------------------------|------------------------|----------------|---------------------------|----------------------------------------------------------|
| GCCcore        | 9.2.0                     | 9.2.0          |                           |                        |                |                           | Used for boostrapping other compilers and basic software |
| GCC            | 9.2.0                     | 9.2.0          | GCC 9.2.0                 |                        |                | GCCcore                   | Compiler toolchain                                       |
| armhpc         | 19.2                      |                | Arm compiler for HPC 19.2 |                        |                |                           | Compiler toolchain                                       |
| armhpc         | 19.3                      |                | Arm compiler for HPC 19.3 |                        |                |                           | Compiler toolchain                                       |
| gompi          | 2019b                     | 9.2.0          | GCC 9.2.0                 | OpenMPI 4.0.1          |                | GCCcore, GCC              | Compiler+MPI toolchain                                   |
| aompi          | 19.2                      |                | Arm compiler for HPC 19.2 | OpenMPI 4.0.1          |                | armhpc                    | Compiler+MPI toolchain                                   |
| aompi          | 19.3                      |                | Arm compiler for HPC 19.3 | OpenMPI 4.0.1          |                | armhpc                    | Compiler+MPI toolchain                                   |
| goolf          | 2019b                     | 9.2.0          | GCC 9.2.0                 | OpenMPI 4.0.1          | OpenBLAS 0.3.7 | GCCcore, GCC, gompi       | Compiler+MPI+Math toolchain                              |
| aplompi        | 19.2                      |                | Arm compiler for HPC 19.2 | OpenMPI 4.0.1          | Arm PL 19.2    | armhpc, aompi             | Compiler+MPI+Math toolchain                              |
| aplompi        | 19.3                      |                | Arm compiler for HPC 19.3 | OpenMPI 4.0.1          | Arm PL 19.3    | armhpc, aompi             | Compiler+MPI+Math toolchain                              |
