#!/usr/bin/env Python

import os
import json
import argparse
import logging
logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)

def main():
    # Read in data
    with open('../Catalogs/release2_file_pids.json') as jsn:
        data = json.load(jsn)

    dataset_pids = {}
    with open('../Catalogs/dataset-ids-pids_release2_202002.csv') as r:
        for line in r:
            id, pid = line.split(',')[0], line.split(',')[1].strip()
            dataset_pids[id] = pid

    # Set up json header
    jout = {}
    jout["header"] = {"application:": '', 'Author': '', 'Institution': '', 'Date': '', 'version': ''}
    jout["results"] = {}
    jout["datasets"] = {}

    for dsid, files in data.items():
        if "piControl" in dsid or "amip" in dsid:
            print(f'skipping ds {dsid}')
            continue
        dspid = dataset_pids[dsid]
        # print(dsid, dspid)
        json_ds_qc = {'error_severity': '', 'error_message': ''}
        ds_qcStatus = ""

        json_files = {}
        for f in files:
            for fpid, fname in f.items():
                json_files[fpid] = {'filename': fname,
                                    'qc_status': '',
                                    'error_severity': '',
                                    'error_message': ''
                                    }

        jout["datasets"][dspid] = {'dset_id': dsid,
                                   'qc_status': ds_qcStatus,
                                   'dataset_qc': json_ds_qc,
                                   'files': json_files
                                   }

    # Output JSON
    json_obj = json.dumps(jout, indent=4)
    with open('QC_template.json', "a+") as o:
        o.write(json_obj)


if __name__ == "__main__":

    main()