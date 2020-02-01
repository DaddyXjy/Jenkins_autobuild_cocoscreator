#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/30
#Author: dylan
#Desc: cocos 构建编译工具
from optparse import OptionParser
import jsonFileUtils
import os
import deleteUnusedMetaFile
import customerConfigUtils
import re
import subprocess
import time
import random
import sys

#COCOS引擎目录
enginePath = 'C:/CocosCreator'
#COCOS打包命令
COCOS_BUILD_CMD = 'CocosCreator.exe --path {0} --build \"{1}\"'
#COCOS编译命令
COCOS_COMPILE_CMD = 'CocosCreator.exe --path {0} --compile \"{1}\"'
#natve打包参数
BUILD_PARAM = 'platform=android;debug=false;appABIs=[\'armeabi-v7a\',\'x86\'];optimizeHotUpdate=true;inlineSpriteFrames=false;template=link;apiLevel=android-24;\
androidStudio=true;xxteaKey=e7fc65d6-aaf3-48;zipCompressJs=false;encryptJs=true;\
useDebugKeystore=false;keystorePassword=123456;keystoreAlias=key0;keystoreAliasPassword=123456'
#pc打包参数
BUILD_PARAM_PC = 'platform=web-desktop;debug=false;mergeStartScene=false;inlineSpriteFrames=true'
#h5打包参数
BUILD_PARAM_MOBILE = 'platform=web-mobile;debug=false;mergeStartScene=false;inlineSpriteFrames=true;webOrientation=landscape'
#签名文件路径
KEY_STORE_PATH = 'ly_build_tools/auto_build_customer/hhyxKey.jks'
#cocos BUILDER
COCOS_BUILDER_PATH = 'settings/builder.json'
#启动场景UUID
START_SCENE_UUID = 'b6c6405b-9200-46f4-a91e-dfb7922f4367'
ANDROID_BUILD_GRADLE = 'build/jsb-link/frameworks/runtime-src/proj.android-studio/app/build.gradle'
kCocosEngineCnt = 8
useCocosIndex = None


def getBuildCMD(workPath , buildParam):
    return COCOS_BUILD_CMD.format(workPath , buildParam)

def getCompileCMD(workPath , buildParam):
    return COCOS_COMPILE_CMD.format(workPath , buildParam)

def addBuildParam(buildParam , param):
    buildParam += ';' + param 
    return buildParam

#执行平台CMD命令
def excuteCmd(cmdStr):
    os.system(cmdStr)

def getNativeBuildParam(workPath , customerMark):
    buildParam = BUILD_PARAM
    customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
    buildParam = addBuildParam(buildParam, 'title=' + customerConfig['apkName'])
    keyStorePath = os.path.abspath(os.path.join(workPath ,   KEY_STORE_PATH))
    buildParam = addBuildParam(buildParam, 'keystorePath='+ keyStorePath)
    return buildParam

def updateBuilderFileStartScene():
    data = jsonFileUtils.getJsonDataFromFile(COCOS_BUILDER_PATH)
    data['startScene'] = START_SCENE_UUID
    jsonFileUtils.saveJsonDataToFile(COCOS_BUILDER_PATH , data)

def buildNative(workPath , customerMark = 'huihuang'):
    deleteUnusedMetaFile.run()
    os.system("echo " + 'start buildNative')
    buildParam = getNativeBuildParam(workPath , customerMark)
    cwd = os.getcwd()
    #切换到引擎目录打包
    #os.chdir(enginePath)
    #开始执行构建命令
    cmdBuild = getBuildCMD(workPath , buildParam)
    os.system("echo " + 'cmdBuild:' +cmdBuild)
    cocosRetryBuildCompile(cmdBuild)
    os.system("echo cocos native build complete.")
    #切回到工作目录
    os.chdir(cwd)

def compileNativeAndroid(workPath, customerMark = 'huihuang'):
    buildParam = getNativeBuildParam(workPath , customerMark)
    cmdCompile = getCompileCMD(workPath , buildParam)
    cwd = os.getcwd()
    #切换到引擎目录打包
    #os.chdir(enginePath)
    os.system("echo " + 'cmdCompile:' +cmdCompile)
    cocosRetryBuildCompile(cmdCompile)
    os.system("echo cocos native compile complete.")
    #切回到工作目录
    os.chdir(cwd)  

