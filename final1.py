import os
import sys
import json
import gzip
import base64

#create dictionary with sha256 content directories
layers_root = "/var/snap/docker/common/var-lib-docker/image/overlay2/layerdb/sha256/"

result = {}
for layer_dir in os.listdir(layers_root):
    path = "{}/{}/diff".format(layers_root, layer_dir) 
    with open(path, "r") as lfp:
        key = lfp.read()
        result[key] = "{}/{}".format(layers_root, layer_dir)

#map diffids to the dictionary
image_path = "/var/snap/docker/common/var-lib-docker/image/overlay2/imagedb/content/sha256"
with open("{}/{}".format(image_path, sys.argv[1]), "r") as fin:
    image_info = json.loads(fin.read())
    for layer_id in image_info['rootfs']['diff_ids']:
        print(layer_id)
        if layer_id in result.key():
            print (result.get(layer_id))
            layer_id.tarsplit_decoder()
            #read cache_id
            with open("/var/snap/docker/common/var-lib-docker/image/overlay2/layerdb/sha256/" + "layer_id" +"diff" + "cache_id" , "r") as x: 
                print(x.read())
            

#tar-split decoder function
def tarsplit_decoder():
    with gzip.open('tar-split.json.gz', 'r') as fin, open('layer.tar', 'wb') as fout:
        for line in fin.readlines():
            entry = json.loads(line)
            if entry['type'] == 2 and entry['payload'] and len(entry['payload']) > 0:
                decoded = base64.b64decode(entry['payload'])
                fout.write(decoded)
            elif entry['type'] == 1 and entry['payload'] and len(entry['payload']) > 0:
                with open(image_path +"/"+entry['name'], "rb") as fin:
                    content = fin.read()
                    print("Read {} bytes".format(len(content)))
                    fout.write(content)

def main(dir_name):
    main_path="/var/snap/docker/common/var-lib-docker/image/overlay2/imagedb/sha256/"
    with open("/var/snap/docker/common/var-lib-docker/image/overlay2/imagedb/sha256/" + "dir_name"):
        reqd=json.loads(key)