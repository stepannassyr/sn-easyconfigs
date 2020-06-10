############################################
# Copyright 2020 Forschungszentrum Juelich #
############################################
"""
EasyBlock for building gem5

@author: Stepan Nassyr (Forschungszentrum Juelich - Juelich Supercomputing Center (JSC))
"""
from easybuild.framework.easyblock import EasyBlock
from easybuild.framework.easyconfig import MANDATORY
from easybuild.tools.run import run_cmd


class gem5(EasyBlock):

    @staticmethod
    def extra_options():
        extra_vars = {
            'gem5_isa': ['X86', "Target Instruction Set Architecture (ISA)", MANDATORY],
        }
        return EasyBlock.extra_options(extra_vars)

    def configure_step(self):
        pass

    def build_step(self, verbose=False):
        par = ''
        if self.cfg['parallel']:
            par = "-j %s" % self.cfg['parallel']

        cmd = "%(prebuildopts)s scons build/%(gem5_isa)s/gem5.opt %(par)s %(buildopts)s" % {
            'buildopts': self.cfg['buildopts'],
            'gem5_isa': self.cfg['gem5_isa'],
            'prebuildopts': self.cfg['prebuildopts'],
            'par': par,
        }
        (out, _) = run_cmd(cmd, log_all=True, log_output=verbose)

        return out

    def test_step(self):
        pass

    def install_step(self):
        cmd = "mkdir -p %(installdir)s/bin; cp build/%(gem5_isa)s/gem5.opt %(installdir)s/bin/" % {
            'installdir': self.installdir,
            'gem5_isa': self.cfg['gem5_isa'],
        }
        (out, _) = run_cmd(cmd, log_all=True)

        return out
