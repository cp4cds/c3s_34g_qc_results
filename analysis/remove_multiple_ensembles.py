#!/usr/bin/env Python

import os
import re

base = '/gws/nopw/j04/cp4cds1_vol3/c3s_34g/c3s_34g_qc_results/'
ifile = os.path.join(base, 'Catalogs/dataset_ids_release2_no-piControl-amip_202002.txt')

def main():

    with open(ifile) as r:
        dss = [line.strip() for line in r]

    uexpts = set()
    [uexpts.add('.'.join(ds.split('.')[:5])) for ds in dss]

    uens = set()
    [uens.add('.'.join(ds.split('.')[:6])) for ds in dss]

    ens_dict = {}
    for uex in uexpts:
        variants = set()
        [variants.add(d.split('.')[5]) for d in dss if uex in d]
        v_list = []

        for v in variants:
            ids = set()
            for ds in dss:
                if '.'.join([uex, v]) in ds:
                    ids.add(ds)

            v_list.append({v: len(ids)})
            ens_dict[uex] = v_list

        for k, v in ens_dict.items():
            max_num = 0
            max_set = {}
            for x in v:
                for var, num in x.items():
                  if num > max_num:
                    max_set[var] = num
                    max_num = num
                    max_id = var

        max_ens = '.'.join([uex, max_id])
        dsids = set()
        for ds in dss:
            if max_ens in ds:
                dsids.add(ds)

        u_and_v = False
        for ds in dsids:
            if 'uas' in ds:
                for d in dsids:
                    if 'vas' in d:
                        u_and_v = True
            if not u_and_v:
                if 'vas' in ds:
                    for d in dsids:
                        if 'uas' in d:
                            u_and_v = True

        if not u_and_v:
            print('mismatch winds ', max_ens)
    for expt, vars in ens_dict.items():
        print(expt, vars)


if __name__ == "__main__":
    main()