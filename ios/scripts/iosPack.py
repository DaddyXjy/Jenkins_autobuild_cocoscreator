#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import argparse
import shutil
import datetime
import plistlib
import re
import customerConfigUtils
import io
import threading
import multiprocessing
kProcessCnt = 6

def build(projdir, plist, odir, name, env):
    os.system('echo build start...')
    os.system('security unlock-keychain -p " " ~/Library/Keychains/login.keychain')
    tmpPath = os.path.join(projdir, 'frameworks/runtime-src/proj.ios_mac/build/')
    #os.system('rm -rf ' + tmpPath)
    archPath = os.path.join(tmpPath, 'build.xcarchive')
    res = os.system('xcodebuild archive -project ' + os.path.join(projdir, 'frameworks/runtime-src/proj.ios_mac/huihuang.xcodeproj') + ' -scheme niuniu1031-mobile -archivePath ' + archPath + ' -allowProvisioningUpdates')
    if res != 0:
        raise Exception('build failed')
    res = os.system('xcodebuild -exportArchive -archivePath ' +  archPath + ' -exportPath ' + odir + ' -exportOptionsPlist ' + plist)
    if res != 0:
        raise Exception('export failed')
    outipa =  os.path.join(odir, name)
    os.system('mv ' + os.path.join(odir, 'niuniu1031-mobile.ipa') + ' ' + outipa)
    if not os.path.exists(outipa):
        raise Exception('pack failed!!')
    os.system('rsync -e "ssh -o PubkeyAuthentication=yes -o stricthostkeychecking=no" -r -t --delete ' + outipa + ' leying@172.20.100.100:/cygdrive/f/http_server/ios/' + env)

def copyTemplateDir(srcDir , dstDir):
    if not os.path.exists(srcDir):
        return
    for dirTemp in os.listdir(srcDir):
        realSrcDir = os.path.join(srcDir , dirTemp)
        realDstDir = os.path.join(dstDir , dirTemp)
        if not os.path.exists(os.path.dirname(realDstDir)):
            os.makedirs(os.path.dirname(realDstDir))
        if os.path.isdir(realSrcDir):
            copyTemplateDir(realSrcDir , realDstDir)
        else:
            os.system('echo copy file:', realSrcDir, realDstDir)
            shutil.copyfile(realSrcDir , realDstDir)

def changeBundleID(dir):
    infofile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/ios/Info.plist')
    bundle = None
    with open(infofile) as f:
        data = plistlib.readPlist(f)
        bundle = data['CFBundleIdentifier']
    pxfile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/huihuang.xcodeproj/project.pbxproj')
    pxData = None
    with open(pxfile) as f:
        data = f.read()
        pxData = re.sub(r'PRODUCT_BUNDLE_IDENTIFIER = .*;', 'PRODUCT_BUNDLE_IDENTIFIER = ' + bundle + ';', data)
    with open(pxfile, 'w') as f:
        f.write(pxData)

