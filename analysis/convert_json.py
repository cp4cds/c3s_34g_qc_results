#!/usr/bin/env Python

import json
import sys

ifile = sys.argv[1]

with open(ifile) as jsn:
    data = json.load(jsn)

ofile = ifile.replace('.json', '_formated.json')
new_data = {"datasets": data}
with open(ofile, 'w+') as jout:
    json.dump(new_data, jout, indent=4)