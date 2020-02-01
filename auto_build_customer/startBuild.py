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
import threading
import multiprocessing
import shutil
import copyZip
import re
import apkCopy
import iosCopyTools
import iosPackPrepare
import versionControlUtil
import urllib
import zipfile
import json
reload(sys)
sys.setdefaultencoding('utf8')
kUsePool = False
kProcessCnt = 6
gameID = ''
workSpace = ''
deleteUnuseAssetsPath = ''
customerMark = ''
def buildTest():
    cocosBuildUtils.buildNative(workSpace, customerMark)

def buildiOS():
    os.system("echo " + 'start buildiOS')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForPackage()
    beforeBuildUtils.deleteNativeApkAssets(customerMark)
    cocosBuildUtils.updateBuilderFileStartScene()
    os.system(deleteUnuseAssetsPath + " " + workSpace + " " + customerMark)
    beforeBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace, customerMark)
    afterBuildUtils.dealNativeAssets(customerMark)
    iosCopyTools.run()
    iosPackPrepare.run(customerMark)

def buildApk():
    os.system("echo " + 'start buildApk')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForPackage()
    beforeBuildUtils.deleteNativeApkAssets(customerMark)
    cocosBuildUtils.updateBuilderFileStartScene()
    os.system(deleteUnuseAssetsPath + " " + workSpace + " " + customerMark)
    beforeBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace, customerMark)
    afterBuildUtils.dealAndroidProject(customerMark)
    afterBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.compileNativeAndroid(workSpace , customerMark)
    apkCopy.run("F:/http_server/apk/sepreate_" + os.environ["PACKAGE_BRANCH"].lower(), customerMark)

def buildiOSWithHall():
    os.system("echo " + 'start buildiOSWithHall')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForHotHall()
    cocosBuildUtils.updateBuilderFileStartScene()
    os.system(deleteUnuseAssetsPath + " " + workSpace + " " + customerMark)
    beforeBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace, customerMark)
    afterBuildUtils.dealNativeAssets(customerMark)
    with open(afterBuildUtils.NATIVE_RES_PATH + "/packWithHall", "w+"):
        pass
    iosCopyTools.run()
    iosPackPrepare.run(customerMark)

def buildApkWithHall():
    os.system("echo " + 'start buildApkWithHall')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForHotHall()
    cocosBuildUtils.updateBuilderFileStartScene()
    os.system(deleteUnuseAssetsPath + " " + workSpace + " " + customerMark)
    beforeBuildUtils.dealNativeAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace, customerMark)
    afterBuildUtils.dealAndroidProject(customerMark)
    afterBuildUtils.dealNativeAssets(customerMark)
    with open(afterBuildUtils.NATIVE_RES_PATH + "/packWithHall", "w+"):
        pass
    cocosBuildUtils.compileNativeAndroid(workSpace , customerMark)
    apkCopy.run("F:/http_server/apk/sepreate_" + os.environ["PACKAGE_BRANCH"].lower(), customerMark)

def buildHallHot():
    os.system("echo " + 'start buildHallHot')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForHotHall()
    cocosBuildUtils.updateBuilderFileStartScene()
    cmd = deleteUnuseAssetsPath + " " + workSpace + " " + customerMark
    os.system(cmd)
    beforeBuildUtils.dealHallHotAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace , customerMark)
    afterBuildUtils.dealHallHotAssets(customerMark)

def buildHallHotTest():
    os.system("echo " + 'start buildHallHot')
    beforeBuildUtils.deleteWorkSpaceOtherCustomerAssets(customerMark)
    beforeBuildUtils.deleteAssetsForHotHall()
    cocosBuildUtils.updateBuilderFileStartScene()
    cmd = deleteUnuseAssetsPath + " " + workSpace + " " + customerMark
    os.system(cmd)
    beforeBuildUtils.dealHallHotAssets(customerMark)
    cocosBuildUtils.buildNative(workSpace , customerMark)
    afterBuildUtils.dealHallHotAssets(customerMark)

