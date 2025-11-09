#!/bin/bash
# script to run all matrix transposition tests and save results to .csv format

mkdir -p csv_out

echo "Saving all matrix experiment results to .csv"
for config in m1024-b16 m8192-b64 m65536-b256 m65536-b4096; do
    naive="out/t-sim-${config}-naive"
    smart="out/t-sim-${config}-smart"
    output="csv/${config}.csv"

    if [[ -f "$naive" && -f "$smart" ]]; then
        paste "$naive" "$smart" | awk '{print $1 "," $2 "," $4}' > "$output"
        echo "Saved: $config -> $output"
    else
        echo "Missing files for $config"
    fi
done
