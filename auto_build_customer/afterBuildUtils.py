#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/31
#Author: dylan
#Desc: 构建后完成的工作

import os
import shutil
from xml.dom import minidom
import codecs
import customerConfigUtils
import jsonFileUtils
import versionControlUtil
import genVersionFileUtils
import copyZip
import h5_redirect
import sys  
import re
reload(sys)  
sys.setdefaultencoding('utf8')

#打包资源目录
BUILD_NATIVE_ASSETS_PATH = "build/jsb-link"
#打包资源目录
BUILD_WEB_MOBILE_ASSETS_PATH = "build/web-mobile"

#安卓studio项目RES配置
ANDROID_RES_CONFIG = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/res'
#安卓studio项目SRC配置
ANDROID_SRC_CONFIG = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/src'
#客户配置文件目录
CUSTOMER_CONFIG_PATH = 'ly_build_tools/auto_build_customer/customer_config'
#安卓studio项目build.gradle配置
ANDROID_BUILD_GRADLE = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/build.gradle'
#安卓微信ACTIVITY
ANDROID_WX_ACTIVITY = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/src/wx/WXEntryActivity.java'
#安卓studio项目manifest
ANDROID_MANIFEST = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/AndroidManifest.xml'
#客户config目录
#NATIVE_CUSTOMER_CONFIG_PATH = 'res/raw-assets/CustomMade/customer_config.json'
#原生资源路径
NATIVE_RES_PATH = 'build/jsb-link/res/raw-assets'
#本地热更新文件夹目录
LOCAL_HOT_PATH = "ly_build_tools/auto_build_customer/HotUpdate"
mutiProcess = False

def getHotFolderName(isGame, flagName):
	if isGame:
		return LOCAL_HOT_PATH + "/SubGames/" + genVersionFileUtils.HOT_FOLDER_PREFIX + flagName
	else:
		return LOCAL_HOT_PATH + "/" + genVersionFileUtils.HOT_FOLDER_PREFIX + flagName
#拷贝APP图标
def copyAppIcon(customerMark):
    customerPath = os.path.join(CUSTOMER_CONFIG_PATH , customerMark)
    templateIconPath = os.path.join(os.path.join(customerPath, 'icon') , 'android')
    for dirTemp in os.listdir(ANDROID_RES_CONFIG):
        if dirTemp.find('mipmap') != -1:
            shutil.rmtree(os.path.join(ANDROID_RES_CONFIG ,dirTemp))
    for dirTemp in os.listdir(templateIconPath):
        shutil.copytree(os.path.join(templateIconPath ,dirTemp), os.path.join(ANDROID_RES_CONFIG ,dirTemp))