def buildGameHot():
    os.system("echo " + 'start buildGameHot')
    beforeBuildUtils.deleteAssetsForHotGame()
    os.system(deleteUnuseAssetsPath + " " + workSpace)
    beforeBuildUtils.dealGameHotAssets(gameID)
    cocosBuildUtils.buildNative(workSpace)
    afterBuildUtils.dealGameHotAssets(gameID)

def buildHallH5():
    os.system("echo " + 'start buildHallH5')
    os.system(deleteUnuseAssetsPath + " " + workSpace)
    beforeBuildUtils.dealHallH5Asset()
    cocosBuildUtils.buildH5(workSpace)
    afterBuildUtils.dealHallH5Asset()

def buildGameH5():
    os.system("echo " + 'start buildGameH5')
    os.system(deleteUnuseAssetsPath + " " + workSpace)
    cocosBuildUtils.buildH5(workSpace)
    afterBuildUtils.dealGameH5Asset(gameID)

def modifyHallHot(sourceUrl):
    sourceZip = sourceUrl + "/" + versionControlUtil.HOT_FOLDER_PREFIX + customerMark + "-zip/all.zip"
    urllib.urlretrieve(sourceZip, "all.zip")
    z = zipfile.ZipFile('all.zip', 'r')
    if os.path.exists("build/jsb-link"):
        shutil.rmtree("build/jsb-link")
    os.makedirs("build/jsb-link")
    z.extractall(r"build/jsb-link")
    z.close()
    #修改customer_config
    find = False
    for root, dirs, files in os.walk("build/jsb-link/res/import"):
        for file in files:
            path = os.path.join(root, file)
            if file.find(".json") != -1:
                dic = json.load(open(path))
                if isinstance(dic, dict) and dic.get('json') and isinstance(dic['json'], dict) and dic['json'].get('HTTP_BASE_URL')\
                and dic['json'].get('WEBSOCKET_BASE_URL') and dic['json'].get('DOWNLOAD_URL_YFB'):
                    customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
                    dic['json']['HTTP_BASE_URL'] = customerConfig['HTTP_BASE_URL']
                    dic['json']['WEBSOCKET_BASE_URL'] = customerConfig['WEBSOCKET_BASE_URL']
                    dic['json']['openinstallKey'] = customerConfig['openinstallKey']
                    dic['json']['DOWNLOAD_URL'] = customerConfig['DOWNLOAD_URL']
                    dic['json']['bigVersion'] = customerConfig['bigVersion']
                    dic['json']['stationMark'] = customerConfig['stationMark']
                    dic['json']['wechatID'] = customerConfig['wechatID']
                    with open(path, 'w') as f:
                        f.writelines(json.dumps(dic))
                    find = True
                    break
        if find:
            break
    os.remove('build/jsb-link/project-tmp.manifest')
    afterBuildUtils.dealHallHotAssets(customerMark)

def threadToRun(taskIndex, buildType, isGame, originWorkSpace):
    if kUsePool:
        i = re.search(r"\d+", multiprocessing.current_process().name).group()
        threadIndex = int(i) - 1
    else:
        threadIndex = taskIndex
    global deleteUnuseAssetsPath, customerMark, workSpace
    cocosBuildUtils.useCocosIndex = threadIndex
    afterBuildUtils.mutiProcess = True
    os.chdir(originWorkSpace)
    if isGame:
        customerMarks = os.environ["GAME_ID"]
    else:
        customerMarks = os.environ["CUSTOMER_MARK"]
    arrCus = customerMarks.split(' ')
    index = 0
    for it in arrCus:
        if (kUsePool and index == taskIndex) or (not kUsePool and index % kProcessCnt == taskIndex):
            customerMark = it
            os.chdir(originWorkSpace + "/..")
            folderName = "FuGou" + str(threadIndex)
            os.system("rsync -r -t --chmod=777 --delete FuGou/ " + folderName)
            workSpace = os.path.abspath(os.path.join(os.getcwd(), folderName))
            os.chdir(workSpace)
            deleteUnuseAssetsPath = os.path.abspath(os.path.join(os.getcwd(), "ly_build_tools", "auto_build_customer", "deleteUnuseAssets"))
            if buildType == 'apk':
                buildApk()
            elif buildType == 'ios':
                buildiOS()
            elif buildType == 'hallHot':
                buildHallHot()
                os.chdir(workSpace)
                #拷贝HotUpdate走
                combineFolder(afterBuildUtils.LOCAL_HOT_PATH, "../HotUpdate")
            elif buildType == 'hotGame':
                buildGameHot()
            elif buildType == 'apkWithHall':
                buildApkWithHall()
            elif buildType == 'iosWithHall':
                buildiOSWithHall()
        index = index + 1
