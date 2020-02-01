#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import argparse
import shutil

def run():
    cwd = os.getcwd()
    os.chdir("ly_build_tools/auto_build_customer")
    path = '~/packConfig'
    path = path.replace("\\", "/")
    #把本地的资源覆盖上去
    os.system("rsync -e 'ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete ../ios/ leying@leyingdeMacBook-Pro:" + path)
    os.system("rsync -e 'ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete ../auto_build_customer/customer_config leying@leyingdeMacBook-Pro:" + path)
    os.system("rsync -e 'ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete ../auto_build_customer/customerConfigUtils.py leying@leyingdeMacBook-Pro:" + path + "/scripts/")
    os.system("rsync -e 'ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no' -r -t --delete ../auto_build_customer/jsonFileUtils.py leying@leyingdeMacBook-Pro:" + path + "/scripts/")
    os.chdir(cwd)