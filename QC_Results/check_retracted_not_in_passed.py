#!/usr/bin/env Python
import os

RETACTED_DATASETS = "datasets_cp4cds_retracted_20210131.txt"

retracted = []
with open(RETACTED_DATASETS) as r:
    for line in r:
        id, versions = line.split(',')[0].strip(), line.split(',')[1:]
        for v in versions:
            if v.startswith('2'):
                retracted.append('.'.join([id, 'v'+ v]).strip())

ERROR_DATASETS = 'datasets_cp4cds_error_20210131.txt'

with open(ERROR_DATASETS) as r:
    error_ds = [line.strip() for line in r]


with open('QC_passed_all_sites.txt') as r:
    passed_ds = [line.strip() for line in r]

for ds_ok in passed_ds:
    if ds_ok in error_ds:
        print(f"CATASTROPE {ds_ok}")