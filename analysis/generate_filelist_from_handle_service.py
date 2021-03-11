#!/usr/bin/env Python

import os
import logging
import requests
import json

logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)

DATASET_IDS_FILE = '../Catalogs/dataset-ids-pids_release2_202002_2.csv'
HANDLE_SERVICE = "http://hdl.handle.net/api/handles/"

with open(DATASET_IDS_FILE) as r:
    ds_pids = [line.split(',')[1].strip().lstrip('hdl:') for line in r]

pids_dict ={}

for ds in ds_pids:
    logging.debug(ds)
    url = f'{HANDLE_SERVICE}{ds}'
    logging.debug(url)
    resp = requests.get(url)
    content = resp.json()
    if not content['responseCode'] == 1:
        logging.debug(f"{ds}: {content['responseCode']}")
        continue

    fpids = ''
    for res in content['values']:
        if res['type'] == 'HAS_PARTS':
            fpids = res['data']['value']

    pids_dict[ds] = fpids.split(';')

with open('fpids_from_handleService.json', 'w+') as jout:
    json.dump(pids_dict, jout, indent=4)