def dealiOSProject(dir, customerMark):
    customerConfigUtils.CUSTOMER_CONFIG_PATH = "../customer_config"
    customerConfig = customerConfigUtils.getCustomerConfig(customerMark)
    #先同步样例工程的Info.plist,niuniu1031-mobile.entitlements
    infofile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/ios/Info.plist')
    entitlementsFile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/niuniu1031-mobile.entitlements')
    os.system("rsync -t ~/originProj/huihuang/frameworks/runtime-src/proj.ios_mac/ios/Info.plist " + infofile)
    os.system("rsync -t ~/originProj/huihuang/frameworks/runtime-src/proj.ios_mac/niuniu1031-mobile.entitlements " + entitlementsFile)
    with open(infofile, "r") as f:
        infoData = plistlib.readPlist(f)
    #0.修改appName
    infoData['CFBundleDisplayName'] = customerConfig['appName']
    #1.修改buldleID
    if not customerConfig.has_key('iosBundleID'):
        raise Exception('error when get iosBundleID from customer_config:' + customerMark)
    pxfile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/huihuang.xcodeproj/project.pbxproj')
    with open(pxfile) as f:
        pxData = f.read()
    pxData = re.sub(r'PRODUCT_BUNDLE_IDENTIFIER = [^;]*\.GeTui;', 'PRODUCT_BUNDLE_IDENTIFIER = ' + customerConfig['iosBundleID'] + '.GeTui;', pxData)
    pxData = re.sub(r'PRODUCT_BUNDLE_IDENTIFIER = [^;]*(?<!GeTui);', 'PRODUCT_BUNDLE_IDENTIFIER = ' + customerConfig['iosBundleID'] + ';', pxData)
    with open(pxfile, 'w') as f:
        f.write(pxData)
    #2.修改OpenInstall，3个地方
    with open(entitlementsFile, "r") as f:
        entitleData = plistlib.readPlist(f)
    if not customerConfig.has_key('openinstallKey'):
        raise Exception('error when get openinstallKey from customer_config:' + customerMark)
    entitleData['com.apple.developer.associated-domains'][0] = "applinks:" + customerConfig['openinstallKey'] + ".openinstall.io"
    for item in infoData['CFBundleURLTypes']:
        if item["CFBundleURLName"] == "openinstall":
            item['CFBundleURLSchemes'][0] = customerConfig['openinstallKey']
            break
    infoData['com.openinstall.APP_KEY'] = customerConfig['openinstallKey']
    with open(entitlementsFile, "w") as f:
        plistlib.writePlist(entitleData, f)
    #3.填写wechatID
    for item in infoData['CFBundleURLTypes']:
        if item["CFBundleURLName"] == "weixin":
            if customerConfig.has_key('wechatID'):
                item['CFBundleURLSchemes'][0] = customerConfig['wechatID']
            else:
                item['CFBundleURLSchemes'][0] = ""
            break
    with open(infofile, "w") as f:
        plistlib.writePlist(infoData, f)
    #4.修改个推id
    pushInfoFile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/pushNotification/Info.plist')
    with open(pushInfoFile, "r") as f:
        pushData = plistlib.readPlist(f)
    pushData['CFBundleIdentifier'] = customerConfig['iosBundleID'] + ".GeTui"
    with open(pushInfoFile, "w") as f:
        plistlib.writePlist(pushData, f)
    AppControllerFile = os.path.join(dir, 'frameworks/runtime-src/proj.ios_mac/AppController.h')
    controllerData = ''
    with io.open(AppControllerFile, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                line = re.sub(r'(#define\s+kGtAppId\s+@")[^"]*', r'\g<1>' + customerConfig["GETUI_APP_ID"], line)
                line = re.sub(r'(#define\s+kGtAppKey\s+@")[^"]*', r'\g<1>' + customerConfig["GETUI_APP_KEY"], line)
                line = re.sub(r'(#define\s+kGtAppSecret\s+@")[^"]*', r'\g<1>' + customerConfig["GETUI_APP_SECRET"], line)
                controllerData += line
    with io.open(AppControllerFile, 'w', encoding="utf-8") as f:
        f.write(controllerData)
def threadToRun(threadIndex, args):
    channels = args['c'].split(' ')
    index = 0
    for channel in channels:
        if index % kProcessCnt == threadIndex:
            ddir = os.path.abspath(args['d'])
            env = args['e']
            tdir = os.path.abspath(args['t'] or os.path.join('../', env, 'template'))
            sdir = os.path.abspath(args['t'] or os.path.join('../', env, channel))
            if not os.path.exists(sdir):
                sdir = tdir
            pdir = os.path.join(ddir, env, channel, 'huihuang')
            plistName = args['l'] or channel
            if(not os.path.exists(os.path.join(args['p'], plistName + '.plist'))):
                plistName = 'enterprise'
            plist = os.path.abspath(os.path.join(args['p'], plistName + '.plist'))
            time = datetime.datetime.today()
            odir =  args['o'] or os.path.abspath(os.path.join('/Users/leying/out', env, str(time.year) + '_' + str(time.month) + '_' + str(time.day), channel, args['b']))
            name = args['n'] or ('v2_' + env + '_' + channel + '.ipa')
            os.system('echo project:' + pdir)
            os.system('echo channel:' + channel)
            os.system('echo key plist:' + plist)
            os.system('echo template:' + sdir)
            os.system('echo output:' + os.path.join(odir, name))
            os.system('echo packing...')
            #copyTemplateDir(sdir, pdir)
            os.system("rsync -r -t " + sdir + "/ " + pdir)
            #用与安卓通用的配置文件对工程进行处理
            os.environ["PACKAGE_BRANCH"] = env
            dealiOSProject(pdir, channel)
            #changeBundleID(pdir)
            build(pdir, plist, odir, name, env)
        index = index + 1
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='pack ios ipa')
    parser.add_argument('-d', help='project root dir', default='/Users/leying/tmpProjs/')
    parser.add_argument('-c', help='channel name', required=True)
    parser.add_argument('-t', help='project template')
    parser.add_argument('-e', help='pack env', default='test')
    parser.add_argument('-o', help='output dir')
    parser.add_argument('-n', help='ipa name')
    parser.add_argument('-p', help='export plist dir', default='../pack/')
    parser.add_argument('-l', help='export plist name', default=None)
    parser.add_argument('-b', help='build num', default=0)
    args = vars(parser.parse_args())
    arrCus = args['c'].split(' ')
    processes = []
    for index in range(kProcessCnt):
        if index >= len(arrCus):
            break
        if len(arrCus) <= 1:
            threadToRun(index, args)
        else:
            t = threading.Thread(target=threadToRun,args=(index, args))
            processes.append(t)
            t.daemon = True
            t.start()
        # else:
        #     t = multiprocessing.Process(target=threadToRun,args=(index, args))
    for t in processes:
        t.join()
    
