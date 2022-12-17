#cat tar-split-decoder.py 
import gzip
import json
import base64


segments = []
filename = None

with gzip.open('tar-split.json.gz', 'r') as fin:
    json_lines = fin.readlines()
    for json_line in json_lines:
        json_str = json_line.decode('utf-8')
        data = json.loads(json_str)
        if data['type'] == 1:
            filename = data['name']
        elif len(data['payload']) > 0:
            segments.append(data['payload'])

if filename:
    with open("/tmp/"+filename+".tar", 'wb') as fout:
        for segment in segments:
            fout.write(base64.b64decode(segment))
        #fout.write(bytes(int("777", 8)))