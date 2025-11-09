"""
---------------------------------------------------------------------------------

    - Adriana Rodríguez Flórez
    - adrirflorez@gmail.com
    - Course: NTIN066 Data Structures
    - Homework 7, MATRIX EXPERIMENT
    - Version: ÚFAL 24/25; April 2025 

---------------------------------------------------------------------------------
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# params: student number (UKČO), and tree construction to test
STUDENT_ID = "17957513"
CONFIGS = ["m1024-b16", "m8192-b64", "m65536-b256", "m65536-b4096"]
TESTS = ["naive", "smart"]

# results: .csv format
RESULTS_FILE = "./matrix_results.csv"
CSV_COLS = ["Cache_Config", "Impl", "N", "Misses_Per_Item"]

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------

def plot(df, config):
    """
    For a given test, plot its results saved onto a CSV file.
    
    Parameters
    ----------
    config : str
        name of the cache config to plot results for
    """
    plt.figure(figsize=(10, 6))
    title = f"[{config}] Avg. Cache Misses per Transposed Item"
    x_label = "Matrix size (N)"
    y_label = "Avg. Misses per Item"

    for t in TESTS:
        label = "Trivial" if t == "naive" else "Cache-Oblivious"
        data = df[(df["Cache_Config"] == config) & (df["Impl"] == t)]
        if not data.empty:
            plt.plot(data["N"], data["Misses_Per_Item"], marker="o", label=label)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xscale("log", base=2)
    
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.subplots_adjust(bottom=0.15)
    plt.figtext(
        0.5, 0.02, 
        "Logarithmic scale used for X axis.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.legend()
    
    filename = f"./plots/{config.replace('-', '_')}_plot.png"
    plt.savefig(filename)
    plt.show()
    print(f"📊 Saved comparative plot: {filename}")

def plot_separately(df, config):
    """
    Plot a single experimental curve along with theoretical curves of complexities:
    O(1), O(n) and O(log n).

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the results
    config : str
        cache configuration
    """
    plt.figure(figsize=(10, 6))
    title = f"[{config}] Cache Misses per Item (Cache-Oblivious 'smart' impl.)"
    x_label = "Matrix size (N)"
    y_label = "Avg. Misses per Item"

    # compare my impl. vs the asymptotic trend
    data = df[(df["Cache_Config"] == config) & (df["Impl"] == "smart")]
    if data.empty:
        print(f"⚠️ No data found for the cache-oblivious impl. on {config}")
        return

    label = "Cache-Oblivious"
    plt.plot(data["N"], data["Misses_Per_Item"], marker="o", label=label)

    n_values = np.array(sorted(data["N"].unique()))
    c_factor = 1e-4 

    plt.plot(n_values, np.ones_like(n_values), 'r--', label="O(1) - Constant Time")
    plt.plot(n_values, c_factor * n_values, 'g--', label="O(n) - Linear Time")
    plt.plot(n_values, c_factor * np.log2(n_values), 'b--', label="O(log n) - Logarithmic Time")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)

    # Add a text box for the figure description
    plt.figtext(0.5, 0.02, "Theoretical trend lines added: O(1), O(log n), O(n).", ha="center", fontsize=9, color="gray")
    
    # Save the figure
    filename = f"./plots/{config.replace('-', '_')}_asymptotics.png"
    plt.savefig(filename)
    plt.show()
    print(f"📈 Saved asymptotic comparison plot: {filename}")



# ---------------------------------------------------------------------------------

def main():

    # plotting the results of each test
    df = pd.read_csv(RESULTS_FILE)

    print("\n\n🔜 Plotting results...")
    for config in CONFIGS:
        plot(df, config)
    print(f"🎯 [NAIVE vs. CACHE-OBLIVIOUS] Plot figure saved for test '{config}' in [./plots] directory!")

    # plotting the results of each test and each tree
    # so as to see the asymptotic trend
    print("\n\n🔜 Plotting asymptotic trends...")
    df = pd.read_csv(RESULTS_FILE)
    for config in CONFIGS:
        plot_separately(df, config)
        print(f"🎯 [ASYM. TREND] Plot figure saved for test '{config}' in [./plots] directory!")

if __name__ == "__main__":
    main()
