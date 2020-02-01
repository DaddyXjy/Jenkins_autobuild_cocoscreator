#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/10/27
#Author: dylan
#Desc: 拷贝ipa到指定目录
#暂时废弃，直接从苹果打包机上iosPack.py拷贝到HFS
import io
import os
import sys
import datetime
def processPath(path):
	path = path.replace("\\", "/")
	path = path.replace(":/", "/")
	path = "/cygdrive/" + path
	return path

# os.environ['CUSTOMER_MARK'] = "boke001"
# os.environ['PACKAGE_BRANCH'] = "yfb"
# os.environ['BUILD_NUMBER'] = "15"
REMOTE_PATH = sys.argv[1]
channel = os.environ['CUSTOMER_MARK']
env = os.environ['PACKAGE_BRANCH']
buildNumber = os.environ['BUILD_NUMBER']
time = datetime.datetime.today()
ipaPath = os.path.join('/Users/leying/out', env, str(time.year) + '_' + str(time.month) + '_' + str(time.day),
	channel, buildNumber, env + '_' + channel + '.ipa')
httpPath = os.path.join(REMOTE_PATH, env)
ipaPath = ipaPath.replace("\\", "/")
httpPath = processPath(httpPath)
os.system('rsync -e "ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no" -r -t --delete leying@leyingdeMacBook-Pro:' + ipaPath
	+ ' ' + httpPath)