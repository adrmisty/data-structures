"""
---------------------------------------------------------------------------------

    - Adriana Rodríguez Flórez
    - adrirflorez@gmail.com
    - Course: NTIN066 Data Structures
    - Homework 5, AB TREE EXPERIMENT
    - Version: ÚFAL 24/25; March 2025 

---------------------------------------------------------------------------------
"""

import subprocess
import pandas as pd
import csv, numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# params: student number (UKČO), and tree construction to test
STUDENT_ID = "17957513"
TESTS = ["insert", "min", "random"]
TREES = ["2-3", "2-4"]

# results: .csv format,
RESULTS_FILE = "ab_results.csv"
CSV_COLS = ["Test", "Tree", "n", "Structural_Changes_Per_Operation"]

# ---------------------------------------------------------------------------------

def run(test, tree):
    """
    Runs a specific test for a specific (a,b)-tree and 
    saves the output for further processing.
    
    Parameters
    ----------
    test : str
        name of the test to run (sequential|random|subset) 
    tree : str
        dimensions of the tree to test (2-3|2-4...)
    
    Returns
    -------
    lines : list
        list of output string lines in the command line
    """
    cli = ["python", "./hw5_abtree-experiment/ab_experiment.py", test, STUDENT_ID[-2:], tree]
    result = subprocess.run(cli, check=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error running {test} with ({tree})-tree: {result.stderr}")
        return []
    
    return result.stdout.splitlines()

def save(test, impl, line, file, writer):
    """
    For a given experiment of a test done for specific tree dimensions,
    the output consists of the number of structural changes done per operation.

    Parameters
    ----------
    line : str
        output line from the command line's execution of a splay experiment
    
    Returns
    -------
    writer : csv.Writer
        comma-separated-value format writer with the newly-added data
    """
    parts = line.split()
    n, structural_changes = parts
    #CSV_COLS = ["Test", "Tree", "n", "Structural_Changes_Per_Operation"]
    writer.writerow([test, impl, int(n), float(structural_changes)])
    file.flush() # refresh file
    return writer, file

# ---------------------------------------------------------------------------------

def plot(df, test):
    """
    For a given test, plot its results saved onto a CSV file.
    
    Parameters
    ----------
    test : str
        name of the test (sequential|random|subset) to plot results for
    subset : bool
        default False, whether it is a test for the subset
    """
    plt.figure(figsize=(10, 6))
    title = f"[{test.capitalize()}] structural changes per operation"
    x_label = "Set size (n)"
    y_label = "Avg. structural Changes per operation"
    
    for tree in TREES:
        tree_type = f"({tree.replace('-', ',')})-tree"
        data = df[(df["Test"] == test) & (df["Tree"] == tree)]
        if not data.empty:
            plt.plot(data["n"], data["Structural_Changes_Per_Operation"], marker="o", label=tree_type)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.subplots_adjust(bottom=0.15)
    plt.figtext(
        0.5, 0.02, 
        "Logarithmic scale used for both axes.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.legend()
    plt.savefig(f"./plots/{test}_plot.png")
    plt.show()

def plot_separately(df, test, tree_type):
    """
    Plot a single experimental curve along with theoretical curves of complexities:
    O(1), O(n) and O(log n).

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the results
    test : str
        name of the test (insert|min|random) to plot results for.
    tree_type : str
        The type of tree to plot results for (e.g., "2-3", "2-4").
    """
    plt.figure(figsize=(10, 6))
    title = f"[{test.capitalize()}] Structural Changes per Operation - {tree_type} Tree"
    x_label = "Set size (n)"
    y_label = "Avg. Structural Changes per Operation"
    
    # filter out data
    data = df[(df["Test"] == test) & (df["Tree"] == tree_type)]
    if data.empty:
        print(f"⚠️ No data found for test '{test}' with tree type '{tree_type}'.")
        return

    plt.plot(data["n"], data["Structural_Changes_Per_Operation"], marker="o", label=f"Empirical - {tree_type} Tree")
    
    # scale values
    n_values = np.array(sorted(data["n"].unique()))
    c_factor = 1e-4 

    plt.plot(n_values, np.ones_like(n_values), 'r--', label="O(1) - Constant Time")
    plt.plot(n_values, c_factor * n_values, 'g--', label="O(n) - Linear Time")
    plt.plot(n_values, c_factor * np.log2(n_values), 'b--', label="O(log n) - Logarithmic Time")
    
    # no log scale

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(f"./plots/{test}_{tree_type}_plot.png")
    plt.show()



# ---------------------------------------------------------------------------------

def main():

    """
    with open(RESULTS_FILE, mode="w", newline="") as file, open("debug.log", "w") as debug_file:
        writer = csv.writer(file)
        writer.writerow(CSV_COLS)

        print("🔜 Running tests for all trees...")
        for tree in TREES:
            for test in TESTS:
                print(f"\n🔄 Running test: {test} for {tree} tree")
                output_lines = run(test, tree)
                print(f"✅ Done: {test} for ({tree}) tree, saving results...")
                for line in output_lines:
                    writer,file = save(test, tree, line, file, writer)
                print(f"📌 Saved: {test} for ({tree}) tree")

    print(f"\n🎯 Experiments completed and results saved to [{RESULTS_FILE}]!")
    """

    # plotting the results of each test
    df = pd.read_csv(RESULTS_FILE)
    """
    print("\n\n🔜 Plotting results...")
    for test in TESTS:
        plot(df, test)
        print(f"🎯 Plot figures saved to [./plots] directory!")
    """

    # plotting the results of each test and each tree
    # so as to see the asymptotic trend
    for test in TESTS:
        for tree in TREES:
            plot_separately(df, test, tree)
            print(f"🎯 [ASYM. TREND] Plot figure saved for test '{test}' and tree '{tree}' in [./plots] directory!")

if __name__ == "__main__":
    main()
