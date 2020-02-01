#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import csv
import os
import plistlib
import re
import gDocUtil

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def changeiosplist(content):
    for channel in content:
        for branch, configs in content[channel].items():
            if branch == 'name':
                continue
            
            os.system("echo " + ('START EDIT:', branch, channel))
            path = os.path.join('../ios', branch, channel, 'frameworks/runtime-src/proj.ios_mac/ios/Info.plist')
            if os.path.exists(path):        
                data = None
                os.system("echo " + ('Edit file:', path))
                os.system("echo " + ('bundle', configs['bundle']))
                os.system("echo " + ('appkey', configs['appkey']))
                os.system("echo " + ('weixin', configs['app_wechat_id']))
                with open(path, 'r') as f:
                    data = plistlib.readPlist(f)
                    os.system("echo " + data)
                    if configs['bundle']:
                        data['CFBundleIdentifier'] = configs['bundle']
                    data['CFBundleDisplayName'] = (branch == 'online' and content[channel]['name'] or (content[channel]['name'] + '_'+branch)).encode('UTF-8')
                    if configs['appkey']:
                        data['com.openinstall.APP_KEY'] = configs['appkey']
                    for item in data['CFBundleURLTypes']:
                        if item['CFBundleURLName'] == 'openinstall':
                            if configs['appkey']:
                                item['CFBundleURLSchemes'] = [configs['appkey']]
                        
                        if item['CFBundleURLName'] == 'weixin':
                            item['CFBundleURLSchemes'] = [configs['app_wechat_id']]
                with open(path, 'w') as f:
                    plistlib.writePlist(data, f)
            

            path = os.path.join('../ios', branch, channel, 'frameworks/runtime-src/proj.ios_mac/niuniu1031-mobile.entitlements')
            if os.path.exists(path) and configs['appkey']:
                data = None
                with open(path, 'r') as f:
                    os.system("echo " + ('Edit file:', path))
                    os.system("echo " + ('appkey', configs['appkey']))
                    data = f.read()
                    data = re.sub(r'applinks:.*\.openinstall\.io', 'applinks:' + configs['appkey'] + '.openinstall.io', data)
                with open(path, 'w') as f:
                    f.write(data)

def run():
    gDocUtil.download('out.csv')
    content = gDocUtil.read('out.csv')
    if content:
        changeiosplist(content)
    else:
        raise Exception('read csv error!!')
    os.remove('out.csv')

if __name__ == "__main__":
    run()
