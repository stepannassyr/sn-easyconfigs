# Jülich Supercomputing Centre JUAWEI easyconfig repository

* This is an easybuild/easyconfig repository for JSC's JUAWEI cluster.
* The repository is based on https://github.com/easybuilders/JSC but includes some updates and AArch64-specific modifications
* The work here is heavily WIP and contains some ugly hacks
* Also the same disclaimers apply as with the public JSC repository: no compatibility guarantees, provided as-is, etc...

# Available Software

* Not all software that is available in the public JSC repository is available here. Specifically:
    * There is only 1 Stage: 2019b
    * Golden\_Repo/2019b-unconfirmed  contains Software that did not compile for the system or which has not been tested to compile.
    * Fewer available toolchains
