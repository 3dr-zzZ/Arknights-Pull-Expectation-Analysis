import random
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


def summarize(input_list: list[int]) -> dict:
    """Given an input_list, output its min, max, mean, median, and key percentiles as rounded integers."""
    data = np.array(input_list)
    rslt = {
        "min": round(np.min(data)),
        "max": round(np.max(data)),
        "mean": round(np.mean(data)),
        "median": round(np.median(data)),
        "p10": round(np.percentile(data, 10)),
        "p25": round(np.percentile(data, 25)),
        "p75": round(np.percentile(data, 75)),
        "p90": round(np.percentile(data, 90))
    }

    for key, value in rslt.items():
        print(f"{key}: {value}")
    return rslt


def plot_histogram(input_list: list[int]) -> None:
    """Create a histogram about input_list.
    """
    plt.hist(input_list, bins = 30)
    plt.xlabel("Number of pulls")
    plt.ylabel("Count")
    plt.show()


def find_percentile(input_list: list[int], n: int) -> float:
    """Find the percentile of n in input_list."""
    cnt = 0
    for item in input_list:
        if item < n:
            cnt += 1
    return cnt / len(input_list)


def simulate(banner_type: str, n_sample: int, n_rate_up: int, m_rate_up: int = 0,
             to_csv: bool = False, file_name: str = "output.csv") -> list:
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
        print(f"开始模拟「特殊寻访」，抽取「{n_rate_up}」个up干员，样本量：{n_sample}")
    elif banner_type == "Limited banner":
        b = LimitedBanner()
        print(f"开始模拟「限定寻访」，抽取至少「{n_rate_up}」个限定干员、「{m_rate_up}」个陪跑干员，样本量：{n_sample}")
    elif banner_type == "Standard banner":
        b = StandardBanner()
        print(f"开始模拟「标准寻访」，抽取至少「{n_rate_up}」个进店干员、「{m_rate_up}」个陪跑干员，样本量：{n_sample}")

    # Simulate
    results = []
    t0 = time.time()
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
    print(f"模拟完成，耗时：{round(time.time() - t0, 2)}s")

    # Export
    if to_csv:
        if isinstance(b, SpecialBanner):
            col_name = f'{type(b).__name__}: {n_rate_up}'
        else:
            col_name = f'{type(b).__name__}: {n_rate_up}+{m_rate_up}'
        print(col_name)
        export_to_csv(results, col_name, file_name)

    return results

if __name__ == '__main__':
    ############### Basic Setup ###############
    random.seed(123)
    banner_types = ["Special banner", "Limited banner", "Standard banner"]

    sample = 100000
    n = 6  # number of main operators
    m = 0  # number of peipao operators
    ###########################################

    result = simulate(banner_types[0], sample, n, m)

    print()
    n_pulls = 46
    # print(f"在所有样本中，{n_pulls}抽以内占：", find_percentile(result, n_pulls) * 100, "%")

    print("\n统计数据：")
    summarize(result)
    # plot_histogram(result)

    # for i in range(6):
    #     result = simulate(banner_types[1], sample, i+1, to_csv = False, file_name="limited_banner.csv")
    #     summarize(result)
