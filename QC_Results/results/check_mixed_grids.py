import json


qc_recs = "QC_cfchecker.json"


def check_records(fname=qc_recs):

    print(f"Checking file: {qc_recs}")

    with open(fname) as reader:
        data = json.load(reader)

    mismatches = {}
    notlists = []

    for hdl, result in data['datasets'].items():

        dset_id = result["dset_id"]
        dset_grid = dset_id.split('.')[8]
        

        for content in result['files'].values():
            
            filename = content["filename"] 
            file_grid = filename.split('_')[5].split('.')[0]

            if dset_grid != file_grid:
                mismatches.setdefault(dset_id, [])
                mismatches[dset_id].append(filename)
                print(f"MISMATCH: {dset_id} :: {filename} :: {dset_grid} != {file_grid}")


    print("\n\nRESULTS:")
    print(f"\tFound in {len(mismatches)} datasets.")
    print(f"\tJSON content incorrect for {len(notlists)} datasets.")


if __name__ == '__main__':

    check_records()
