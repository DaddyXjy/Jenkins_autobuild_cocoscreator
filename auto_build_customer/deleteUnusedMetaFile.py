#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/10/26
#Author: dylan
#Desc: 删除废弃的meta文件,解决废弃mata文件,导致Jenkins打包无法进行的BUG,该脚本是在打包脚本前执行
import io
import os
import json
import shutil
import sys

def deleteUnuseMetaFileInDir(targetDir):
    for sPath in os.listdir(targetDir):
        realPath = os.path.join(targetDir , sPath)
        if os.path.isdir(realPath):
            deleteUnuseMetaFileInDir(realPath)
        else:
            if os.path.splitext(sPath)[-1] == '.meta':
                allPath = os.listdir(targetDir)
                if sPath[:-5] not in allPath:
                    os.remove(realPath)
                    os.system("echo " + 'delete unuse meta file:' + realPath)

def run():
    PRJ_ASSERT_PATH = os.path.join(os.getcwd() , 'assets')    
    deleteUnuseMetaFileInDir(PRJ_ASSERT_PATH)
    os.system("echo " + '=============delete mata file success!==============')
if __name__ == "__main__":
    run()