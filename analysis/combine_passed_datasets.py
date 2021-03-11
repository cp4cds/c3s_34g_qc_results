#!/usr/bin/env Python

import os
import logging
import datetime as dt

logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)
TODAY = dt.datetime.today().isoformat()[:10]
DATE = '2021-02-23'
BASEDIR = '/gws/nopw/j04/cp4cds1_vol3/c3s_34g/c3s_34g_qc_results/QC_Results'
QC_TYPES = ['cf', 'errata', 'nctime', 'prepare', 'ranges', 'handle']
CEDA_MISSING = os.path.join(BASEDIR, 'datasets_missing_at_ceda.txt')
DKRZ_MISSING = os.path.join(BASEDIR, 'datasets_missing_at_dkrz.txt')


def get_set(data_str, type='qc'):

    if type == 'qc':
        d_set = set()
        fname = os.path.join(BASEDIR, f'{data_str}-{DATE}', 'passed.txt')
        with open(fname) as r:
            for line in r:
                id = line.strip().split(',')[1].strip(')').strip()
                d_set.add(id)

    if type == 'missing':
        fname = os.path.join(BASEDIR, f'datasets_missing_at_{data_str}.txt')
        d_set = set()
        with open(fname) as r:
            [d_set.add(line.strip()) for line in r]

    logging.debug(f'Generated {data_str} set')
    return d_set


def main():

    cf_set = get_set('cf', type='qc')
    errata_set = get_set('errata', type='qc')
    nctime_set = get_set('nctime', type='qc')
    prepare_set = get_set('prepare', type='qc')
    range_set = get_set('ranges', type='qc')
    handle_set = get_set('handle', type='qc')

    logging.debug(f'CF: {type(cf_set)}, {len(cf_set)}')
    logging.debug(f'ERRATA: {type(errata_set)}, {len(errata_set)}')
    logging.debug(f'NCTIME: {type(nctime_set)}, {len(nctime_set)}')
    logging.debug(f'PREPARE: {type(prepare_set)}, {len(prepare_set)}')
    logging.debug(f'RANGE: {type(range_set)}, {len(range_set)}')
    logging.debug(f'HANDLE: {type(handle_set)}, {len(handle_set)}')

    logging.info(f'Generating intersection of qc results')
    result_set = cf_set.intersection(errata_set, nctime_set, prepare_set, range_set, handle_set)
    logging.debug(f'LEN CF: {len(cf_set)}')
    logging.debug(f'LEN ERRATA: {len(errata_set)}')
    logging.debug(f'LEN NCTIME: {len(nctime_set)}')
    logging.debug(f'LEN PREPARE: {len(prepare_set)}')
    logging.debug(f'LEN RANGE: {len(range_set)}')
    logging.debug(f'LEN HANDLE: {len(handle_set)}')
    logging.info(f'RESULT SET: {len(result_set)}')

    ceda_missing = get_set('ceda', type='missing')
    dkrz_missing = get_set('dkrz', type='missing')
    ipsl_missing = get_set('ipsl', type='missing')
    logging.debug(f'CEDA MISSING: {len(ceda_missing)}, DKRZ MISSING {len(dkrz_missing)}, IPSL MISSING {len(ipsl_missing)}')

    missing_sets = ceda_missing.union(dkrz_missing, ipsl_missing)

    # missing_sets = ceda_missing.intersection(dkrz_missing)
    logging.debug(f'CEDA MISSING: {len(ceda_missing)}')
    logging.debug(f'DKRZ MISSING: {len(dkrz_missing)}')
    logging.info(f'TOTAL MISSING: {len(missing_sets)}')

    final_results = result_set - missing_sets
    logging.debug(f'RESULT SET: {len(result_set)}')
    logging.debug(f'MISSING SET: {len(missing_sets)}')
    logging.debug(f'FINAL SET: {len(final_results)}')

    with open('../QC_Results/QC_passed_all_sites.txt', 'w+') as w:
        for ds in final_results:
            w.writelines(f'{ds}\n')


if __name__ == "__main__":
    main()