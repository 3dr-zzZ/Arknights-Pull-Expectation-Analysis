import random
import time

import pandas as pd

from banner import Banner
from special_banner import SpecialBanner
from limited_banner import LimitedBanner
from standard_banner import StandardBanner
from summary import summarize
from tqdm import trange


############### Basic Setup ###############
random.seed(123)
banner_types = ["SpecialBanner", "LimitedBanner", "StandardBanner"]  # 支持的卡池种类，请勿修改
banner_to_simulate = banner_types[0]  # 选择模拟的卡池

sample = 100000
n = 1  # number of main operators
m = 0  # number of peipao operators
###########################################


def export_to_csv(new_column: list, column_name: str, file_path: str = "sample_output.csv") -> None:
    """Add or create a column in an existing CSV file."""
    try:
        df = pd.read_csv(file_path)
        df[column_name] = new_column
    except FileNotFoundError:
        df = pd.DataFrame({column_name: new_column})

    df.to_csv(file_path, index=False)
    print(f"Column '{column_name}' exported to '{file_path}'")


def simulate(banner_type: str, num_sample: int, n_rate_up: int, m_rate_up: int = 0,
             to_csv: bool = False, file_path: str = "sample_output.csv") -> list:
    """Make simulations with banner_type banner, aim to get n_rate_up main
    operator(s) and m_rate_up peipao operator(s) if any. If sort = True, the
    result will be sorted in ascending order. When to_csv = True, results will
    be exported to file_path.
    """
    if banner_type not in banner_types:
        raise ValueError(f"Banner type {banner_type} does not exist.")
    if n_rate_up == 0 and m_rate_up == 0:
        raise ValueError("Does not apply: please get at least 1 "
                         "main/peipao operator.")

    # Initialize the banner.
    if banner_type == banner_types[0]:
        b = SpecialBanner()
        print(f"开始模拟「特殊寻访」，抽取「{n_rate_up}」个up干员，样本量：{num_sample}")
    elif banner_type == banner_types[1]:
        b = LimitedBanner()
        print(f"开始模拟「限定寻访」，抽取至少「{n_rate_up}」个限定干员、「{m_rate_up}」个陪跑干员，样本量：{num_sample}")
    elif banner_type == banner_types[2]:
        b = StandardBanner()
        print(f"开始模拟「标准寻访」，抽取至少「{n_rate_up}」个进店干员、「{m_rate_up}」个陪跑干员，样本量：{num_sample}")
    else:
        raise ValueError(f"模拟的卡池{b}不支持")

    # Simulate
    results = []
    t0 = time.time()
    for _ in trange(num_sample):
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
        export_to_csv(results, col_name, file_path)

    return results


if __name__ == '__main__':
    result = simulate(banner_type=banner_to_simulate, num_sample=sample,
                      n_rate_up=n, m_rate_up=m,
                      to_csv=True, file_path=f"simulations/{banner_to_simulate}.csv")

    print()
    n_pulls = 46
    # print(f"在所有样本中，{n_pulls}抽以内占：", find_percentile(result, n_pulls) * 100, "%")

    print("\n统计数据：")
    summarize(result)
    # plot_histogram(result)

    # for i in range(6):
    #     result = simulate(banner_types[1], sample, i+1, to_csv = False, file_path="limited_banner.csv")
    #     summarize(result)
