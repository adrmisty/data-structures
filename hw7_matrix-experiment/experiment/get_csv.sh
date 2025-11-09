echo "Cache_Config,Impl,N,Misses_Per_Item" > csv/results.csv

for config in m1024-b16 m8192-b64 m65536-b256 m65536-b4096; do
    for algo in naive smart; do
        file="out/t-sim-${config}-${algo}"
        if [[ -f "$file" ]]; then
            while read -r n miss; do
                echo "$config,$algo,$n,$miss" >> csv/matrix_results.csv
            done < "$file"
        fi
    done
done

echo "✅ Combined all results into results.csv"
