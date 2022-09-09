##
# Copyright 2020-2022 Ghent University
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
EasyBuild support for building and installing PyTorch, implemented as an easyblock

@author: Alexander Grund (TU Dresden)
"""

import os
import re
import tempfile
from distutils.version import LooseVersion
from easybuild.easyblocks.pytorch import EB_PyTorch
from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.config import build_option
import easybuild.tools.environment as env
from easybuild.tools.modules import get_software_root, get_software_version
from easybuild.tools.systemtools import POWER, get_cpu_architecture
from easybuild.tools.filetools import symlink, apply_regex_substitutions


class EB_PyTorchCANN(EB_PyTorch):
    """Support for building/installing TensorFlow."""

    @staticmethod
    def extra_options():
        extra_vars = PythonPackage.extra_options()
        extra_vars.update({
            'excluded_tests': [{}, 'Mapping of architecture strings to list of tests to be excluded', CUSTOM],
            'custom_opts': [[], 'List of options for the build/install command. Can be used to change the defaults ' +
                                'set by the PyTorch EasyBlock, for example ["USE_MKLDNN=0"].', CUSTOM],
        })
        extra_vars['download_dep_fail'][0] = True
        extra_vars['sanity_pip_check'][0] = True

        return extra_vars

    def __init__(self, *args, **kwargs):
        super(EB_PyTorchCANN, self).__init__(*args, **kwargs)

    def fetch_step(self, skip_checksums=False):
        super(EB_PyTorchCANN, self).fetch_step(skip_checksums)

    def prepare_step(self, *args, **kwargs):
        super(EB_PyTorchCANN, self).prepare_step(*args, **kwargs)

    def configure_step(self):
        super(EB_PyTorchCANN, self).configure_step()

    def test_step(self):
        super(EB_PyTorchCANN, self).test_step()

    def test_cases_step(self):
        super(EB_PyTorchCANN, self).test_cases_step()

    def sanity_check_step(self, *args, **kwargs):
        super(EB_PyTorch, self).sanity_check_step(*args, **kwargs)

    def make_module_req_guess(self):
        return super(EB_PyTorch, self).make_module_req_guess()
