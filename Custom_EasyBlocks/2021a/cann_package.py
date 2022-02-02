##
# This file is an EasyBuild reciPY as per https://github.com/easybuilders/easybuild
#
# Copyright:: Copyright 2022 Forschungszentrum Juelich GmbH
# Authors::   Stepan Nassyr
# License::   MIT/GPL
# $Id$
##
"""
EasyBuild support for Huawei CANN-related packages, implemented as an easyblock

@author: Stepan Nassyr (Forschungszentrum Juelich)
"""
import os
import stat
import platform
import grp

from distutils.version import LooseVersion

from easybuild.easyblocks.generic.binary import Binary
from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import apply_regex_substitutions,adjust_permissions,mkdir,symlink,remove_file
from easybuild.tools.run import run_cmd


class cann_package(Binary):
    """
    Support for installing CANN packages.
    """
    @staticmethod
    def extra_options():
        """Support for generic 'default' modules with specific real versions"""
        extra_vars = {
                'cann_installers': [None, "List of tuples: name, path to installation script (after extraction) and additional arguments for each package, i.e [(Ascend-acllib, acllib/scripts/install.sh, ''), ...]", CUSTOM],
                'subdir_symlinks': [None, "List of tuples: symlinks to create, alt_suf will be replaced, i.e ('opp','opp_linux.alt_suf') would create opp_linux.arm64 -> arm64-linux/opp on an aarch64 system", CUSTOM]
        }
        return extra_vars

    subinstallers = {}
    package_dirs = {}

    def fix_scripts(self, package_dir):
        # get all shell scripts in package directory
        scripts = []
        for root,dirs,files in os.walk(package_dir, topdown=False):
            for name in files:
                if name.endswith('.sh'):
                    scripts.append(os.path.join(root,name))

        subs = [
                (r'`cat /etc/passwd \| cut -f1 -d\':\' \| grep -w "(\$[^"]+)" -c`',r'$(getent passwd \1 | grep -w "\1" -c)'),
                (r'^(un|)chattrFiles\(\)\s*{',r'\1chattrFiles() {'+'\n'+'return'+'\n'+'}'+'\n'+r'\1chattrFiles_disabled() {'),
                (r'^(function\s*|)checkEmptyUserAndGroup\(\)\s*{',r'\1checkEmptyUserAndGroup() {'+'\n'+'return'+'\n'+'}'+'\n'+r'\1checkEmptyUserAndGroup_disabled() {'),
                (r'^checkInstallCondition\(\)\s*{',r'checkInstallCondition() {'+'\n'+'return'+'\n'+'}'+'\n'+r'checkInstallCondition_disabled() {'),
                ]
        apply_regex_substitutions(scripts, subs)

    def extract_step(self):
        """Extract main installer and any subpackages inside it, then fix the """


        cann_installers = self.cfg['cann_installers']
        main_installer = self.src[0]['path']


        (out,ret) = run_cmd("/bin/sh " + main_installer + " --noexec --extract=" + self.builddir)
        if 0 != ret:
            raise EasyBuildError("Main installer " + main_installer + " failed. output: " + out)
        
        # Gather the subinstallers
        subinst_dir = os.path.join(self.builddir,'run_package')
        for root,dirs,files in os.walk(subinst_dir, topdown=False):
            for name in files:
                if name.endswith('.run'):
                    for package in cann_installers:
                        package_name = package[0]
                        if name.startswith(package_name):
                            self.subinstallers[package_name] = os.path.join(root,name)
                            self.package_dirs[package_name] = (os.path.join(root,name.replace('.run','-unpacked')))


        # extract the subinstallers
        for package in cann_installers:
            package_name = package[0]
            (out,ret) = run_cmd("/bin/sh " + self.subinstallers[package_name] + " --noexec --extract=" + self.package_dirs[package_name])
            if 0 != ret:
                raise EasyBuildError("Subinstaller " + self.subinstallers[package_name] + " failed. output: " + out)
        
        for package in cann_installers:
            package_name = package[0]
            self.fix_scripts(self.package_dirs[package_name])

    def install_step(self):
        """ Run all subinstallers """

        hiai_group = os.getenv("HIAIGROUP","InvalidGroup")
        if "InvalidGroup" == hiai_group:
            raise EasyBuildError("Please specify the group for using Ascend devices in the HIAIGROUP environment variable")


        arch_suf = platform.machine()
        alt_suf = {
                'x86_64'  : 'x64',
                'aarch64' : 'arm64'
        }
        alt_suf = alt_suf[arch_suf]
        installdir_toolkit=os.path.join(self.installdir,'ascend-toolkit',self.version,alt_suf+'-linux')
        mkdir(installdir_toolkit,parents=True)

        cann_installers = self.cfg['cann_installers']
        parent_dir = os.getcwd()

        common_args = " --quiet --full --install-username=$USER --install-usergroup=" + hiai_group + " --install-path=" + installdir_toolkit + ' '

        for package in cann_installers:
            package_name   = package[0]
            installer_path = package[1]
            custom_args    = package[2]
            os.chdir(self.package_dirs[package_name])
            (out,ret) = run_cmd("/bin/sh " + installer_path + " --placeholder --placeholder " + custom_args + ' ' + common_args)
            if 0 != ret:
                raise EasyBuildError("Installing " + package_name + " failed: " + out)
            os.chdir(parent_dir)



    def post_install_step(self):
        """chmod + chown everything so it's usable and create symlinks"""

        hiai_group = os.getenv("HIAIGROUP","InvalidGroup")
        if "InvalidGroup" == hiai_group:
            raise EasyBuildError("Please specify the group for using Ascend devices in the HIAIGROUP environment variable")
        hiai_gid = grp.getgrnam(hiai_group).gr_gid
        adjust_permissions(self.installdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP, add=True, recursive=True, relative=True, onlydirs=True, group_id=hiai_gid)
        adjust_permissions(self.installdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP, add=True, recursive=True, relative=True, onlyfiles=True, group_id=hiai_gid)

        arch_suf = platform.machine()
        alt_suf = {
                'x86_64'  : 'x64',
                'aarch64' : 'arm64'
        }
        alt_suf = alt_suf[arch_suf]
        installdir_toolkit=os.path.join(self.installdir,'ascend-toolkit',self.version)

        prev_dir = os.getcwd()
        os.chdir(installdir_toolkit)
        subdir_symlinks = self.cfg['subdir_symlinks']
        for sl in subdir_symlinks:
            src = os.path.join(alt_suf+'-linux',sl[0])
            dst = sl[1].replace('alt_suf',alt_suf)
            if os.path.islink(dst):
                remove_file(dst)
            symlink(src,dst)
        os.chdir(prev_dir)

        super(cann_package, self).post_install_step()

