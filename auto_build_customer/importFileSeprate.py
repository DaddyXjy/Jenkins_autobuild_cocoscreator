#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2019/01/28
#Author: dylan
#Desc: 分离import文件

import jsonFileUtils
import os
PRJ_WORK_PATH = ''
uuidLibraryFilePath = 'library//uuid-to-mtime.json'

def getUUIDLibraryData(filePath):
    return jsonFileUtils.getJsonDataFromFile(filePath)

#根据模块路径获取uuid数据
def getRelativeUUIDDatas(uuidDatas , modulePath):
    results = []
    for uuid , uuidData in uuidDatas.items():
        relativePath = uuidData['relativePath']
        if relativePath.startswith(modulePath):
           results.append(uuid) 
    return results

#提取import文件目录
def extractUUIDModuleFiles(uuidDatas , modulePath):    
if __name__ == "__main__":
    PRJ_WORK_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../workspace/FuGou/"))
    #切换到工作目录
    os.chdir(PRJ_WORK_PATH)
    uuidDatas = getUUIDLibraryData(uuidLibraryFilePath)
    targetUUIDDatas = getRelativeUUIDDatas(uuidDatas , 'CustomMade\\ledian001')
    for data in targetUUIDDatas:
        os.system("echo " + data)





