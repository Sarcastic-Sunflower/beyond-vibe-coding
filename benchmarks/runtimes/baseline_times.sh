#!/bin/bash

PARENT_DIR="../../datasets/input/"
OUTPUT_FILE="baseline_benchmarks.txt"

if [ ! -d "$PARENT_DIR" ]; then
    echo "Error: Directory $PARENT_DIR not found."
    exit 1
fi

echo "ID, Time (ms)" > "$OUTPUT_FILE"

TIMEFORMAT='%R'

echo "Starting benchmarks in $PARENT_DIR..."

        EXEC_TIME=$({ time python3 dataset1.py > /dev/null 2>&1; } 2>&1)

        MS_TIME=$(echo "$EXEC_TIME * 1000" | bc -l | xargs printf "%.0f")

        echo "Dataset1, $MS_TIME" >> "$OUTPUT_FILE"


echo "Starting benchmarks in $PARENT_DIR..."

        EXEC_TIME=$({ time python3 dataset2.py > /dev/null 2>&1; } 2>&1)

        MS_TIME=$(echo "$EXEC_TIME * 1000" | bc -l | xargs printf "%.0f")

        echo "Dataset2, $MS_TIME" >> "$OUTPUT_FILE"

echo "------------------------------------------------"
echo "Done! Results saved to $(realpath "$OUTPUT_FILE")"
