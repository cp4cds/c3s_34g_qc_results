# Testing

Create dir and unzip all files:

```
mkdir results
cp QC_cfchecker.json QC_handle.json QC_errata.tar.gz  QC_nctime.tgz  QC_prepare.json.zip  QC_ranges.json.gz  QC_template.gz results/

cd results/

$ gunzip QC_ranges.json.gz
$ gunzip QC_template.gz

$ unzip QC_prepare.json.zip
Archive:  QC_prepare.json.zip
  inflating: c3s_34g_qc_results/QC_Results/c34results_files_apr21.json

$ mv c3s_34g_qc_results/QC_Results/c34results_files_apr21.json QC_prepare.json
$ rmdir -fr c3s_34g_qc_results
$ gunzip QC_errata.tar.gz

$ tar xvf QC_errata.tar
QC_errata.json

$ tar xzvf QC_nctime.tgz
QC_nctime.json

NOTE!!! I manually removed the first and last lines of: QC_template.json
```

Now we have:
```
QC_cfchecker.json
QC_errata.json
QC_handle.json
QC_nctime.json
QC_prepare.json
QC_ranges.json
QC_template.json
```

Compile all missing results:

```
$ head -3 MISSING_IN_R3.txt
CMIP6.ScenarioMIP.CCCma.CanESM5.ssp370.r1i1p1f1.Amon.rlut.gn.v20190429
CMIP6.ScenarioMIP.CAMS.CAMS-CSM1-0.ssp370.r1i1p1f1.Amon.pr.gn.v20190708
CMIP6.CMIP.BCC.BCC-CSM2-MR.historical.r1i1p1f1.LImon.snd.gn.v20181114
$ wc -l MISSING_IN_R3.txt
481 MISSING_IN_R3.txt
```


