#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/10/27
#Author: dylan
#Desc: 拷贝APK到指定目录
import io
import os
import json
import shutil
import sys
#import qrcode
def processPath(path):
	path = path.replace("\\", "/")
	path = path.replace(":/", "/")
	path = "/cygdrive/" + path
	return path
def run(REMOTE_PATH, customerMark):
	branch = os.environ["PACKAGE_BRANCH"]
	ANDROID_PATH = os.path.join(os.getcwd() , 'build/jsb-link/publish/android')
	cwd = os.getcwd()
	os.chdir(ANDROID_PATH)
	appPreFixName = customerMark
	appPreFixName = customerMark+'_' + branch
	apkName = appPreFixName + '-release-signed.apk'
	#开始拷贝APK
	remoteApkPath = os.path.join(REMOTE_PATH, "v2_" + apkName)
	if not os.path.exists("F:/http_server"):
		remoteApkPath = "leying@172.20.100.100:" + remoteApkPath
		os.system('scp ' + apkName + ' ' + remoteApkPath)
	else:
		remoteApkPath = processPath(remoteApkPath)
		os.system('rsync -e "ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no" -r -t --delete ' + apkName + ' ' + remoteApkPath)
	os.system("echo " + 'copy apk to:' + remoteApkPath + ' success!')
	os.chdir(cwd)
#开始生产二维码
# os.chdir(REMOTE_PATH)
# makeUrl = HTTP_APK_PATH +apkName 
# #img = qrcode.make(makeUrl)
# #img.save( appPreFixName + ".png")
# os.system("echo " + '[qrcodeUrl] ' + '<img src= ' + HTTP_APK_PATH + appPreFixName + ".png" + ' height=\"200\" width=\"200\" />')
# os.system("echo " + '[buildName] ' + appPreFixName)
# os.system("echo " + 'qrcode build success')