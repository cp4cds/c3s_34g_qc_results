#!/usr/bin/env Python

import os
import re
from copy import deepcopy
import logging

# SETTINGS
logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)
base = '/gws/nopw/j04/cp4cds1_vol3/c3s_34g/c3s_34g_qc_results/'
ifile = os.path.join(base, 'QC_Results/QC_passed_dataset_ids_2021-02-25.txt')
ofile = os.path.join(base, 'QC_Results/QC_passed_dataset_ids_2021-03-09.txt')
if os.path.exists(ofile):
    os.remove(ofile)
# def set_max(variant, count):
#
#     max_set = {variant: count}
#     max_num = count
#     max_variant = variant
#
#     return max_set, max_num, max_variant


def main():

    # Input file is a list of CMIP6 dataset ids
    logging.debug(f'Reading file {ifile}')
    with open(ifile) as r:
        dss = [line.strip() for line in r]

    # Generate a set of uniq experiments
    uniq_models = set()
    [uniq_models.add('.'.join(ds.split('.')[2:4]).strip("'")+'.') for ds in dss]
    logging.debug(f'Number of uniq models {len(uniq_models)}')

    expts_dict = {}
    for model in list(uniq_models):
        # # TEST for winds uniq experiment:
        # if u_expt == 'CMIP6.ScenarioMIP.CCCma.CanESM5-CanOE.ssp245':

        logging.debug(f'Unique experiment {model}')

        # For each unique experiment generate a set of unique variant ids
        experiments = set()
        [experiments.add(d.split('.')[4].strip("'")) for d in dss if model in d]
        # for d in dss:
        #     if model in d:
        #         experiments.add(d.split('.')[4].strip("'"))
        if 'historical' not in experiments:
            print(f'skipping {model}')
        expts_dict[model] = experiments

        with open(ofile, 'a+') as w:

            for d in dss:
                if model in d:
                    if 'historical' not in expts_dict[model]:
                        logging.info(f'skipping {model}')
                        logging.debug(f'skipping {d}')
                    else:
                        w.writelines(f'{d}\n')


#         print(expts_dict)
#         ads
#         variant_counts = []
#         for v_id in variants:
#
#             # For each variant id generate a dictionary
#             #   keys: dataset id up to variant
#             #   values: number of datasets within that combination
#             ids = set()
#             [ids.add(ds) for ds in dss if '.'.join([u_expt, v_id]) in ds]
#             variant_counts.append({v_id: len(ids)})
#             variant_dict[u_expt] = variant_counts
#
#         logging.debug(f'Variants dictionary {variant_dict}')
#
#         # For each unique expt-variant determine the ensemble member that has the greatest number of datasets
#         max_num = 0
#         max_variant = False
#         for exp_id, variant_dict_list in variant_dict.items():
#             for v_dict in variant_dict_list:
#                 for variant, variant_count in v_dict.items():
#                     if variant_count > max_num:
#                         max_variant = variant
#
#         main_ensemble = '.'.join([u_expt, max_variant])
#
#         logging.debug(f'{main_ensemble}')
#
#         dsids = set()
#         [dsids.add(ds.strip("'")) for ds in dss if main_ensemble in ds]
#         [logging.debug(d) for d in dsids]
#         logging.debug(f'LEN dataset ids {len(dsids)}')
#
#         logging.debug(f'Datasets defined for main ensemble {len(dsids)}')
#
#         ds_to_remove = resovle_wind_inconsisencies(dsids, main_ensemble)
#         for _ in ds_to_remove:
#             with open(os.path.join(base, 'QC_Results', 'inconsistent_winds_datasets.txt'), 'a+') as w:
#                 w.writelines(f'{_}\n')
#             dsids.remove(_)
#             logging.debug(f'REMOVED INCONSISENT WIND {_}')
#         logging.debug(f'LEN datasets {len(dsids)}')
#
#         with open(os.path.join(base, 'QC_Results', 'QC_passed_consistent_datasets.txt'), 'a+') as wh:
#             for valid_dataset in dsids:
#                 wh.writelines(f'{valid_dataset}\n')
#
#
# def resovle_wind_inconsisencies(dsids, main_ensemble):
#
#     wind_components = ['uas.', 'vas.', 'ua.', 'va.']
#     winds = {}
#     for component in wind_components:
#         winds[component.strip('.')] = '.'.join([main_ensemble, 'Amon', component]).strip("'")
#     logging.debug(f'winds dict: {winds}')
#
#     amon_uas_present, amon_vas_present, amon_ua_present, amon_va_present = False, False, False, False
#
#     for _ in dsids:
#         # _search = re.compile(r'(%s)\.'%winds[uas])
#         if re.match(winds['uas'] + 'g', _):
#             amon_uas_present = True
#         if re.match(winds['vas'] + 'g', _):
#             amon_vas_present = True
#         if re.match(winds['ua'] + 'g', _):
#             amon_ua_present = True
#         if re.match(winds['va'] + 'g', _):
#             amon_va_present = True
#
#     to_remove = []
#
#     if amon_uas_present and not amon_vas_present:
#         [to_remove.append(_) for _ in dsids if re.match(winds['uas'] + 'g', _)]
#
#     if amon_vas_present and not amon_uas_present:
#         [to_remove.append(_) for _ in dsids if re.match(winds['vas'] + 'g', _)]
#
#     if amon_ua_present and not amon_va_present:
#         [to_remove.append(_) for _ in dsids if re.match(winds['ua'] + 'g', _)]
#
#     if amon_va_present and not amon_ua_present:
#         [to_remove.append(_) for _ in dsids if re.match(winds['va'] + 'g', _)]
#
#     return to_remove


if __name__ == "__main__":
    main()
