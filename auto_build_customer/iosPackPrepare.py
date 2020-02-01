#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import argparse
import shutil
CUSTOMER_MARK = None
def run(customerMark):
    global CUSTOMER_MARK
    CUSTOMER_MARK = customerMark
    cwd = os.getcwd()
    os.chdir("ly_build_tools/auto_build_customer")
    copyFile('../../build/jsb-link/src')
    copyFile('../../build/jsb-link/res')
    copyFile('../../build/jsb-link/main.js')
    os.chdir(cwd)

def copyFile(src, dst=None):
    path = dst or os.path.join("~", 'tmpProjs', os.environ["PACKAGE_BRANCH"], CUSTOMER_MARK, 'huihuang', 'frameworks/runtime-src/proj.ios_mac/')
    src = os.path.abspath(src)
    src = src.replace("\\", "/")
    src = src.replace(":/", "/")
    src = "/cygdrive/" + src
    path = path.replace("\\", "/")
    os.system("rsync -e 'ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete " + src + " leying@leyingdeMacBook-Pro:" + path)