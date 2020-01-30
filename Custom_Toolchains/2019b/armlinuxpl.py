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
EasyBuild support for armlinuxpl compiler toolchain (includes ARM Compiler for Linux and ARM performance libraries).

"""

from easybuild.toolchains.armlinux import ArmLinux
from easybuild.toolchains.fft.armfft import ArmFFT
from easybuild.toolchains.linalg.armblas import ArmBLAS


class ArmLinuxPL(ArmLinux, ArmFFT, ArmBLAS):
    """Compiler toolchain with ARM compiler for Linux and ARM performance libraries."""
    NAME = 'armlinuxpl'
    SUBTOOLCHAIN = ArmLinux.NAME
