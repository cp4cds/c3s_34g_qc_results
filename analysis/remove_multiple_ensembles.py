#!/usr/bin/env Python

import os
import re
from copy import deepcopy
import logging

# SETTINGS
logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)
base = '/gws/nopw/j04/cp4cds1_vol3/c3s_34g/c3s_34g_qc_results/'
ifile = os.path.join(base, 'Catalogs/dataset_ids_release2_no-piControl-amip_202002.txt')


def set_max(variant, count):

    max_set = {variant: count}
    max_num = count
    max_variant = variant

    return max_set, max_num, max_variant


def main():

    # Input file is a list of CMIP6 dataset ids
    logging.info(f'Reading file {ifile}')
    with open(ifile) as r:
        dss = [line.strip() for line in r]

    # Generate a set of uniq experiments
    uniq_expts = set()
    [uniq_expts.add('.'.join(ds.split('.')[:5])) for ds in dss]
    logging.info(f'Number of uniq experiments {len(uniq_expts)}')

    variant_dict = {}
    for u_expt in list(uniq_expts):
      if u_expt == 'CMIP6.ScenarioMIP.MOHC.UKESM1-0-LL.ssp119':
        logging.info(f'Unique experiment {u_expt}')

        # For each unique experiment generate a set of unique variant ids
        variants = set()
        [variants.add(d.split('.')[5]) for d in dss if u_expt in d]

        variant_counts = []
        for v_id in variants:

            # For each variant id generate a dictionary
            #   keys: dataset id up to variant
            #   values: number of datasets within that combination
            ids = set()
            [ids.add(ds) for ds in dss if '.'.join([u_expt, v_id]) in ds]
            variant_counts.append({v_id: len(ids)})
            variant_dict[u_expt] = variant_counts
        logging.info(f'Variants dictionary {variant_dict}')

        # For each unique expt-variant determine the ensemble member that has the greatest number of datasets
        for u_ex, v_counts in variant_dict.items():
            max_set, max_num, max_variant = set_max(list(v_counts[0].keys())[0], 0)
            for _ in v_counts:
                max_set, max_num, max_variant = zip(*[set_max(variant, count) for variant, count in _.items()])

        main_ensemble = '.'.join([u_expt, list(max_variant)[0]])
        logging.info(f'{main_ensemble}')

        dsids = set()
        [dsids.add(ds) for ds in dss if main_ensemble in ds]
        [logging.debug(d) for d in dsids]

        logging.info('MAIN ENSEMBLE DEFINED')
        amon_uas = '.'.join([main_ensemble, 'Amon', 'uas.'])
        amon_vas = '.'.join([main_ensemble, 'Amon', 'vas.'])
        logging.debug(amon_uas)
        logging.debug(amon_vas)

        for _ in dsids:
            if re.search(amon_uas, _):
                print(f'uas present in dataset')

        new_ds = set()
        for ds in dsids:
            if amon_uas in ds:
                print(f'skipping uas')
            else:
                new_ds.add(ds)

        dsids = new_ds
        for _ in dsids:
            if re.search(amon_uas, _):
                print(f'uas still present :(')
        print('uas removed from ds')


        # dsids_passed = deepcopy(dsids)

        amon_uas_present = False
        amon_vas_present = False
        print(amon_uas_present, amon_vas_present)
        for _ in dsids:
            if re.search(amon_uas, _):
                amon_uas_present = True
            if re.search(amon_vas, _):
                amon_vas_present = True
        print(amon_uas_present, amon_vas_present)

        if (amon_uas_present and not amon_vas_present) or (amon_vas_present and not amon_uas_present):
            # dsids_passed.remove(ds)
            print('mismatch winds ', main_ensemble)
        else:
            print('surface winds ok')

        # if ('ua.' in dsids and 'va.' not in dsids) or ('va.' in dsids and 'ua.' not in dsids):
        #     # dsids_passed.remove(ds)
        #     print('mismatch winds ', main_ensemble)
        # else:
        #     print('Pressure level winds ok')


    #
    # for expt, vars in variant_dict.items():
    #     print(expt, vars)


if __name__ == "__main__":
    main()
