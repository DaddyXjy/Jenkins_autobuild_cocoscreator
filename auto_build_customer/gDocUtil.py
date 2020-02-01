#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/1/17
#Author: dylan
#Desc: google 文档工具

import requests
import csv
import os

gDocUrl = 'https://docs.google.com/spreadsheets/d/1gvVNSZCJsL5FIlb5y6coJCiusKxGz6TipodmDMBaMQg/export?format=csv&id=1YI6OBlnG9eExaToD3pmrPDA-z7R65mvr6jJdI5VULx0&gid=0'

def download(out):
    res = requests.get(gDocUrl)
    docFile = open(out, 'wb')
    for chunk in res.iter_content(10000):
        docFile.write(chunk)
    docFile.close()

def read(input):
    resultDoc = {}
    with open(input, 'rb') as f:
        reader = csv.reader(f)
        contents = []
        for row in reader:
            contents.append(row)
        for i in range(4 ,len(contents)):
            docKey = contents[i][0]
            resultDoc[docKey] = {}
            resultDoc[docKey]['name'] = contents[i][1]
            branch = None
            for j in range(1, len(contents[1])):    
                if(contents[1][j]):
                    branch = contents[1][j]
                    resultDoc[docKey][branch] = {}
                if branch:
                    subKey = contents[3][j]
                    if subKey:
                        resultDoc[docKey][branch][subKey] = contents[i][j]
        return resultDoc

#os.system("echo " + read('out.csv'))