

# 1. Parse all the information into separate pandas DataFrames.
# 2. Rename the check result columns in each so that they are unique.
# 3. Do some consistency checking across them all - i.e. they should all have the same number of records (datasets and files)
# 4. Merge dataframes so that all results exist in separate columns

import pandas as pd
import os
import json
import gzip
import tarfile
from functools import reduce

qc_types = ['cfchecker', 'errata', 'nctime', 'prepare', 'ranges']


def load_file(filepath, q):

    # read in different file types and read json data


    # unzip
    if filepath.endswith('json.gz'):
        with gzip.open(filepath,'rt') as zipfile:
            data = json.load(zipfile)
        return data

    # un tar
    elif filepath.endswith('tgz') or filepath.endswith('tar.gz'):
        tar = tarfile.open(filepath, 'r:*')
        path = os.path.join('../',q)
        tar.extractall(path)
        json_file = tar.getnames()[0]
        json_file = os.path.join(path,json_file)
        tar.close()
        with open(json_file) as reader:
            data = json.load(reader)
        os.remove(json_file)
        return data
        #os.remove(json_file)
    else:
        with open(filepath) as reader:
            data = json.load(reader) 
              
        return data

def form_df(data):

    headers = ["pid", "dset_id", "dset_qc_status", "dset_error_severity", "dset_error_message"]

    records = []
    
    for handle, record in data['datasets'].items():
        
        records.append([handle,record["dset_id"],record["dset_qc_status"],record["dset_error_severity"],record["dset_error_message"]])
        
    df = pd.DataFrame(records, columns=headers)
    return df
        
def rename_field(df, qc_type):
    df.rename(columns={"dset_qc_status":f"{qc_type}_dset_qc_status","dset_error_severity":f"{qc_type}_dset_error_severity","dset_error_message":f"{qc_type}_dset_error_message"},inplace=True,errors='raise')
                                    #,'file_qc_status':f'{qc_type}_file_qc_status','file_error_severity':f'{qc_type}_file_error_severity',
                                    #'file_error_severity':f'{qc_type}_file_error_severity' }, inplace=True)
    return df


#def merge_df():


def main():

    data_frames = []

    for q in qc_types:

        QC_DIR = f'../{q}'

        for f in os.listdir(QC_DIR):

            if f.startswith('QC'):

                fpath = os.path.join(QC_DIR,f)
                print(f'reading in {fpath}')
                
                data = load_file(fpath, q) # unzip and untar files and extract data
                
                df = form_df(data) # get items we want and create pandas df

                #print(df.info)

 
                print(f'renaming fields in {q} dataframe')
                df_renamed = rename_field(df,q)

                #print(df_renamed.info())
                
                if not len(df_renamed.dset_id.unique()) == 14570:
                    raise ValueError('This dataframe does not contain the right number of datasets')
                #if not len(df_renamed) == 104590:
                    #raise ValueError('This dataframe does not contain the right number of files')
    

        data_frames.append(df_renamed)
    print(data_frames)
    
    main_df = reduce(lambda left,right: pd.merge(left,right,on=['pid','dset_id'], how='outer'), data_frames)  # add the new unique columns into one df with the same amount of rows
    
    pd.DataFrame.to_csv(main_df, 'qc-checked_all-sites_15-10-21.csv', sep=',',index=False)
       
               

    

if __name__ == "__main__":
    main()





