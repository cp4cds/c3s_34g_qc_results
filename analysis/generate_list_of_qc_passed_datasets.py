#!/usr/bin/env Python

import os, sys
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
UNKNOWN_DATASETS = os.path.join(QCDIR, f'unknown_ds_{today}.txt')
LOGFILES = [MISSING_DATASETS, FAILED_DATASETS, PASSED_DATASETS, UNKNOWN_DATASETS]

for file in LOGFILES:
    if os.path.exists(file):
        os.remove(file)


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


def get_checks():
    # load all logs
    CHECKS = {}

    qc_types = ['cf', 'errata', 'nctime', 'prepare', 'ranges', 'handle']
    qc_types = ['cf', 'errata', 'nctime', 'handle']

    for qc in qc_types:
        fname = f'QC_{qc}.json'
        qc_data = read_qc_log(os.path.join(QCDIR, f'QC_{qc}.json'))
        if qc:
            CHECKS[qc] = qc_data

    return CHECKS


def check_missing(pid, pids_dict, ids_and_pids, QC_CHECKS):

    missing = False
    for check in QC_CHECKS.keys():
        logging.debug(f'{check}')
        if not pid in pids_dict[check]:
            logging.debug(f"MISSING: {check} {pid}")
            write_log(f"{check, pid, ids_and_pids[pid]}", MISSING_DATASETS)
            missing = True

    return missing


def main():

    # Read all datasets for release
    ids_and_pids = read_dsids_and_pids(RELEASE_DATASETS_FILE)
    pids = list(ids_and_pids.keys())
    QC_CHECKS = get_checks()
    if len(QC_CHECKS.keys()) < 1:
        sys.exit()

    for pid in pids:
      # test missing pid from file
      # if pid == 'hdl:21.14100/80538650-b2b2-3ee8-be87-66994c3ce895':

      # test missing qc status
      # if pid == 'hdl:21.14100/9835ddcb-5e71-3801-a594-bb7191528461':

        ds_status = {}
        pids_dict = {}

        for check, qc_results in QC_CHECKS.items():
            pids_dict[check] = list(qc_results['datasets'].keys())
        # [list(qc_results['datasets'].keys()) for check, qc_results in QC_CHECKS.items()]

        for check, qc_results in QC_CHECKS.items():
            # Check for any missing data in results files
            missing = check_missing(pid, pids_dict, ids_and_pids, QC_CHECKS)
            if missing:
                continue

            logging.debug(f"Interogating {pid}")
            ds_status[check] = qc_results['datasets'][pid]['qc_status']
            if not ds_status[check]:
                ds_status[check] = 'missing'

        if ('fail' in ds_status.values()) or ('missing' in ds_status.values()) or ('unknown' in ds_status.values()):
            for qc, status in ds_status.items():
                if status == 'fail':
                    logging.debug(f'dataset failed {qc, status}')
                    write_log(f"{qc, pid, ids_and_pids[pid]}", FAILED_DATASETS)

                elif (status == 'missing') or (status == 'unknown'):
                    logging.debug(f'dataset missing {qc, status}')
                    write_log(f"{qc, pid, ids_and_pids[pid]}", UNKNOWN_DATASETS)
        else:
            logging.debug(f'dataset passed {pid}')
            write_log(f"{pid, ids_and_pids[pid]}", PASSED_DATASETS)


if __name__ == "__main__":

    main()