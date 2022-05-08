##
# Copyright 2013-2019 Ghent University
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
Support for ARM compiler for HPC as toolchain linear algebra library.

:author: Stepan Nassyr (Forschungszentrum Juelich)
"""

from easybuild.tools.toolchain.linalg import LinAlg


TC_CONSTANT_ARMPL = 'ARMPL'


class ArmBLAS(LinAlg):
    """
    Provide support for ARMPL as BLAS and LAPACK library
    """
    BLAS_MODULE_NAME   = ['ArmBLAS']
    BLAS_LIB           = ['armpl']
    BLAS_FAMILY        = TC_CONSTANT_ARMPL
    LAPACK_MODULE_NAME = ['ArmBLAS']
    LAPACK_LIB         = ['armpl']
    LAPACK_FAMILY      = TC_CONSTANT_ARMPL
