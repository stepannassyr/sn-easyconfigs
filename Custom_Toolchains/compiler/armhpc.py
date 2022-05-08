##
# Copyright 2013-2019 Ghent University
# Copyright 2019 Forschungszentrum Juelich
#
# This file is triple-licensed under GPLv2 (see below), MIT, and
# BSD three-clause licenses.
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Support for ARM compiler for HPC (armclang) as toolchain compiler.
Base on clang.py

:author: Stepan Nassyr (Forschungszentrum Juelich)
"""

import os
import easybuild.tools.systemtools as systemtools
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.toolchain.compiler import Compiler

TC_CONSTANT_ARMHPC = "ArmHPC"


class ArmHPCcompiler(Compiler):
    """ArmHPC compiler class"""

    COMPILER_MODULE_NAME = ['armhpc']
    COMPILER_FAMILY = TC_CONSTANT_ARMHPC

    # Don't set COMPILER_FAMILY in this class because Clang does not have
    # Fortran support, and thus it is not a complete compiler as far as
    # EasyBuild is concerned.

    COMPILER_UNIQUE_OPTS = {
        'loop-vectorize': (False, "Loop vectorization"),
        'basic-block-vectorize': (False, "Basic block vectorization"),
    }
    COMPILER_UNIQUE_OPTION_MAP = {
        'unroll': 'funroll-loops',
        'loop-vectorize': ['fvectorize'],
        'basic-block-vectorize': ['fslp-vectorize'],
        # Clang's options do not map well onto these precision modes.  The flags enable and disable certain classes of
        # optimizations.
        # 
        # -fassociative-math: allow re-association of operands in series of floating-point operations, violates the
        # ISO C and C++ language standard by possibly changing computation result.
        # -freciprocal-math: allow optimizations to use the reciprocal of an argument rather than perform division.
        # -fsigned-zeros: do not allow optimizations to treat the sign of a zero argument or result as insignificant.
        # -fhonor-infinities: disallow optimizations to assume that arguments and results are not +/- Infs.
        # -fhonor-nans: disallow optimizations to assume that arguments and results are not +/- NaNs.
        # -ffinite-math-only: allow optimizations for floating-point arithmetic that assume that arguments and results
        # are not NaNs or +-Infs (equivalent to -fno-honor-nans -fno-honor-infinities)
        # -funsafe-math-optimizations: allow unsafe math optimizations (implies -fassociative-math, -fno-signed-zeros,
        # -freciprocal-math).
        # -ffast-math: an umbrella flag that enables all optimizations listed above, provides preprocessor macro
        # __FAST_MATH__.
        #
        # Using -fno-fast-math is equivalent to disabling all individual optimizations, see
        # http://llvm.org/viewvc/llvm-project/cfe/trunk/lib/Driver/Tools.cpp?view=markup (lines 2100 and following)
        #
        # 'strict', 'precise' and 'defaultprec' are all ISO C++ and IEEE complaint, but we explicitly specify details
        # flags for strict and precise for robustness against future changes.
        'strict': ['fno-fast-math'],
        'precise': ['fno-unsafe-math-optimizations'],
        'defaultprec': [],
        'loose': ['ffast-math', 'fsimdmath', 'fno-unsafe-math-optimizations'],
        'veryloose': ['ffast-math', 'fsimdmath'],
        'vectorize': {False: 'fno-vectorize', True: 'fvectorize'},
    }

    # used when 'optarch' toolchain option is enabled (and --optarch is not specified)
    COMPILER_OPTIMAL_ARCHITECTURE_OPTION = {
        (systemtools.AARCH64, systemtools.AARCH64): 'mcpu=native'
    }
    # used with --optarch=GENERIC
    COMPILER_GENERIC_OPTION = {
        (systemtools.AARCH64, systemtools.AARCH64): 'march=armv8-a -mtune=generic'
    }

    COMPILER_CC  = 'armclang'
    COMPILER_CXX = 'armclang++'
    COMPILER_C_UNIQUE_FLAGS = []

    COMPILER_F77 = 'armflang'
    COMPILER_F90 = 'armflang'
    COMPILER_FC  = 'armflang'

    LIB_MULTITHREAD = ['pthread']

    LIB_MATH = ['m']
    def _set_compiler_vars(self):
        """Set compiler variables."""
        super(ArmHPCcompiler, self)._set_compiler_vars()

        extra_libdirs=os.getenv("EBCUSTOM_EXTRA_LIB_DIRS")
        if None != extra_libdirs:
            extra_libdirs=extra_libdirs.split(':')
            for i in extra_libdirs:
                self.variables.append_subdirs("LDFLAGS", i)
        extra_libs=os.getenv("EBCUSTOM_EXTRA_LIBS")
        if None != extra_libs:
            extra_libs=extra_libs.split(',')
            for i in extra_libs:
                self.variables.append("LIBS", i)

        if self.options.get('32bit', None):
            raise EasyBuildError("_set_compiler_vars: 32bit set, but no support yet for 32bit Clang in EasyBuild")
