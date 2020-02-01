import uuid
import json
import os
from shutil import copyfile
import errno


def collect_uuids(fpath):
    meta_uuids = {}
    for root, dirs, files in os.walk(fpath, topdown=False):
        for name in files:
            if(os.path.splitext(name)[1] != '.meta'): continue
            name = os.path.join(root, name)
            with open(name) as f:
                jdata = json.loads(f.read())
                def walkjson(dic):
                    nid = dic.get('uuid')
                    if(nid):
                        meta_uuids[str(nid)] = str(uuid.uuid4())
                    for k,v in dic.items():
                        if isinstance(v, dict):
                            walkjson(v)
                walkjson(jdata)
            # print(meta_uuids)
    return meta_uuids
def replace_uuids(meta_uuids , fpath, opath):
    for root, dirs, files in os.walk(fpath, topdown=False):
        outroot = root.replace(fpath, opath)
        for name in files:
            ext = os.path.splitext(name)[1]
            out = os.path.join(outroot, name)
            name = os.path.join(root, name)
            # print(out, name)
            if(not os.path.exists(os.path.dirname(out))):
                os.makedirs(os.path.dirname(out))
            if(ext != '.meta' and ext != '.prefab' and ext != '.fire'):
                if name != out
                    copyfile(name, out)
                continue
            with open(name) as f:
                data = f.read()
                for k,v in meta_uuids.items():
                    data = data.replace(k, v)
                    with open(out, 'w') as o:
                        o.write(data)

def main():
    meta_uuids = collect_uuids('./origin')
    replace_uuids(meta_uuids , './origin', './gened')
main()