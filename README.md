# c3s_34g_qc_results

Once all the QC result json files have been added to `releases/r<n>/<QC-check-name>/`, the results can be combined into one pandas dataframe using the following script:
  
 `cd releases/r4/initial/`
  
 `python combine_result.py`
  
Note - this will produce a csv file in the same directory and the filename is currently hard coded
  
  
For the final data delivery report to C3S the following statistics are required:
  
  - The number of failed datasets for each QC test and the Failure rate (fail/total)
  - The number of missing datasets (not able to replicate)
  - The number of datasets that passed for each experiment, the total number for each experiment and the availability rate (pass/total)
  - The number of datasets that passed for each variable, the total number for each variable and the availability rate (pass/total)
  - The number of datasets that passed for each model, the total number for each model and the availability rate (pass/total)
