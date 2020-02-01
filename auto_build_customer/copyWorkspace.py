#!/usr/bin/python
# -*- coding: UTF-8 -*- 

#Date: 2018/10/26
#Author: dylan
#Desc: 拷贝工程
import io
import os
import json
import shutil
import sys

os.system("echo " + os.path.join(os.getcwd(), "../../.."))

prj_name =  os.path.basename(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
work_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
copy_path = os.path.abspath(os.path.join('../../../../' , prj_name + '_clone'))
if os.path.exists(copy_path):
	shutil.rmtree(copy_path)
shutil.copytree(work_path , copy_path)
os.system("echo " + '=============copy prj success!==============')