#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/1/17
#Author: dylan
#Desc: 在openinstall 上面创建应用
import optparse
import requests
import logging
import sys
import json
logging.basicConfig(level=logging.DEBUG , stream =sys.stdout)

openInstallLoginUrl = 'https://developer.openinstall.io/cgi/account/login'
username = 'qq9456421173@gmail.com'
password = 'f666d9092293ac4cefcc48794611a90e606623397741772156a704ad31e270dc83fb384e34d66cfbf4714a7af9e5f007ab6346b76bd707cbb05ccaf291f66e38'
openinstallAddUrl = 'https://developer.openinstall.io/cgi/appinfo/add'
appListUrl = 'https://developer.openinstall.io/cgi/appinfo/all?_=1547451189095'

def addOpeninstallApp(appName):
    existFlag = isAppNameExist(getAppList() , appName)
    if existFlag:
        raise Exception('app is already existed! create failed')
    #login
    loginReq = requests.post(url = openInstallLoginUrl , data = {
        'username' : username , 'password' : password
    })
    #add
    requests.post(openinstallAddUrl, data= {"appName": appName}, cookies = loginReq.cookies)
    logging.info(u'[+] create app:' + u' success')
def getAppList():
    #login
    loginReq = requests.post(url = openInstallLoginUrl , data = {
        'username' : username , 'password' : password
    })
    appListReq = requests.get('https://developer.openinstall.io/cgi/appinfo/all?_=1547451189095', cookies=loginReq.cookies)
    apps = json.loads(appListReq.text)['body']['ownerApps']
    return apps

def isAppNameExist(appList , appName):
    for app in appList:
        if appName == app['appName']:
            return True
    return False
def main():
    parser = optparse.OptionParser('Usage %prog -name <app name> ')
    parser.add_option('-n' , dest = 'appName' , type = 'string' , help = 'specify target appName')
    (options , args) = parser.parse_args()
    appName = options.appName
    addOpeninstallApp(appName)
if __name__ == "__main__":
    main()