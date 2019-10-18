##
# Copyright 2012-2019 Ghent University
# Copyright 2019 Forschungszentrum Juelich
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
EasyBuild support for ARM compiler for HPC toolchain.

:author: Stepan Nassyr (Forschungszentrum Juelich)
"""

from easybuild.toolchains.compiler.armhpc import ArmHPCcompiler
from easybuild.tools.toolchain import DUMMY_TOOLCHAIN_NAME

TC_CONSTANT_ARMHPC = 'ArmHPC'

class ArmHPC(ArmHPCcompiler):
    """Compiler-only toolchain, including only ARM compiler for HPC."""
    NAME = 'armhpc'
    TOOLCHAIN_FAMILY = TC_CONSTANT_ARMHPC
    # Replace the default compiler module name with our own
    SUBTOOLCHAIN = DUMMY_TOOLCHAIN_NAME
    # GCCcore is only guaranteed to be present in recent toolchains
    # for old versions of some toolchains (GCC, intel) it is not part of the hierarchy and hence optional
    OPTIONAL = True
