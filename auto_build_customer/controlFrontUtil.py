#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/1/17
#Author: dylan
#Desc: 总控后台登录脚本

from PIL import Image
import pytesseract
import requests
import time
import json
import os
codePhotoUrl = 'http://controlfront.wg-dns-prod.com/api/generateCode?'
loginUrl = 'http://controlfront.wg-dns-prod.com/api/login'
siteListUrl = 'http://controlfront.wg-dns-prod.com/api/siteManage/sitelist'
userName = 'admin'
password = '123456'
def downloadPhoto(out):
    res = requests.get(codePhotoUrl + str(int(time.time())))
    photoFile = open(out, 'wb')
    for chunk in res.iter_content(10000):
        photoFile.write(chunk)
    photoFile.close()

def getCodeFromPhoto(input):
    img = Image.open(input)
    text = pytesseract.image_to_string(img)
    return text

def getCode():
    photoPath = 'test.png'
    downloadPhoto(photoPath)
    text = getCodeFromPhoto(photoPath)
    return text

def login():
    loginReq = None
    cookies = None
    try:
        code = getCode()
        loginReq = requests.post(url= loginUrl , data = {
            "username": userName,
            "password": password,
            "code": code
        })
        loginReq.raise_for_status()
    except:
        pass
    else:
        if json.loads(loginReq.text)['code'] == '200':
            cookies = loginReq.cookies
    return cookies

def loginUntilSuccess():
    for i in range(0 , 1000):
        cookies = login()
        if cookies:
            return cookies         
def getSiteList(cookies):
    data = {
        "conditionsMap":{"siteName": "", "account": "", "status": "", "maintainStatus": ""},
        "limit": 1000,
        "offset": 0,
        "sort": "createDate",
        "sortOrder": "desc"
    }
    jsonData = json.dumps(data)
    siteListReq = requests.post(url = siteListUrl, json = data, cookies= cookies)
    return json.loads(siteListReq.text)

def getSiteIdByStationMark(stationMark):
    os.system("echo " + 'process getSiteIdByStationMark')
    cookies = loginUntilSuccess()
    siteList = getSiteList(cookies)
    siteRowDataList = siteList['rows']
    for siteRowData in siteRowDataList:
        if siteRowData['stationMark'] == stationMark:
            return siteRowData['siteId']
if __name__ == "__main__":
    os.system("echo " + getSiteIdByStationMark('wg0001'))
