

# 1. Parse all the information into separate pandas DataFrames.
# 2. Rename the check result columns in each so that they are unique.
# 3. Do some consistency checking across them all - i.e. they should all have the same number of records (datasets and files)
# 4. Merge dataframes so that all results exist in separate columns

import pandas as pd
import sys
import os
import json
import glob
import gzip
import tarfile
import zipfile

from functools import reduce

qc_types = ['cfchecker', 'errata', 'nctime', 'prepare', 'ranges']

EXPECTED_DS_COUNTS = {
    "r3": 13794,
    "r4": 14570
}


def load_file(filepath, qc_type):
    """
    Read the file path in, depending on the qc_type and the file type.
    Return the data as a dictionary (from the JSON content).
    """

    # gunzip
    if filepath.endswith('json.gz'):
        with gzip.open(filepath,'rt') as gzipfile:
            data = json.load(gzipfile)

    # untar
    elif filepath.endswith('tgz') or filepath.endswith('tar.gz'):
        tar = tarfile.open(filepath, 'r:*')
        path = os.path.join('../', qc_type)
        tar.extractall(path)
        json_file = tar.getnames()[0]
        json_file = os.path.join(path,json_file)
        tar.close()

        with open(json_file) as reader:
            data = json.load(reader)

        os.remove(json_file)

    # unzip
    elif filepath.endswith("zip"):
        with zipfile.ZipFile(filepath, 'r') as z:
            filename = z.namelist()[0]

            with z.open(filename) as reader:
                content = reader.read()
                data = json.loads(content)

    else:
        with open(filepath) as reader:
            data = json.load(reader) 
              
    return data


def create_dataframe(data):
    """
    Builds a DataFrame from a dictionary and returns it.
    """
    headers = ["pid", "dset_id", "dset_qc_status", "dset_error_severity", "dset_error_message"]
    records = []
    
    for handle, record in data['datasets'].items():
        
        records.append([handle, record["dset_id"], record["dset_qc_status"], record["dset_error_severity"], 
                        record["dset_error_message"]])
        
    return pd.DataFrame(records, columns=headers)
        

def rename_qc_fields(df, qc_type):
    "Rename the qc field by qc_type. Changes DataFrame in place."
    renamers = {
        "dset_qc_status": f"{qc_type}_dset_qc_status",
        "dset_error_severity": f"{qc_type}_dset_error_severity",
        "dset_error_message": f"{qc_type}_dset_error_message"
    }

    df.rename(columns=renamers, inplace=True, errors='raise')
#    df.rename(columns={"dset_qc_status":f"{qc_type}_dset_qc_status","dset_error_severity":f"{qc_type}_dset_error_severity","dset_error_message":f"{qc_type}_dset_error_message"},inplace=True,errors='raise')


def main():
    """
    Read in all the results from each qc_type, 
    """
    release = sys.argv[1]
    data_frames = []

    for qc_type in qc_types:

        print(f"[INFO] Processing: {qc_type}")
        QC_DIR = f'releases/{release}/{qc_type}'

        qc_results = glob.glob(f"releases/{release}/{qc_type}/QC*")
        if len(qc_results) != 1:
            raise Exception(f"Wrong number found: {qc_results}")        
        
        qc_results_file = qc_results[0]
        data = load_file(qc_results_file, qc_type)
        df = create_dataframe(data)

        print(f"[INFO] Renaming fields in {qc_type} dataframe")
        rename_qc_fields(df, qc_type)
        print(f"[INFO] Columns are now: {list(df.columns)}")

        exp_count = EXPECTED_DS_COUNTS[release]

        if not len(df.dset_id.unique()) == exp_count:
            raise ValueError(f"{qc_type} does not have expected ds count: "
                             f"{len(df.dset_id.unique())} != {exp_count}")

        data_frames.append(df)

    print("[INFO] Compiled data frames.") 

    # Combine into single data frame
    print("[INFO] Combining...")  
    main_df = reduce(lambda left, right: pd.merge(left, right, on=['pid', 'dset_id'], how='outer'), data_frames)
    
    output_path = f"releases/{release}/combined/combined_results.csv.gz"
    main_df.to_csv(output_path, sep=',',index=False)
    print(f"[INFO] Columns in merged df are: {list(main_df.columns)}")
    print(f"[INFO] Wrote: {output_path}")
       

if __name__ == "__main__":

    main()

