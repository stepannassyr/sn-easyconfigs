The table below shows the details of the toolchains in the 2020a stage:

| Toolchain name |     Toolchain version     | Underlying GCC |         Compiler          |          MPI           | Math libraries |  Includes software from   |                          Notes                           |
|----------------|---------------------------|----------------|---------------------------|------------------------|----------------|---------------------------|----------------------------------------------------------|
| GCCcore        | 9.3.0                     | 9.3.0          |                           |                        |                |                           | Used for boostrapping other compilers and basic software |
| GCC            | 9.3.0                     | 9.3.0          | GCC 9.3.0                 |                        |                | GCCcore                   | Compiler toolchain                                       |
| Clang          | 9.0.1                     |                | Clang 9.0.1               |                        |                |                           | Compiler toolchain                                       |
| armlinux         | 20.0                      |                | Arm compiler for HPC 20.0 |                        |                |                           | Compiler toolchain                                       |
| gompi          | 2020a                     | 9.3.0          | GCC 9.3.0                 | OpenMPI 4.0.3          |                | GCCcore, GCC              | Compiler+MPI toolchain                                   |
| alompi          | 20.0                      |                | Arm compiler for HPC 20.0 | OpenMPI 4.0.3          |                | armlinux                    | Compiler+MPI toolchain                                   |
| goolf          | 2020a                     | 9.3.0          | GCC 9.3.0                 | OpenMPI 4.0.3          | OpenBLAS 0.3.9 | GCCcore, GCC, gompi       | Compiler+MPI+Math toolchain                              |
| alplompi        | 20.0                      |                | Arm compiler for HPC 20.0 | OpenMPI 4.0.3          | Arm PL 20.0    | armlinux, alompi             | Compiler+MPI+Math toolchain                              |
