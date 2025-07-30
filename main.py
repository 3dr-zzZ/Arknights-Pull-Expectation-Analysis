import random
import pandas as pd
from banner import Banner
from special_banner import SpecialBanner
from limited_banner import LimitedBanner
from standard_banner import StandardBanner


def export_to_csv(new_column: list, column_name: str, file_name: str = "output.csv") -> None:
    """Add or create a column in an existing CSV file."""
    try:
        df = pd.read_csv(file_name)
        df[column_name] = new_column
    except FileNotFoundError:
        df = pd.DataFrame({column_name: new_column})

    df.to_csv(file_name, index=False)
    print(f"Column '{column_name}' exported to '{file_name}'")


def convert_gap_records(l: list) -> list:
    """Output records based on the pulls used between the occurance of each
    six-star gained.
    """
    if not l:
        return []

    cur_pull = 0
    records_gap = []
    for pull_cnt in l:
        records_gap.append(pull_cnt - cur_pull)
        cur_pull = pull_cnt
    return records_gap

if __name__ == '__main__':
    ############### Basic Setup ###############
    random.seed(123)
    n_sample = 10000  # number of samples

    ### Choose Banner & Num of Character(s) ###
    b = StandardBanner()
    n_rate_up = 1  # num of rate-up operators from each sample.
    m_rate_up = 0  # num of second character if two rate-up operators.
    if n_rate_up == 0 and m_rate_up == 0:
        print("Does not apply: please get at least 1 main/peipao operator.")

    # Simulate
    results = []
    for _ in range(n_sample):
        if isinstance(b, SpecialBanner):
            results.append(b.pull_n_desired(n_rate_up)[-1])
        else:
            pulls = b.pull_desired(n_rate_up, m_rate_up)
            if m_rate_up > 0 and n_rate_up > 0:
                results.append(max(pulls[0][-1], pulls[1][-1]))
            elif n_rate_up > 0:
                results.append(pulls[0][-1])
            elif m_rate_up > 0:
                results.append(pulls[1][-1])
        b.reset()
    print(results)

    # Export
    if isinstance(b, SpecialBanner):
        col_name = f'{type(b).__name__}({n_rate_up})'
    else:
        col_name = f'{type(b).__name__}({n_rate_up}+{m_rate_up})'
    print(col_name)
    export_to_csv(results, col_name)