def buildH5(workPath):  
    deleteUnusedMetaFile.run()
    buildParam = BUILD_PARAM_MOBILE
    cwd = os.getcwd()
    #切换到引擎目录打包
    #os.chdir(enginePath)
    #开始执行构建命令
    cmdBuild = getBuildCMD(workPath , buildParam)
    os.system("echo " + 'cmdBuild:' + cmdBuild)
    cocosRetryBuildCompile(cmdBuild)
    os.system("echo cocos H5 build complete.")
    #切回到工作目录
    os.chdir(cwd)
#最容易失败的一步，build，compile，多次重试
def cocosRetryBuildCompile(cmd):
    buildStr = "build" if cmd.find("--build") != -1 else "compile"
    res = 1
    times = 0
    gradlePath = os.path.abspath(os.path.join(os.getcwd(), ANDROID_BUILD_GRADLE))
    productFile = ''
    debugString = "release"
    # if os.environ.get("PACKAGE_BRANCH") != None and os.environ["PACKAGE_BRANCH"].lower() != "online":
    #     cmd = re.sub(r'\bdebug=([^;]+)', 'debug=true', cmd)
    #     debugString = "debug"
    if buildStr == "compile":
        title = re.search(r'title=([^;]+)', cmd).group(1)
        productFile = "build/jsb-link/publish/android/" + title + "-{0}-signed.apk".format(debugString)
    else:
        platform = re.search(r'platform=([^;]+)', cmd).group(1)
        if platform == "web-mobile":
            strPlatform = "web-mobile"
        else:
            strPlatform = "jsb-link"
        productFile = "build/" + strPlatform + "/flagCompleted"
    productFile = os.path.abspath(os.path.join(os.getcwd(), productFile))
    if os.path.exists(productFile):
        os.remove(productFile)
    while (res != 0):
        enginePathTmp = enginePath
        if useCocosIndex != None:
            cocosIndex = useCocosIndex
        else:
            cocosIndex = random.randint(0, kCocosEngineCnt - 1)
        cocosIndex = cocosIndex + 8
        if cocosIndex != 0:
            enginePathTmp = enginePath + str(cocosIndex)
        if not os.path.exists(enginePathTmp):
            continue
        #修改gradle
        data = ''
        if buildStr == "compile":
            with open(gradlePath, 'r') as f:
                for line in f.readlines():
                    line = re.sub(r'C:/CocosCreator\d*', enginePathTmp, line)
                    data += line
                with open(gradlePath, 'w') as f:
                    f.writelines(data)
        os.chdir(enginePathTmp)
        #命令行执行
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            oriLine = p.stdout.readline()
            line = oriLine.replace("\r", "")
            line = line.replace("\n", "")
            if line != "":
                os.system("echo " + line + " useCocosIndex" + str(useCocosIndex))
            if (p.poll() != None and not oriLine) or line.find("no valid client ID") != -1 or line.find("Builder: do custom process [compile-finished]") != -1 or\
                re.search("Built to .* successfully", line) or line.find("at _combinedTickCallback") != -1 or line.find("Error: Compile failed.") != -1:
                break
            # if line.find("Error: Compile failed.") != -1:
            #     raise Exception('Compile failed.')
        os.system("echo subprocess is compelted useCocosIndex" + str(useCocosIndex))
        if p.poll() == None:
            p.kill()
            time.sleep(5)
        if line.find("Builder: do custom process [compile-finished]") != -1 or re.search("Built to .* successfully", line) or os.path.exists(productFile):
            if (productFile.find("flagCompleted") != -1) and os.path.exists(productFile):
                os.remove(productFile)
            res = 0
        else:
            times += 1
            os.system("echo cocos " + buildStr + " error times:" + str(times) + " useCocosIndex" + str(useCocosIndex))
            if times >= 10 and useCocosIndex == None:
                raise Exception(buildStr + ' error 20 times')
            os.system("echo " + buildStr + " again, please wait... useCocosIndex" + str(useCocosIndex))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-e' , '--enginePath' , dest = "enginePath" , default = 'C:/CocosCreator')
    parser.add_option('-w' , '--workPath' , dest = "workPath" , default = '../..')
    (option , args) = parser.parse_args()
    enginePath = option.enginePath
    workPath = option.workPath
    