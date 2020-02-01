import os
import argparse

PROJ_DIR = '~/jenkins/'


PROJ_DIR = '~/jenkins/'
PACKAGE_BRANCH = None
def clean():
    path = os.path.join(PROJ_DIR, PACKAGE_BRANCH, 'huihuang', 'frameworks/runtime-src/proj.ios_mac/build')
    os.system('rm -rf ' + path)
    os.system('mkdir ' + path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pack ios clean')
    parser.add_argument('-e', help='pack env', default='test')
    args = vars(parser.parse_args())
    PACKAGE_BRANCH = args['e']

    clean()