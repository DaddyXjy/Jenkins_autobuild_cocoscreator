#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/30
#Author: dylan
#Desc: 版本控制工具

import subprocess
import os
import jsonFileUtils
import customerConfigUtils
import time

#构建大厅manifiset路径
BUILD_HALL_VERSION_MANIFEST = 'assets/version.manifest'
#构建大厅 prj manifiset路径
BUILD_HALL_PRJ_MANIFEST = 'assets/project.manifest'
#构建游戏manifiset路径
BUILD_GAME_VERSION_MANIFEST = 'assets/resources/Versions'
#热更新文件夹前缀
HOT_FOLDER_PREFIX = 'remote-assets2-'
#热更新大厅文件夹格式
HOT_HALL_FOLDER_FORMAT = '{0}/{1}{2}'
#热更新大厅文件夹格式
HOT_GAME_FOLDER_FORMAT = '{0}/SubGames/{1}{2}'
#热更新大厅version_mainfest地址格式
HOT_HALL_VERSION_MAINFEST_FORMAT = '{0}/{1}{2}/version.manifest'
#热更新大厅project_mainfest地址格式
HOT_HALL_PRJ_MAINFEST_FORMAT = '{0}/{1}{2}/project.manifest'
#热更新游戏version_mainfest地址格式
HOT_Game_VERSION_MAINFEST_FORMAT = '{0}/SubGames/{1}{2}/version.manifest'
#热更新游戏project_mainfest地址格式
HOT_Game_PRJ_MAINFEST_FORMAT = '{0}/SubGames/{1}{2}/project.manifest'
timeAutoVersion = None

def getHotUpdateUrl():
    return os.environ["hotUpdate"]

def getHotFolderFormat(isGame):
	if isGame:
		return HOT_GAME_FOLDER_FORMAT
	else:
		return HOT_HALL_FOLDER_FORMAT

def getVersionManifestFormat(isGame):
	if isGame:
		return HOT_Game_VERSION_MAINFEST_FORMAT
	else:
		return HOT_HALL_VERSION_MAINFEST_FORMAT

def getProjectManifestFormat(isGame):
	if isGame:
		return HOT_Game_PRJ_MAINFEST_FORMAT
	else:
		return HOT_HALL_PRJ_MAINFEST_FORMAT

def getDefaultVersion(bigVersion):
	version = str(bigVersion) + '.0.0'
	return version

def getGitCommitCount():
	# currentDir = os.getcwd()
	# os.chdir(os.environ['WORKSPACE'])
	# p = subprocess.Popen('git rev-list HEAD --first-parent --count' , stdout=subprocess.PIPE)
	# commitCount = p.stdout.read()
	# commitCount = commitCount.strip('\n')
	# os.system("echo git auto version:" + commitCount)
	# os.chdir(currentDir)
	global timeAutoVersion
	if timeAutoVersion == None:
		timeAutoVersion = str(2080 + int(time.time()) - 1561517763)
	os.system("echo git auto version:" + timeAutoVersion)
	return timeAutoVersion

def getHotVersion(bigVersion):
	version = getDefaultVersion(bigVersion)
	vList = str.split(version , '.') 
	vList[2] = getGitCommitCount()
	versionStr = '.'.join(vList)
	return versionStr

def updateVersionManifestFile(filePath , folder , version , isGame):
	data = jsonFileUtils.getJsonDataFromFile(filePath)
	url = getHotUpdateUrl()
	data['packageUrl'] = getHotFolderFormat(isGame).format(url , HOT_FOLDER_PREFIX , folder)
	data['remoteManifestUrl'] = getProjectManifestFormat(isGame).format(url , HOT_FOLDER_PREFIX , folder)
	data['remoteVersionUrl'] = getVersionManifestFormat(isGame).format(url , HOT_FOLDER_PREFIX , folder)
	data['version'] = version
	jsonFileUtils.saveJsonDataToFile(filePath , data)

def updateHallAllManifestFiles(customerMark , hallVersion):
	#修改大厅版本文件
	updateVersionManifestFile(BUILD_HALL_VERSION_MANIFEST ,customerMark , hallVersion ,False)
	if os.path.exists(BUILD_GAME_VERSION_MANIFEST):
		#修改游戏版本文件
		gameDefaultVersion = getGameDefaultVersion()
		for fileTemp in os.listdir(BUILD_GAME_VERSION_MANIFEST):
			filePath = os.path.join(BUILD_GAME_VERSION_MANIFEST , fileTemp)
			gameID = os.path.splitext(fileTemp)[0].split('_')[1]
			updateVersionManifestFile(filePath , gameID , gameDefaultVersion , True)	

def getCustomerCurrentVersion(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	bigVersion = customerConfig['bigVersion']
	return getHotVersion(bigVersion)

def getCustomerDefaultVersion(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	bigVersion = customerConfig['bigVersion']
	return getDefaultVersion(bigVersion)

def getGameDefaultVersion():	
	bigVersion = '1'
	return getDefaultVersion(bigVersion)

def getGameCurrentVersion():	
	bigVersion = '1'
	return getHotVersion(bigVersion)