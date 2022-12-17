#Dummy script to generate one layer (has hardcoding)...

import sys
import gzip
import json
import base64


path = "/var/lib/docker/overlay2/2c5a65206136a2500080c2d2c8b2fc6246cce660db4dcc29e9979fc9cf8150ea/diff"

with gzip.open('tar-split.json.gz', 'r') as fin, open('layer.tar', 'wb') as fout:
    for line in fin.readlines():
        entry = json.loads(line)
        if entry['type'] == 2 and entry['payload'] and len(entry['payload']) > 0:
            decoded = base64.b64decode(entry['payload'])
            fout.write(decoded)
        elif entry['type'] == 1 and entry['payload'] and len(entry['payload']) > 0:
            with open(path+"/"+entry['name'], "rb") as fin:
                content = fin.read()
                print("Read {} bytes".format(len(content)))
                fout.write(content)