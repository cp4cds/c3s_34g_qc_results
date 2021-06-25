#!/usr/bin/env python


import json


missing = open("MISSING_IN_R3.txt").read().strip().split()

"""
==> incomplete_dset_at_ipsl.txt <==
CMIP6.CMIP.CAS.CAS-ESM2-0.historical.r1i1p1f1.Amon.hur.gn.v20200502
CMIP6.CMIP.CAS.CAS-ESM2-0.historical.r1i1p1f1.Amon.hus.gn.v20200502

==> inconsistent_winds_datasets.txt <==
CMIP6.ScenarioMIP.MOHC.HadGEM3-GC31-LL.ssp245.r1i1p1f3.Amon.va.gn.v20190908
CMIP6.ScenarioMIP.KIOST.KIOST-ESM.ssp585.r1i1p1f1.Amon.vas.gr1.v20191106

==> missing_at_ceda.txt <==
CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.fx.sftlf.gr1.v20190726
CMIP6.CMIP.NOAA-GFDL.GFDL-CM4.historical.r1i1p1f1.Ofx.deptho.gr.v20180701

==> missing_at_dkrz.txt <==
/mnt/lustre02/work/ik1017/CMIP6/data/CMIP6/AerChemMIP/BCC/BCC-ESM1/ssp370/r1i1p1f1/Ofx/basin/gn/v20201021
/mnt/lustre02/work/ik1017/CMIP6/data/CMIP6/CMIP/CAS/FGOALS-g3/historical/r1i1p1f1/SImon/siconc/gn/v20210108

==> missing_at_ipsl.txt <==
CMIP6.CMIP.CAS.CAS-ESM2-0.historical.r1i1p1f1.Amon.hur.gn.v20200502
CMIP6.CMIP.CAS.CAS-ESM2-0.historical.r1i1p1f1.Amon.hus.gn.v20200502

==> missing_dset_at_ipsl.txt <==
CMIP6.CMIP.EC-Earth-Consortium.EC-Earth3-Veg.historical.r12i1p1f1.Ofx.basin.gr.v20200925
CMIP6.ScenarioMIP.EC-Earth-Consortium.EC-Earth3.ssp126.r6i1p1f1.Ofx.basin.gn.v20200201

"""


def parse_json(fname):
    with open(fname) as reader:
       return json.load(reader)


def filter_out(tag, m):
    tag_map = {
"incomplete_ipsl": "incomplete_dset_at_ipsl.txt",
"inconsistent_winds": "inconsistent_winds_datasets.txt",
"missing_ceda": "missing_at_ceda.txt",
"missing_dkrz": "missing_at_dkrz.txt",
"missing_ipsl": ("missing_at_ipsl.txt", "missing_dset_at_ipsl.txt"),
"missing_34e_scan": "34e_FAILS_UNIQUE.txt"
}

    files = tag_map[tag]
    if isinstance(files, str):
        files = (files,)

    print(f"Removing due to: {tag}")
    items = []
    for fname in files:
        items.extend(open(f"../{fname}").read().strip().replace("/mnt/lustre02/work/ik1017/", "").replace("/", ".").split())

    r_count = 0

    for item in items:
        if item in m:
            m.remove(item) 
            r_count += 1

    print(f"\tRemoved: {r_count}\n")
    return r_count


def remove_with(tag, m):
    print(f"Removing due to errors with: {tag}")
    json_path = f"QC_{tag}.json"
    data = parse_json(json_path)
    r_count = 0

    for hdl, result in data['datasets'].items():
        status = result['dset_qc_status']
        dset_id = result["dset_id"]

        if status.lower() == 'fail' and dset_id in m:
            print(dset_id)
            m.remove(dset_id)
            r_count += 1

    print(f"\tRemoved: {r_count}\n")
    return r_count


def main():
    m = set(missing)

    checks = ("cfchecker", "errata", "handle", "nctime", "prepare", "ranges")

    for check in checks:
        remove_with(check, m)

    tags = ("incomplete_ipsl", "inconsistent_winds", "missing_ceda", "missing_dkrz", 
            "missing_ipsl", "missing_34e_scan")

    for tag in tags:
        filter_out(tag, m)

    print(f"All done: remaining dsets: {len(m)}")
    unresolved_file = 'UNRESOLVED_MISSING.txt'

    with open(unresolved_file, 'w') as w:
        w.write("\n".join(sorted(m)))

    print(f"Wrote: {unresolved_file}")


if __name__ == "__main__":

    main()
