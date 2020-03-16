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
Support for ARM Performance Libraries as FFT library.

:author: Stepan Nassyr (Forschungszentrum Juelich)
"""

import os
from easybuild.toolchains.fft.fftw import Fftw
from easybuild.tools.modules import get_software_version


TC_CONSTANT_ARMPL = 'ARMPL'


class ArmFFT(Fftw):
    """
    Provide support for ARMPL as FFT library
    """
    FFT_MODULE_NAME = ['ArmFFT']
    FFT_LIB         = ['armpl']
    FFT_FAMILY      = TC_CONSTANT_ARMPL

    def _set_fftw_variables(self):
        self.FFT_LIB_MT = self.FFT_LIB
