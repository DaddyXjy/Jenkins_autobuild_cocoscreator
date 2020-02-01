#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/31
#Author: dylan
#Desc: 构建前完成的工作

import os
import shutil
import customerConfigUtils
import jsonFileUtils
import versionControlUtil
import afterBuildUtils
WORKSPACE_ASSETS = 'assets'
#移除其他客户的资源
def deleteOtherCustomersAsset(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	tree = os.path.join(WORKSPACE_ASSETS, 'CustomMade')
	for dirName in os.listdir(tree):
		realDir = os.path.join(tree , dirName)
		if os.path.isdir(realDir) and customerMark != dirName:
			if dirName != customerConfig['dependRes']:
				shutil.rmtree(realDir)

def deleteNativeApkAssets(customerMark):
	tree1 = os.path.join(WORKSPACE_ASSETS, 'Hall/Texture/Login')
	tree2 = os.path.join(WORKSPACE_ASSETS, 'Hall/Texture/NewMenuScene')
	tree3 = os.path.join(WORKSPACE_ASSETS, 'resources')
	if os.path.exists(tree1):
		shutil.rmtree(tree1)
	if os.path.exists(tree2):
		shutil.rmtree(tree2)
	if os.path.exists(tree3):
		shutil.rmtree(tree3)
    #移除其他客户的资源
	deleteOtherCustomersAsset(customerMark)

def deleteWorkSpaceOtherCustomerAssets(customerMark):
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	tree = os.path.join(WORKSPACE_ASSETS , 'CustomMade')
	for dirName in os.listdir(tree):
		realDir = os.path.join(tree , dirName)
		if os.path.isdir(realDir) and customerMark != dirName:
			if dirName != customerConfig['dependRes']:
				shutil.rmtree(realDir)	

	tree2 = os.path.join(WORKSPACE_ASSETS , 'resources/CustomMade')
	if os.path.exists(tree2):
		for dirName in os.listdir(tree2):
			realDir = os.path.join(tree2 , dirName)
			if os.path.isdir(realDir) and customerMark != dirName:
				if dirName != customerConfig['dependRes']:
					shutil.rmtree(realDir)	

def _deleteAssets(assetsPath):
	if os.path.exists(assetsPath):
		shutil.rmtree(assetsPath)
#热更新游戏的时候删除资源
def deleteAssetsForHotGame():
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'resources/CommonDynamicAssets/Texture/LoadingLayerSecond'))
#打包APP时候删除资源
def deleteAssetsForPackage():
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'resources/CustomMade'))
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'resources/CommonDynamicAssets/Texture/CirCleHead'))
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'resources/CommonDynamicAssets/Texture/Head'))
	deleteAssetsForHotHall()
#热更新时候删除大厅资源
def deleteAssetsForHotHall(): 
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'resources/CommonDynamicAssets/Texture/LoadingLayerSecond'))
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'CommonStaticAssets/Texture/GameCommon'))
	_deleteAssets(os.path.join(WORKSPACE_ASSETS, 'CommonStaticAssets/Texture/Prefabs/GameUse'))
#2.0版本部分处理必须放到编译前去做，都放在这里了
def copyCustomerConfigFile(customerMark):
	customerConfigPath = 'assets/CustomMade/customer_config.json'
	customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
	jsonFileUtils.saveJsonDataToFile(customerConfigPath , customerConfig)

def dealNativeAssets(customerMark):
	copyCustomerConfigFile(customerMark)
	hallDefaultVersion = versionControlUtil.getCustomerDefaultVersion(customerMark)
	versionControlUtil.updateHallAllManifestFiles(customerMark, hallDefaultVersion)
def dealHallHotAssets(customerMark):
	copyCustomerConfigFile(customerMark)
	hallDefaultVersion = versionControlUtil.getCustomerDefaultVersion(customerMark)
	versionControlUtil.updateHallAllManifestFiles(customerMark , hallDefaultVersion)

def dealHallH5Asset():
    copyH5CustomerConfig()

def dealGameHotAssets(gameID):
	pass

def copyH5CustomerConfig():
	customerConfigPath = 'assets/CustomMade/customer_config.json'
	config = {}
	for customer in afterBuildUtils.getAllCustomers():
		config[customer] = customerConfigUtils.getConfigData(customer)
	jsonFileUtils.saveJsonDataToFile(customerConfigPath , config)