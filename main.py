import random
import pandas as pd
from banner import Banner
from special_banner import SpecialBanner
from limited_banner import LimitedBanner
from standard_banner import StandardBanner
from tqdm import trange

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

def simulate(banner_type: str, n_sample: int, n_rate_up: int, m_rate_up: int = 0,
             sort: bool = False, to_csv: bool = False, file_name: str = "output.csv") -> list:
    """Make simulations with banner_type banner, aim to get n_rate_up main
    operator(s) and m_rate_up peipao operator(s) if any. If sort = True, the
    result will be sorted in ascending order. When to_csv = True, results will
    be exported to file_name.
    """
    types = ["Special banner", "Limited banner", "Standard banner"]
    if banner_type not in types:
        raise ValueError(f"Banner type {banner_type} does not exist.")
    if n_rate_up == 0 and m_rate_up == 0:
        raise ValueError("Does not apply: please get at least 1 "
                         "main/peipao operator.")

    # Initialize the banner.
    if banner_type == "Special banner":
        b = SpecialBanner()
    elif banner_type == "Limited banner":
        b = LimitedBanner()
    elif banner_type == "Standard banner":
        b = StandardBanner()

    # Simulate
    results = []
    for _ in trange(n_sample):
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

    if sort:
        results.sort()

    # Export
    if to_csv:
        if isinstance(b, SpecialBanner):
            col_name = f'{type(b).__name__}({n_rate_up})'
        else:
            col_name = f'{type(b).__name__}({n_rate_up}+{m_rate_up})'
        print(col_name)
        export_to_csv(results, col_name, file_name)

    return results

if __name__ == '__main__':
    ############### Basic Setup ###############
    random.seed(123)
    banner_types = ["Special banner", "Limited banner", "Standard banner"]

    sample = 100000
    n = 1  # number of main operators
    m = 0  # number of peipao operators
    ###########################################

    result = simulate(banner_types[1], sample, n, m, sort = True)
    print(result)
