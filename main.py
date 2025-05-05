import random
import pandas as pd
from banner import Banner
from special_banner import SpecialBanner
from limited_banner import LimitedBanner

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
    # Basic setup
    random.seed(123)
    n_sample = 10000  # number of samples
    n_rate_up = 1  # the number of rate-up operators from each sample.
    m_rate_up = 1  # if there are two rate-up operators.
    # Choose the banner:
    b = LimitedBanner()

    # Simulate
    results = []
    for _ in range(n_sample):
        if isinstance(b, SpecialBanner):
            results.append(b.pull_n_desired(n_rate_up)[-1])
        else:
            results.append(max(b.pull_desired(n_rate_up, m_rate_up)[0][-1],
                               b.pull_desired(n_rate_up, m_rate_up)[1][-1]))
        b.reset()
    print(results)

    # Export
    col_name = 'Limited Banner: 1+1'
    export_to_csv(results, col_name)
