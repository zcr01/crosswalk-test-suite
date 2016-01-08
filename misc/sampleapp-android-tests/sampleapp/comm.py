#!/usr/bin/env python
# coding=utf-8
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
#         Cici,Li<cici.x.li@intel.com>

import unittest
import os
import sys
import commands
import shutil
import glob
reload(sys)
sys.setdefaultencoding("utf-8")

script_path = os.path.realpath(__file__)
const_path = os.path.dirname(script_path)
sample_src_pref = "/tmp/crosswalk-samples/"
app_tools_dir = os.environ.get('CROSSWALK_APP_TOOLS_CACHE_DIR')
index_path = "index.html"


def setUp():
    global xwalk_version, ARCH, MODE, device, apptools, crosswalkzip

    xwalk_version = os.environ.get('XWALK_VERSION')
    device = os.environ.get('DEVICE_ID')

    if not device:
        print (" get device id error\n")
        sys.exit(1)

    if not app_tools_dir:
        print ("Not find CROSSWALK_APP_TOOLS_CACHE_DIR\n")
        sys.exit(1)

    fp = open(const_path + "/../arch.txt", 'r')
    ARCH = fp.read().strip("\n\t")
    fp.close()

    mode = open(const_path + "/../mode.txt", 'r')
    MODE = mode.read().strip("\n\t")
    mode.close()

    # app tools commend
    apptools = "crosswalk-pkg"
    if os.system(apptools) != 0:
        apptools = app_tools_dir + "/crosswalk-app-tools/src/crosswalk-pkg"

    # crosswalk lib
    if not xwalk_version:
        zips = glob.glob(os.path.join(app_tools_dir, "crosswalk-*.zip"))
        if len(zips) == 0:
            print ("Not find crosswalk zip in CROSSWALK_APP_TOOLS_CACHE_DIR\n")
            sys.exit(1)
        # latest version
        zips.sort(reverse = True)
        crosswalkzip = zips[0]
    else:
        if "64" in ARCH:
            crosswalkzip = os.path.join(app_tools_dir, "crosswalk-%s-64bit.zip" % xwalk_version)
        else:
            crosswalkzip = os.path.join(app_tools_dir, "crosswalk-%s.zip" % xwalk_version)
        if not os.path.exists(crosswalkzip):
            crosswalkzip = xwalk_version

def check_appname():
    global app_name
    xwalk_version = os.environ.get('XWALK_VERSION')
    #xwalk_version = '8.38.208.0'
    if int(xwalk_version.split('.')[0]) < 9:
        app_name = 'xwalk_echo_app'
    else:
        app_name = 'Sample'


def pack(cmd, appname, self):
    setUp()
    pack_path = const_path + "/../testapp/"
    os.chdir(pack_path)
    print "Generate APK %s ----------------> START" % appname
    print cmd
    packstatus = commands.getstatusoutput(cmd)
    self.assertEquals(0, packstatus[0])
    print "\nGenerate APK %s ----------------> OK\n" % appname
    result = commands.getstatusoutput("ls")
    self.assertIn(appname, result[1])
    os.chdir("../..")


def app_install(cmd, cmdfind, self):
    print "Install APK ----------------> START"
    inststatus = commands.getstatusoutput(cmd)
    self.assertEquals(0, inststatus[0])
    print "Install APK ----------------> OK"
    pmstatus = commands.getstatusoutput(cmdfind)
    self.assertEquals(0, pmstatus[0])
    print "Find Package in device ----------------> OK"


def app_launch(cmd, self):
    print "Launch APK ----------------> START"
    launchstatus = commands.getstatusoutput(cmd)
    self.assertNotIn("error", launchstatus[1].lower())
    print "Launch APK ----------------> OK"


def app_stop(cmd, self):
    print "Stop APK ----------------> START"
    stopstatus = commands.getstatusoutput(cmd)
    self.assertEquals(0, stopstatus[0])
    print "Stop APK ----------------> OK"


def app_uninstall(cmd, self):
    print "Uninstall APK ----------------> START"
    unistatus = commands.getstatusoutput(cmd)
    self.assertEquals(0, unistatus[0])
    print "Uninstall APK ----------------> OK"

