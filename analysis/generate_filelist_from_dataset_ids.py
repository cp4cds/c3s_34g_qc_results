#!/usr/bin/env Python

import os, sys
import logging
import requests
import json

logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)


DATASET_IDS_FILE = sys.argv[1]
# DATANODE = 'esgf-data.dkrz.de'
DATANODE = "esgf-index1.ceda.ac.uk"
FILEOUT = sys.argv[2]#'fnames_for_json_template.json'

def main():

    with open(DATASET_IDS_FILE) as r:
        ids = [line.split(',')[0].strip() for line in r]

    fname_dict = {}
    for id in ids:
        # id = 'CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.historical.r1i1p1f1.Amon.hfss.gn.v20180827'

        logging.debug(f'Searching {id}')
        era, mip, inst, model, expt, ens, table, var, grid, version = id.split('.')
        url = f"https://{DATANODE}/esg-search/search?type=File&mip_era=CMIP6&" \
              f"activity_id={mip}&source_id={model}&experiment_id={expt}&" \
              f"member_id={ens}&table_id={table}&variable_id={var}&" \
              f"replica=false&distrib=true&latest=true&retracted=false&" \
              f"fields=id,tracking_id&" \
              f"format=application%2Fsolr%2Bjson&limit=10000"

        logging.debug(url)
        resp = requests.get(url)
        content = resp.json()
        fnames = {}
        for res in content['response']['docs']:
            fname = '.'.join(res['id'].split('|')[0].split('.')[10:])
            fpid = res['tracking_id'][0]
            fnames[fname] = fpid

        fname_dict[id] = fnames

    with open(FILEOUT, 'w+') as jout:
        json.dump(fname_dict, jout, indent=4)


if __name__ == "__main__":
    main()