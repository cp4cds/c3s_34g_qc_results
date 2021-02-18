#!/usr/bin/env Python

import os
import re
from copy import deepcopy

base = '/gws/nopw/j04/cp4cds1_vol3/c3s_34g/c3s_34g_qc_results/'
ifile = os.path.join(base, 'Catalogs/dataset_ids_release2_no-piControl-amip_202002.txt')


def set_max(variant, count):

    max_set = {variant: count}
    max_num = count
    max_variant = variant

    return max_set, max_num, max_variant


def main():

    # Input file is a list of CMIP6 dataset ids
    with open(ifile) as r:
        dss = [line.strip() for line in r]

    # Generate a set of uniq experiments
    uniq_expts = set()
    [uniq_expts.add('.'.join(ds.split('.')[:5])) for ds in dss]


    variant_dict = {}
    for u_expt in uniq_expts:

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

        # For each unique expt-variant determine the ensemble member that has the greatest number of datasets
        for u_ex, v_counts in variant_dict.items():
            max_set, max_num, max_variant = set_max(list(v_counts[0].keys())[0], 0)
            for _ in v_counts:
                max_set, max_num, max_variant = zip(*[set_max(variant, count) for variant, count in _.items()])
        main_ensemble = '.'.join([u_expt, max_variant])

        dsids = set()
        [dsids.add(ds) for ds in dss if main_ensemble in ds]

        dsids_passed = deepcopy(dsids)
        for ds in dsids:
            if ('uas' in ds and 'vas' not in ds) or ('vas' in ds and 'uas' not in ds):
                dsids_passed.remove(ds)
                print('mismatch winds ', main_ensemble)

    for expt, vars in variant_dict.items():
        print(expt, vars)


if __name__ == "__main__":
    main()
