import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


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


def summarize_results(input_file: str = "sample_output.csv", output_file: str = "sample_summary.csv") -> None:
    """Summarize each simulation column in input_file and save result as rows in output_file."""
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        return

    summary_data = {}

    for col in df.columns:
        stats = summarize(df[col].dropna().tolist())
        summary_data[col] = stats

    summary_df = pd.DataFrame.from_dict(summary_data, orient="index")
    summary_df.index.name = "simulation"
    summary_df.to_csv(output_file)
    print(f"Summary exported to '{output_file}'")


if __name__ == "__main__":
    summarize_results(input_file="sample_output.csv", output_file="sample_summary.csv")
