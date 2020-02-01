#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/31
#Author: dylan
#Desc: 客户配置文件工具
import os
import jsonFileUtils

#客户配置文件目录
CUSTOMER_CONFIG_PATH = 'ly_build_tools/auto_build_customer/customer_config'

def getConfigData(customerMark):
	configPath = os.path.join(CUSTOMER_CONFIG_PATH , customerMark , 'config.json')
	info = jsonFileUtils.getJsonDataFromFile(configPath)
	return info

def getCustomerConfig(customerMark):
	customerConfig = None
	try:
		customerConfig = getConfigData(customerMark)
		branchKey = '_' + os.environ["PACKAGE_BRANCH"].upper()
		customerConfig['HTTP_BASE_URL'] = customerConfig["HTTP_BASE_URL" + branchKey]
		customerConfig['WEBSOCKET_BASE_URL'] = customerConfig["WEBSOCKET_BASE_URL" + branchKey]
		customerConfig['openinstallKey'] = customerConfig["openinstallKey" + branchKey]
		customerConfig['DOWNLOAD_URL'] = customerConfig["DOWNLOAD_URL"+ branchKey]
		customerConfig['bigVersion'] = customerConfig["bigVersion"+ branchKey]
		customerConfig['stationMark'] = customerConfig["stationMark"+ branchKey]
		customerConfig['wechatID'] = customerConfig["wechatID"+ branchKey]
		customerConfig['packageName'] = customerConfig["packageName"] + '_' +  os.environ["PACKAGE_BRANCH"]
		customerConfig['apkName'] = customerMark + '_' +  os.environ["PACKAGE_BRANCH"]
		appNameFix = ''
		if os.environ["PACKAGE_BRANCH"] != 'online':
			appNameFix =  '_' + os.environ["PACKAGE_BRANCH"]
			customerConfig["appName"] = customerConfig["appName"] + appNameFix
		#服务器地址从jenkins获取,如果jenkins没有获取到,那么就用站点自己的
		if os.environ.has_key('HTTP_BASE_URL'):
			customerConfig['HTTP_BASE_URL'] = os.environ["HTTP_BASE_URL"]
		if os.environ.has_key('WEBSOCKET_BASE_URL'):
			customerConfig['WEBSOCKET_BASE_URL'] = os.environ["WEBSOCKET_BASE_URL"]
		if not customerConfig.has_key('GETUI_APP_ID'):
			customerConfig['GETUI_APP_ID'] = ''
		if not customerConfig.has_key('GETUI_APP_KEY'):
			customerConfig['GETUI_APP_KEY'] = ''
		if not customerConfig.has_key('GETUI_APP_SECRET'):
			customerConfig['GETUI_APP_SECRET'] = ''
		customerConfig["packageBranch"] = os.environ["PACKAGE_BRANCH"].lower()
	except Exception:
		raise Exception('error when get getCustomerConfig from:' + customerMark)
	return customerConfig
