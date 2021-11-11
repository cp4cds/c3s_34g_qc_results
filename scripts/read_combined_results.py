import sys
import pandas as pd

qc_types = ['cfchecker', 'errata', 'nctime', 'prepare', 'ranges']


known_issues = {
    "r4": {
         "nctime": {"365_day calendar in CMCC model (is allowed)": 1830,
                    "Other reasons - allowed by IPSL re-check": 164},
         "prepare": {"further_info_url incorrect (but can be fixed)": 3444}
    }
}


def truncate(arr, length):
    res = []

    for i in arr:
        i = str(i)
        if len(i) > length:
            i = f"{i[:length]}..."

        res.append(i)

    return res


def analyse(df, release):
    """
    Read results and provide some annotated outputs to stdout.
    Returns a new DataFrame of only the data that we want to publish
    in this release.
    """
    initial_count = len(df)
    print(f"[INFO] Number of datasets: {initial_count}")

    dsids_to_exclude = []

    for qc_type in qc_types:
        print(f"\n[INFO] Working on: {qc_type}")
        issues = known_issues.get(release, {}).get(qc_type, {})

        cols = [col for col in df.columns if qc_type in col]
        for col in cols:
            unique_values = sorted([_ for _ in list(df[col].unique()) if str(_) != "nan"])
            print(col, truncate(unique_values, 10))

        status_col = f"{qc_type}_dset_qc_status"
        if len(df[df[status_col] == "pass"]) == initial_count:
            print("[SUCCESS] All passed!") 

        else:
            bad = df[df[status_col] != "pass"]
            unaccounted_for = len(bad) - sum(issues.values())

            if unaccounted_for == 0:
                print(f"[SUCCESS] we found failures - but they are known/fixable issues in: {issues}")

            else:
                print(f"[ERROR] {unaccounted_for} of {initial_count} failed.") 
                dsids_to_exclude.extend(sorted(bad["dset_id"].unique()))

    exclude_count = len(dsids_to_exclude)
    final_count = initial_count - exclude_count 
    print("\n[INFO] Final results.")
    print(f"- initial count: {initial_count}\n- excluded:        {exclude_count}\n- final count:   {final_count}\n")

    return df[~df["dset_id"].isin(dsids_to_exclude)]


def write_final_file(df, release):
    "Writes filtered release file."
    final_file = f"releases/{release}/final/{release}_final.txt"
    dset_ids = sorted(df.dset_id)

    with open(final_file, "w") as writer: 
        writer.write("\n".join(dset_ids) + "\n")

    print(f"[INFO] Wrote: {final_file}")


def main():
    release = sys.argv[1]
    csv_file = f"releases/{release}/combined/combined_results.csv.gz"

    df = pd.read_csv(csv_file)
    df_filtered = analyse(df, release)

    write_final_file(df_filtered, release)
    return df


if __name__ == "__main__":

    df = main()
