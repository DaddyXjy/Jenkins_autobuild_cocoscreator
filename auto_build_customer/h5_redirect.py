#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import re
import argparse

folder = None
build_path = None
redirect_url = None

def do_redirect():
    global redirect_url
    if not redirect_url:
        return
    os.system("echo " + ('redirect main.js url'))
    data = None
    with open(os.path.join(folder, build_path, 'main.js')) as f:
        data = f.read()
    if redirect_url != "" and redirect_url != "\"\"":
        redirect_url = "\"" + redirect_url + "\""
    else:
        redirect_url = "\"\""
    data = re.sub(r'libraryPath:.*,', "libraryPath: \"\" + " + redirect_url + ' + subGameDirPrefix + \"res/import\",' , data)        
    data = re.sub(r'rawAssetsBase:.*,', "rawAssetsBase: \"\" + " + redirect_url + ' + subGameDirPrefix + \"res/raw-\",' , data)        
    with open(os.path.join(folder, build_path, 'main.js'), 'w') as f:
        f.write(data)

def do_config():
    os.system("echo " + ('genarate config file src/customer_config.js'))
    config_data = None
    with open("assets/CustomMade/customer_config.json") as f:
        config_data = f.read()
    
    config_data = "window.GOLOBAL_CUSTOMER_CONFIG = " + config_data
    with open(os.path.join(folder, build_path, "src/customer_config.js"), 'w') as f:
        f.write(config_data)

def run():
    global redirect_url
    global folder
    global build_path
    redirect_url = os.environ["REDIRECT_PATH"]
    folder = 'build'
    build_path = 'web-mobile'
    do_config()
    do_redirect()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='h5 redirect')
    parser.add_argument('-f', help='folder', default='../../build')
    parser.add_argument('-b', help='build path', default='web-mobile')
    parser.add_argument('-r', help='redirect', default=None)
    args = vars(parser.parse_args())
    folder = args['f']
    build_path = args['b']
    redirect_url = args['r']

    do_config()
    do_redirect()