#设置微信SDK配置
def setWXScriptFolder(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	packageName = customerConfig['packageName']
	t = packageName.split('.')
	gap = '/'
	packagePath = gap.join(t)
	dstTree = os.path.join(os.path.join(ANDROID_SRC_CONFIG , packagePath) , 'wxapi')
	srcTree = os.path.join(ANDROID_SRC_CONFIG , 'wx')

	data = ''
	with open(ANDROID_WX_ACTIVITY, 'r') as f:
		for line in f.readlines():
			if(line.find('org.cocos2dx.javascript.wxapi') != -1):
				line = 'package ' + packageName + '.wxapi;\n'
			data += line
	with open(ANDROID_WX_ACTIVITY, 'w') as f:
		f.writelines(data)
	if os.path.exists(dstTree):
		shutil.rmtree(dstTree)
	shutil.copytree(srcTree , dstTree)
	shutil.rmtree(srcTree)

def setAndroidManifest(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	packageName = customerConfig['packageName']
	openinstallKey = customerConfig['openinstallKey']
	data = ''
	with open(ANDROID_MANIFEST, 'r') as f:
		for line in f.readlines():
			if(line.find('android:name=\"wx\"') != -1):
				line = '\t\t\tandroid:name=' + '\"' + packageName + '.wxapi.WXEntryActivity' + '\"\n'
			if(line.find('android:taskAffinity=\"wx\"') != -1):
				line = '\t\t\tandroid:taskAffinity=' + '\"' + packageName + '\"\n'
			if(line.find('<data android:scheme=\"openinstall\"') != -1):
				line = '\t\t\t\t<data android:scheme=' + '\"' + openinstallKey + '\"/>\n'
			if(line.find('<meta-data android:name=\"com.openinstall.APP_KEY\"') != -1):
				line = '\t\t<meta-data android:name=\"com.openinstall.APP_KEY\" android:value=\"' + openinstallKey + '\"/>\n'
			data += line
	with open(ANDROID_MANIFEST, 'w') as f:
		f.writelines(data)	

def setAppName(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	appName = customerConfig['appName']
	nameConfig = os.path.join(ANDROID_RES_CONFIG , 'values\\strings.xml')
	doc = minidom.parse(nameConfig)
	root = doc.documentElement
	target = root.getElementsByTagName("string")
	node = target[0].childNodes[0] 
	node.data = appName.encode('utf-8')
	f= open(nameConfig, 'w')
	writer = codecs.lookup('utf-8')[3](f)
	root.writexml(writer)
	writer.close()    

def setPackageName(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	packageName = customerConfig['packageName']
	data = ''
	with open(ANDROID_BUILD_GRADLE, 'r') as f:
			for line in f.readlines():
				if(line.find('applicationId') != -1):
					line = '\t\tapplicationId ' + '\"' + packageName + '\"\n'
				line = re.sub(r'(\s*GETUI_APP_ID\s*:\s*")[^"]*"', r'\g<1>' + customerConfig["GETUI_APP_ID"] + '"', line)
				line = re.sub(r'(\s*GETUI_APP_KEY\s*:\s*")[^"]*"', r'\g<1>' + customerConfig["GETUI_APP_KEY"] + '"', line)
				line = re.sub(r'(\s*GETUI_APP_SECRET\s*:\s*")[^"]*"', r'\g<1>' + customerConfig["GETUI_APP_SECRET"] + '"', line)
				data += line
	with open(ANDROID_BUILD_GRADLE, 'w') as f:
			f.writelines(data)

#移除其他客户的资源,2.0删除
# def deleteOtherCustomersAsset(customerMark):
# 	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
# 	tree = os.path.join(NATIVE_RES_PATH , 'CustomMade')
# 	for dirName in os.listdir(tree):
# 		realDir = os.path.join(tree , dirName)
# 		if os.path.isdir(realDir) and customerMark != dirName:
# 			if dirName != customerConfig['dependRes']:
# 				shutil.rmtree(realDir)

def copyMainJS(buildFolder):
	shutil.copy('ly_build_tools/auto_build_customer/main.js' , buildFolder +  '/main.js')

def copySplashScene():
	if not os.path.exists('SplashScene'):
		os.makedirs('SplashScene')
	shutil.copyfile('ly_build_tools/auto_build_customer/loading.js' , 'SplashScene/loading.js')
	dstTree = os.path.join( BUILD_NATIVE_ASSETS_PATH , 'res/SplashScene')
	if (os.path.exists(dstTree)):
		shutil.rmtree(dstTree)
	shutil.copytree('SplashScene' , dstTree)
def getAllCustomers():
	cList = []
	for sPath in os.listdir(CUSTOMER_CONFIG_PATH):
		realPath = os.path.join(CUSTOMER_CONFIG_PATH , sPath)
		if os.path.isdir(realPath):
			cList.append(sPath) 
	return cList

# def copyH5CustomerConfig():
#     	customerConfigPath = os.path.join(BUILD_WEB_MOBILE_ASSETS_PATH , NATIVE_CUSTOMER_CONFIG_PATH)
# 	config = {}
# 	for customer in getAllCustomers():
# 		config[customer] = customerConfigUtils.getConfigData(customer)
# 	jsonFileUtils.saveJsonDataToFile(customerConfigPath , config)

#def _deleteNativeApkAssets(customerMark):
	# tree1 = os.path.join(NATIVE_RES_PATH , 'Hall//Texture//Login')
	# tree2 = os.path.join(NATIVE_RES_PATH , 'Hall//Texture//NewMenuScene')
	# tree3 = os.path.join(NATIVE_RES_PATH , 'resources')
	# if os.path.exists(tree1):
	# 	shutil.rmtree(tree1)
	# if os.path.exists(tree2):
	# 	shutil.rmtree(tree2)
	# if os.path.exists(tree3):
	# 	shutil.rmtree(tree3)
    #移除其他客户的资源
	#deleteOtherCustomersAsset(customerMark)

def dealAndroidProject(customerMark):
	copyAppIcon(customerMark)
	setWXScriptFolder(customerMark)
	setAndroidManifest(customerMark)
	setAppName(customerMark)
	setPackageName(customerMark)

def dealNativeAssets(customerMark):
	copyMainJS(BUILD_NATIVE_ASSETS_PATH)
	if os.path.exists('build/jsb-link/res/logo'):
		shutil.rmtree('build/jsb-link/res/logo')
	#copyCustomerConfigFile(customerMark)
	#删除多余的资源
	#_deleteNativeApkAssets(customerMark)
	#修改版本文件
	# hallDefaultVersion = versionControlUtil.getCustomerDefaultVersion(customerMark)
	# versionControlUtil.updateHallAllManifestFiles(customerMark , hallDefaultVersion)
	#生成版本文件
	genVersionFileUtils.genNativeAppVersionFile(customerMark)
def genZipFolder(customerMark, isGame):
	#生成-zip文件夹
	folderName = getHotFolderName(False, customerMark)
	zipFolderName = folderName + "-zip"
	shutil.copyfile(folderName + "/project.manifest", folderName + "/project-tmp.manifest")
	if not os.path.exists(zipFolderName):
		os.mkdir(zipFolderName)
	cwd = os.getcwd()
	os.chdir(folderName)
	zipFolder = os.path.split(zipFolderName)[1]
	zipName = "../{0}/all.zip".format(zipFolder)
	WINRAR_PATH = os.environ['WINRAR_PATH']
	cmd = '"{1}" a -r {0}'.format(zipName, WINRAR_PATH)
	os.system(cmd)
	os.remove("project-tmp.manifest")
	cmd = '"{1}" d {0} project.manifest version.manifest'.format(zipName, WINRAR_PATH)
	os.system(cmd)
	#生成-zip的manifest文件
	os.chdir(cwd)
	url = versionControlUtil.getHotUpdateUrl()
	if isGame:
		hallCurrentVersion = versionControlUtil.getGameCurrentVersion()
		url = url + '/SubGames'
	else:
		hallCurrentVersion = versionControlUtil.getCustomerCurrentVersion(customerMark)
	os.chdir(LOCAL_HOT_PATH)
	cmd = 'node version_generator-zip.js -v {2} -u {1}/{3}{0}-zip/ -s {3}{0}-zip/ -d {3}{0}-zip/'.format(customerMark, url, hallCurrentVersion, versionControlUtil.HOT_FOLDER_PREFIX)
	os.system(cmd)
	os.chdir(cwd)
def dealHallHotAssets(customerMark):
	copyMainJS(BUILD_NATIVE_ASSETS_PATH)
	#copyCustomerConfigFile(customerMark)
	#修改版本文件
	# hallDefaultVersion = versionControlUtil.getCustomerDefaultVersion(customerMark)
	# versionControlUtil.updateHallAllManifestFiles(customerMark , hallDefaultVersion)
	genVersionFileUtils.genNativeHallHotFiles(customerMark)
	genZipFolder(customerMark, False)
	if not mutiProcess:
		copyZip.process(LOCAL_HOT_PATH , '../')
def dealGameHotAssets(gameID):
	copyMainJS(BUILD_NATIVE_ASSETS_PATH)
	copySplashScene()
	genVersionFileUtils.genNativeGameHotFiles(gameID)
	genZipFolder(gameID, True)
	genVersionFileUtils.redirectGameHotAssets(gameID)
	copyZip.process(LOCAL_HOT_PATH , './')
def dealHallH5Asset():
	copyMainJS(BUILD_WEB_MOBILE_ASSETS_PATH)
	#copyH5CustomerConfig()
	h5_redirect.run()
	copyZip.process(BUILD_WEB_MOBILE_ASSETS_PATH , '../')
def dealGameH5Asset(gameID):
	copyMainJS(BUILD_WEB_MOBILE_ASSETS_PATH)
	shutil.copytree('build/web-mobile/res/' , 'web-mobile/SubGames/'+ gameID +  '/res/')
	shutil.copytree('build/web-mobile/src/' , 'web-mobile/SubGames/'+ gameID +  '/src/')
	shutil.copy('build/web-mobile/main.js' , 'web-mobile/SubGames/'+ gameID +  '/main.js')
	copyZip.process('web-mobile' , './')