#把文件夹a里的内容搬到b里面去
def combineFolder(srcFolder, dstFolder):
    if not os.path.exists(dstFolder):
        os.mkdir(dstFolder)
    for i in os.listdir(srcFolder):
        if not os.path.exists(os.path.join(dstFolder, i)):
            shutil.move(os.path.join(srcFolder, i), dstFolder)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t' , '--buildType' , dest = "buildType")
    parser.add_option('-c' , '--customerMark' , dest = "customerMark")
    parser.add_option('-g' , '--gameID' , dest = "gameID")
    parser.add_option('' , '--onlySend' , dest = "onlySend")
    (option , args) = parser.parse_args()
    buildType = option.buildType
    customerMark = option.customerMark
    gameID = option.gameID
    deleteUnuseAssetsPath = os.path.abspath(os.path.join(os.getcwd(), "deleteUnuseAssets"))
    workSpace = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    sourceUrl = os.environ.get('sourceUrl')
    #切换到工作目录
    os.chdir(workSpace)
    #拉取CustomerUI
    if customerMark != None and sourceUrl == None:
        if os.path.exists("assets/resources/CustomerUI"):
            if os.path.exists(".git"):
                os.system("git clean -f -fdx assets/resources/CustomerUI")
            elif os.path.exists("../.git"):
                os.chdir("..")
                os.system("git clean -f -fdx FuGou/assets/resources/CustomerUI")
                os.chdir(workSpace)
        customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
        if not customerConfig['skinGit'] or not customerConfig['skinGitBranch']:
            raise Exception("皮肤所用git没有配置，customerConfig['skinGit']")
        os.system("git clone " + customerConfig['skinGit'] + " assets/resources/CustomerUI " + "--branch " + customerConfig['skinGitBranch'])
    #更新子模块
    if os.environ.get("PACKAGE_BRANCH") != None and sourceUrl == None:
        list = []
        for root, dirs, files in os.walk(workSpace):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # 遍历所有的文件夹
            for d in dirs:
                gitPath = os.path.join(root, d, ".git")
                if os.path.exists(gitPath):
                    list.append(os.path.join(root, d))
        for d in list:
            dirName = os.path.basename(d)
            if dirName == "CommonStaticAssets" or dirName == "CommonDynamicAssets" or dirName == "CommonStaticFishAssets"\
            or dirName == "CommonDynamicFishAssets":
                branchName = os.environ["PACKAGE_BRANCH"].lower()
                os.chdir(d)
                if dirName == "CommonStaticAssets" and branchName == "yfb":
                    branchName = "cocosV2"
                elif dirName == "CommonDynamicAssets" and branchName == "yfb":
                    branchName = "cocosV2"
                elif dirName == "CommonStaticFishAssets" and branchName == "yfb":
                    branchName = "cv2"
                elif dirName == "CommonDynamicFishAssets" and branchName == "yfb":
                    branchName = "cv2"
                os.system("git checkout " + branchName)
                os.system("git pull")
                os.system("git reset --hard")
                os.system("git clean -fdx")
                os.chdir(workSpace)
    #处理自动图集的bug，删掉自动图集中没引用到的资源
    if buildType == 'modifyHallHot':
        modifyHallHot(sourceUrl)
    elif buildType == 'apk':
        buildApk()
    elif buildType == 'ios':
        buildiOS()
    elif buildType == 'hallHot':
        buildHallHot()
    elif buildType == 'hallHotTest':
        buildHallHotTest()
    elif buildType == 'hallHotBat':
        if option.onlySend == "true":
            sys.exit(0)
        if os.path.exists("../HotUpdate"):
            shutil.rmtree("../HotUpdate")
        os.mkdir("../HotUpdate")
        if os.path.exists("../HotUpdate.zip"):
            os.remove("../HotUpdate.zip")
        customerMarks = os.environ["CUSTOMER_MARK"]
        arrCus = customerMarks.split(' ')
        if not kUsePool:
            processes = []
            for index in range(kProcessCnt):
                if index >= len(arrCus):
                    break
                if len(arrCus) <= 1:
                    threadToRun(index, 'hallHot', False, workSpace)
                    #t = threading.Thread(target=threadToRun,args=(index, 'hallHot', False, workSpace,))
                else:
                    t = multiprocessing.Process(target=threadToRun,args=(index, 'hallHot', False, workSpace,))
                processes.append(t)
                t.daemon = True
                t.start()
            for t in processes:
                t.join()
        else:
            po = multiprocessing.Pool(kProcessCnt)
            for index in range(len(arrCus)):
                po.apply_async(func=threadToRun,args=(index, 'hallHot', False, workSpace,))
            po.close()
            po.join()
        copyZip.process("../HotUpdate" , '../')
        for i in os.listdir("../HotUpdate"):
            for j in arrCus:
                if i == versionControlUtil.HOT_FOLDER_PREFIX + j:
                    arrCus.remove(j)
                    break
        if len(arrCus) > 0:
            os.system("echo these fail:")
            for i in arrCus:
                os.system("echo " + i)

    elif buildType == 'hotGame':
        buildGameHot()
    elif buildType == 'hallH5':
        buildHallH5()
    elif buildType == 'gameH5':
        buildGameH5()
    elif buildType == 'apkWithHall':
        buildApkWithHall()
    elif buildType == 'iosWithHall':
        buildiOSWithHall()
    elif buildType == 'buildTest':
        buildTest()
    elif buildType == 'apkBat':
        customerMarks = os.environ["CUSTOMER_MARK"]
        arrCus = customerMarks.split(' ')
        if not kUsePool:
            processes = []
            for index in range(kProcessCnt):
                if index >= len(arrCus):
                    break
                if len(arrCus) <= 1:
                    threadToRun(index, 'apkWithHall', False, workSpace)
                    #t = threading.Thread(target=threadToRun,args=(index, 'apkWithHall', False, workSpace,))
                else:
                    t = multiprocessing.Process(target=threadToRun,args=(index, 'apkWithHall', False, workSpace,))
                processes.append(t)
                t.daemon = True
                t.start()
            for t in processes:
                t.join()
        else:
            po = multiprocessing.Pool(kProcessCnt)
            for index in range(len(arrCus)):
                po.apply_async(func=threadToRun,args=(index, 'apkWithHall', False, workSpace,))
            po.close()
            po.join()
    elif buildType == 'iosBat':
        customerMarks = os.environ["CUSTOMER_MARK"]
        arrCus = customerMarks.split(' ')
        if not kUsePool:
            processes = []
            for index in range(kProcessCnt):
                if index >= len(arrCus):
                    break
                if len(arrCus) <= 1:
                    threadToRun(index, 'iosWithHall', False, workSpace)
                    #t = threading.Thread(target=threadToRun,args=(index, 'iosWithHall', False, workSpace,))
                else:
                    t = multiprocessing.Process(target=threadToRun,args=(index, 'iosWithHall', False, workSpace,))
                processes.append(t)
                t.daemon = True
                t.start()
            for t in processes:
                t.join()
        else:
            po = multiprocessing.Pool(kProcessCnt)
            for index in range(len(arrCus)):
                po.apply_async(func=threadToRun,args=(index, 'iosWithHall', False, workSpace,))
            po.close()
            po.join()