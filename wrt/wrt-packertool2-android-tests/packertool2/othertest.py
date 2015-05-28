#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Hongjuan, Wang<hongjuanx.wang@intel.com>

import unittest
import os
import sys
import commands
import comm


class TestPackertoolsFunctions(unittest.TestCase):

    def test_packertool_arm_x86(self):
        comm.setUp()
        appRoot = comm.ConstPath + "/../testapp/example/"
        cmd = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --app-root=%s --app-local-path=index.html" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE, appRoot)
        comm.gen_pkg(cmd, self)

    def test_packertool_undefinedOption(self):
        comm.setUp()
        manifestPath = comm.ConstPath + "/../testapp/example/manifest.json"
        cmd = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --manifest=%s --undefinedOption=undefined" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE, manifestPath)
        # print cmd
        packstatus = commands.getstatusoutput(cmd)
        # print packstatus
        errorInfo = "no such option: --undefinedOption"
        self.assertIn(errorInfo, packstatus[1])

    def test_packertool_verbose(self):
        comm.setUp()
        appRoot = comm.ConstPath + "/../testapp/example/"
        cmd = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --app-root=%s --app-local-path=index.html" % \
              (comm.Pck_Tools, comm.ARCH, comm.MODE, appRoot)
        packstatus = commands.getstatusoutput(cmd)
        cmd_ver = "python %smake_apk.py --package=org.xwalk.example --name=example --arch=%s --mode=%s --app-root=%s --app-local-path=index.html --verbose" % \
            (comm.Pck_Tools, comm.ARCH, comm.MODE, appRoot)
        packstatus_ver = commands.getstatusoutput(cmd_ver)
        self.assertGreater(len(packstatus_ver[1]), len(packstatus[1]))

if __name__ == '__main__':
    unittest.main()
