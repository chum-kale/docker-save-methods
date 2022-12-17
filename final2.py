import os
import sys
import json
import gzip
import base64

#create dictionary with sha256 content directories
layers_root = "/var/snap/docker/common/var-lib-docker/image/overlay2/layerdb/sha256/"

layer_map = {}

def load_layer_map():
    for layer_dir in os.listdir(layers_root):
        path = "{}/{}/diff".format(layers_root, layer_dir) 
        with open(path, "r") as lfp:
            key = lfp.read()
            layer_map[key] = "{}/{}".format(layers_root, layer_dir)
            
def save_image():
    #map diffids to the dictionary
    image_path = "/var/snap/docker/common/var-lib-docker/image/overlay2/imagedb/content/sha256"
    with open("{}/{}".format(image_path, sys.argv[1]), "r") as fin:
        image_info = json.loads(fin.read())
        layer_count = 0
        for layer_id in image_info['rootfs']['diff_ids']:
            print(layer_id)
            if layer_id in layer_map:
                print (layer_map.get(layer_id))
                tarsplit_decoder(layer_id, layer_count)
            layer_count += 1

#tar-split decoder function
def tarsplit_decoder(layer_id, layer_count):
    print("Writing layer: {}".format(layer_id))
    cache_id_path = '{}/cache-id'.format(layer_map[layer_id])
    with open(cache_id_path, 'r') as cfin:
        cache_id = cfin.read()

    tar_split_path = '{}/tar-split.json.gz'.format(layer_map[layer_id])
    with gzip.open(tar_split_path, 'r') as fin, open('{}.tar'.format(layer_count), 'wb') as fout:
        for line in fin.readlines():
            entry = json.loads(line)
            if entry['type'] == 2 and entry['payload'] and len(entry['payload']) > 0:
                decoded = base64.b64decode(entry['payload'])
                fout.write(decoded)
            elif entry['type'] == 1 and entry['payload'] and len(entry['payload']) > 0:
                cache_file_path = '/var/snap/docker/common/var-lib-docker/overlay2/{}/diff/{}'.format(cache_id, entry['name'])
                with open(cache_file_path, "rb") as fin:
                    content = fin.read()
                    print("Read {} bytes".format(len(content)))
                    fout.write(content)


if __name__ == '__main__':
    load_layer_map()
    save_image()