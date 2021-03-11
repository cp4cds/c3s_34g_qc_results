#!/usr/bin/env Python

import os
import json
import argparse
import logging
from datetime import datetime as dt

FILENAME_CACHE = '../Catalogs/fnames_for_json_template.json'
RELEASE_IDS_AND_PIDS = '../Catalogs/dataset-ids-pids_release2_202002_2.csv'
OFILE = 'test-template.json'


def setup():
    logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)
    if os.path.exists(OFILE):
        os.remove(OFILE)


def main():
    # Read in data
    with open(FILENAME_CACHE) as jsn:
        data = json.load(jsn)

    dataset_pids = {}
    with open(RELEASE_IDS_AND_PIDS) as r:
        for line in r:
            id, pid = line.split(',')[0], line.split(',')[1].strip()
            dataset_pids[id] = pid

    # Set up json header
    jout = {}
    jout["header"] = {"application:": '', 'Author': '', 'Institution': '', 'Date': '', 'version': '', 'QC_template': 'version 2: 2021-03-05'}
    jout["datasets"] = {}

    for dsid, files in list(data.items()):
        if "piControl" in dsid or "amip" in dsid:
            logging.debug(f'skipping ds in piControl or amip: {dsid}')
            continue

        dspid = dataset_pids[dsid]
        logging.debug(f'ID: {dsid}; PID: {dspid}')

        json_files = {}
        for fname, fpid in files.items():
            logging.debug(f'FILENAME: {fname}, FILE_PID: {fpid}')

            # Set file level info
            json_files[fpid] = {'filename': fname,
                                'file_qc_status': '',
                                'file_error_severity': '',
                                'file_error_message': ''
                                }

        # Set dataset level details
        jout["datasets"][dspid] = {
            'dset_id': dsid,
            'dset_qc_status': '',
            'dset_error_severity': '',
            'dset_error_message': '',
            'files': json_files
        }

    # Output JSON
    json_obj = json.dumps(jout, indent=4)
    with open(OFILE, "a+") as o:
        o.write(json_obj)


if __name__ == "__main__":
    setup()
    main()