#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/2/1
#Author: dylan
#Desc: version文件生成工具

import shutil
import os
import versionControlUtil
import customerConfigUtils
#热更新文件夹前缀
HOT_FOLDER_PREFIX = versionControlUtil.HOT_FOLDER_PREFIX
#本地热更新文件夹目录
LOCAL_HOT_PATH = "ly_build_tools/auto_build_customer/HotUpdate"
#热更新文件夹格式
HOT_FOLDER_FORMAT = '{0}/{1}{2}'
#打包资源目录
BUILD_RES_ASSETS_PATH = "build/jsb-link/res"
#打包脚本目录
BUILD_SRC_ASSETS_PATH = "build/jsb-link/src"    
#打包资源目录
BUILD_ASSETS_PATH = "build/jsb-link"
#自动构建脚本所在目录
AUTO_BUILD_PATH = "ly_build_tools/auto_build_customer"
#node命令
NODE_CMD_FORMAT = 'node version_generator.js -v {2} -u {1}/{3}{0}/ -s {3}{0}/ -d {3}{0}/'
def processPath(path):
    path = path.replace("\\", "/")
    if path.find(":/") != -1:
        path = path.replace(":/", "/")
        path = "/cygdrive/" + path
    return path
def copyAssetsToWorkSpace(folder):
    hotFolder = HOT_FOLDER_FORMAT.format(LOCAL_HOT_PATH , HOT_FOLDER_PREFIX , folder)
    hotResFolder = os.path.join(hotFolder , 'res')
    hotSrcFolder = os.path.join(hotFolder , 'src')
    if os.path.exists(hotResFolder):
        shutil.rmtree(hotResFolder)
    if os.path.exists(hotSrcFolder):
        shutil.rmtree(hotSrcFolder)
    if not os.path.exists(hotFolder):
        os.mkdir(hotFolder)
    os.system("rsync -r -t --chmod=777 " + processPath(BUILD_RES_ASSETS_PATH) + "/ " + processPath(hotResFolder))
    os.system("rsync -r -t --chmod=777 " + processPath(BUILD_SRC_ASSETS_PATH) + "/ " + processPath(hotSrcFolder))
    # shutil.move(BUILD_RES_ASSETS_PATH, hotFolder)
    # shutil.move(BUILD_SRC_ASSETS_PATH, hotFolder)
    shutil.copy(os.path.join(BUILD_ASSETS_PATH , 'main.js') , os.path.join(hotFolder , 'main.js'))

def getHotFolderPath(hotFolder):
    hotFolderPath = HOT_FOLDER_FORMAT.format(LOCAL_HOT_PATH , HOT_FOLDER_PREFIX , hotFolder)
    return hotFolderPath

# def removeOtherCustomerAssets(customerMark):
#     #移除其他客户的资源
#     hotFolderPath =  getHotFolderPath(customerMark)
#     hotRawResFolder = os.path.join(hotFolderPath , 'res/raw-assets')
#     customerMadeDir = os.path.join(hotRawResFolder , 'CustomMade')
#     customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
#     for dirName in os.listdir(customerMadeDir):
#         realDir = os.path.join(customerMadeDir , dirName)
#         if os.path.isdir(realDir) and customerMark != dirName:
#             if dirName != customerConfig['dependRes']:
#                 shutil.rmtree(realDir)    

def genVersionFiles(folder, version ,isGame):
    cwd = os.getcwd()
    nodeScriptDir = os.path.join(AUTO_BUILD_PATH , 'HotUpdate')
    os.chdir(nodeScriptDir)
    url = versionControlUtil.getHotUpdateUrl()
    if isGame:
      url = url + '/SubGames'
    cmd = NODE_CMD_FORMAT.format(folder , url , version, HOT_FOLDER_PREFIX)
    os.system(cmd)
    os.chdir(cwd)

def copyVersionFileToBuildSpace(hotFolder):
    buildRawAssetsPath = os.path.join(BUILD_ASSETS_PATH , 'res/raw-assets')
    hotFolderPath = getHotFolderPath(hotFolder)
    shutil.copy(os.path.join(hotFolderPath , 'version.manifest') , os.path.join(buildRawAssetsPath , 'version.manifest'))
    shutil.copy(os.path.join(hotFolderPath , 'project.manifest') , os.path.join(buildRawAssetsPath , 'project.manifest'))

def redirectGameHotAssets(gameID):
    hotFolder = getHotFolderPath(gameID)
    gameFolder = HOT_FOLDER_PREFIX + str(gameID)
    subGameFolder = os.path.join(LOCAL_HOT_PATH , 'SubGames')
    shutil.move(hotFolder, os.path.join(subGameFolder , gameFolder))
    shutil.move(hotFolder + "-zip", os.path.join(subGameFolder , gameFolder + "-zip"))

def genNativeAppVersionFile(customerMark):
    copyAssetsToWorkSpace(customerMark)
    hallDefaultversion = versionControlUtil.getCustomerDefaultVersion(customerMark)
    genVersionFiles(customerMark , hallDefaultversion , False)
    copyVersionFileToBuildSpace(customerMark)
#效率更高的一个版本，暂时没用到
# def genNativeAppVersionFile2(customerMark):
#     shutil.copy(os.path.join(LOCAL_HOT_PATH , 'version_generator.js'), BUILD_ASSETS_PATH)
#     url = versionControlUtil.getHotUpdateUrl()
#     version = versionControlUtil.getCustomerDefaultVersion(customerMark)
#     cwd = os.getcwd()
#     os.chdir(BUILD_ASSETS_PATH)
#     cmd = 'node version_generator.js -v {2} -u {1}/{3}{0}/ -s ./ -d ./'.format(customerMark , url , version, HOT_FOLDER_PREFIX)
#     os.system(cmd)
#     os.remove('version_generator.js')
#     shutil.move("project.manifest", "res/raw-assets")
#     shutil.move("version.manifest", "res/raw-assets")
#     os.chdir(cwd)

def genNativeHallHotFiles(customerMark):
    copyAssetsToWorkSpace(customerMark)
    #removeOtherCustomerAssets(customerMark)
    hallCurrentVersion = versionControlUtil.getCustomerCurrentVersion(customerMark)
    genVersionFiles(customerMark , hallCurrentVersion , False)

def genNativeGameHotFiles(gameID):
    copyAssetsToWorkSpace(gameID)
    hallCurrentVersion = versionControlUtil.getGameCurrentVersion()
    genVersionFiles(gameID , hallCurrentVersion , True)