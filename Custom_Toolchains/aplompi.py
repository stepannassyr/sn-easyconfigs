##
# Copyright 2013-2018 Ghent University
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
EasyBuild support for aplompi compiler toolchain (includes ARM compiler for HPC, OpenMPI, ARM performance libraries and ScaLAPACK).

"""

from easybuild.toolchains.aompi import Aompi
from easybuild.toolchains.fft.armfft import ArmFFT
from easybuild.toolchains.linalg.armblas import ArmBLAS
from easybuild.toolchains.linalg.scalapack import ScaLAPACK


class Aplompi(Aompi, ArmFFT, ArmBLAS, ScaLAPACK):
    """Compiler toolchain with ARM compiler for HPC and OpenMPI."""
    NAME = 'aplompi'
    SUBTOOLCHAIN = Aompi.NAME
