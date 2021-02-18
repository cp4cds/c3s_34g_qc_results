#!/usr/bin/env Python

import os
import json
import logging
import datetime as dt

today = dt.datetime.today().isoformat()[:10]

logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)


QCDIR = '../QC_Results/'
RELEASE_DATASETS_FILE = os.path.join('../Catalogs/', 'dataset-ids-pids_release2_202002_2.csv')
MISSING_DATASETS = os.path.join(QCDIR, f'missing_ds_{today}.txt')
FAILED_DATASETS = os.path.join(QCDIR, f'failed_ds_{today}.txt')
PASSED_DATASETS = os.path.join(QCDIR, f'passed_ds_{today}.txt')
LOGFILES = [MISSING_DATASETS, FAILED_DATASETS, PASSED_DATASETS]

for file in LOGFILES:
    if os.path.exists(file):
        os.remove(file)


# CHECKS = ['cf', 'errata', 'nctime', 'prepare', 'range']


def read_qc_log(filename):
    """
    Read log file
    :param filename: Valid JSON in correct format
    :return:
    """

    logging.info(f"Reading QC file : {filename}")
    if os.path.exists(filename):
        with open(filename) as jsn_file:
            results = json.loads(jsn_file.read())
        return results
    else:
        return None


def write_log(missing_ds, ofile):
    """
    Append a dataset to a logfile
    :param missing_ds: Dataset id
    :param ofile: logfile
    :return: 
    """
    
    with open(ofile, 'a+') as w:
        w.writelines(f"{missing_ds}\n")


def read_dsids_and_pids(ifile):
    """
    Read dataset and pid csv file
    :param ifile: file with valid dataset and pids for release
    :return: dict[pid] = dataset_id 
    """
    
    logging.info(f"Reading file : {ifile}")
    dsids = {}
    with open(ifile, 'r') as r:
        for line in r:
            dsids[line.split(',')[1].strip()] = line.split(',')[0].strip()

    return dsids


def main():

    # Read all datasets for release
    ids = read_dsids_and_pids(RELEASE_DATASETS_FILE)
    pids = list(ids.keys())

    # load all logs
    CHECKS = []
    cf_results = read_qc_log(os.path.join(QCDIR, 'QC_cfchecker.json'))
    if cf_results: CHECKS.append('cf')
    # errata_results = read_qc_log(os.path.join(QCDIR, 'QC_errata.json'))
    # if errata_results: CHECKS.append('errata')
    # nctime_results = read_qc_log(os.path.join(QCDIR, 'QC_nctime.json'))
    # if nctime_results: CHECKS.append('nctime')
    # prepare_results = read_qc_log(os.path.join(QCDIR, 'QC_prepare.json'))
    # if prepare_results: CHECKS.append('prepare')
    # range_results = read_qc_log(os.path.join(QCDIR, 'QC_rangecheck.json'))
    # if range_results: CHECKS.append('ranges')
    # handle_results = read_qc_log(os.path.join(QCDIR, 'QC_handles.json'))
    # if handle_results: CHECKS.append('handle')

    logging.info(f'CHECKS: {CHECKS}')

    for pid in pids:
        logging.debug(f"Interogating {pid}")
        missing_datasets = set()
        results_status = {}

        for check in CHECKS:
            logging.debug(f'QC CHECK {check}')
            try:
                logging.debug(eval(f"{check}_results")['datasets'][pid])
                results_status[check] = eval(f"{check}_results")['datasets'][pid]
                logging.debug(f" {results_status[check]}")

            except Exception as error:
                logging.debug(f"Error in PID : {error}")
                missing_datasets.add(pid)

        if len(missing_datasets) > 0:
            write_log(f"{pid, ids[pid]}", MISSING_DATASETS)

        else:
            ds_status = {}
            for check in CHECKS:
                results_status[check] = eval(f"{check}_results")['datasets'][pid]
                ds_status[check] = results_status[check]['qc_status']

            for qc, status in ds_status.items():
                if not status == 'pass':
                    logging.debug(f'dataset failed {qc, status}')
                    write_log(f"{pid, ids[pid]}", FAILED_DATASETS)
                    break
                else:
                    write_log(f"{pid, ids[pid]}", PASSED_DATASETS)


if __name__ == "__main__":

    main()