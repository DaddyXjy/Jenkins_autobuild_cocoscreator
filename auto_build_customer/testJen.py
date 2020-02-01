#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/02/01
#Author: dylan
#Desc: 自动构建入口

from optparse import OptionParser  
import beforeBuildUtils
import afterBuildUtils
import cocosBuildUtils
import customerConfigUtils
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

customerMark = ''
gameID = ''
workSpace = ''
def buildApk():
    os.system("echo start buildApk")
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForPackage()
    cocosBuildUtils.updateBuilderFileStartScene()
    cocosBuildUtils.buildNative(workSpace, customerMark)
    afterBuildUtils.dealAndroidProject(customerMark)
    afterBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.compileNativeAndroid(workSpace , customerMark)

def buildHallHot():
    os.system("echo start buildHallHot")
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForHotHall()
    cocosBuildUtils.updateBuilderFileStartScene()
    cocosBuildUtils.buildNative(workSpace , customerMark)
    afterBuildUtils.dealHallHotAssets(customerMark)
def buildGameHot():
    os.system("echo start buildGameHot")
    beforeBuildUtils.deleteAssetsForHotGame()
    cocosBuildUtils.buildNative(workSpace)
    afterBuildUtils.dealGameHotAssets(gameID)

def buildHallH5():
    os.system("echo start buildHallH5")
    cocosBuildUtils.buildH5(workSpace)
    afterBuildUtils.dealHallH5Asset()

def buildGameH5():
    os.system("echo start buildGameH5")
    cocosBuildUtils.buildH5(workSpace)
    afterBuildUtils.dealGameH5Asset(gameID)
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t' , '--buildType' , dest = "buildType")
    parser.add_option('-c' , '--customerMark' , dest = "customerMark")
    parser.add_option('-g' , '--gameID' , dest = "gameID")
    (option , args) = parser.parse_args()
    buildType = option.buildType    
    customerMark = option.customerMark    
    gameID = option.gameID
    workSpace = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    #切换到工作目录
    os.chdir(workSpace)
    os.system("echo " + ("buildType = {0}".format(buildType)))
    if buildType == 'apk':
        buildApk()
    elif buildType == 'hallHot':
        buildHallHot()
    elif buildType == 'hotGame':
        buildGameHot()
    elif buildType == 'hallH5':
        buildHallH5()
    elif buildType == 'gameH5':
        buildGameH5()