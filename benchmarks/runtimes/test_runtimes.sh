#!/bin/bash

PARENT_DIR="../../experiments/runs/"
OUTPUT_FILE="communal_benchmarks.txt"

if [ ! -d "$PARENT_DIR" ]; then
    echo "Error: Directory $PARENT_DIR not found."
    exit 1
fi

echo "ID, Time (ms)" > "$OUTPUT_FILE"

TIMEFORMAT='%R'

echo "Starting benchmarks in $PARENT_DIR..."

for dir in "$PARENT_DIR"*/; do
    # Remove trailing slash
    dir=${dir%/}
    
    if [ -d "$dir" ]; then
        ID=$(basename "$dir")
        
        # Navigate to the subfolder
        cd "$dir" || continue

        if [ -f "main.py" ]; then
            ENTRY_POINT="main.py"
        elif [ -f "code.py" ]; then
            ENTRY_POINT="code.py"
        else
            echo "Skipping $ID: No entry point found."
            cd - > /dev/null
            continue
        fi

        echo "Running project: $ID"

        # Silencing Python output to keep the console clean
        EXEC_TIME=$({ time python3 "$ENTRY_POINT" > /dev/null 2>&1; } 2>&1)

        # Convert seconds to milliseconds (Seconds * 1000)
        MS_TIME=$(echo "$EXEC_TIME * 1000" | bc -l | xargs printf "%.0f")

        echo "$ID, $MS_TIME" >> "$OLDPWD/$OUTPUT_FILE"

        cd - > /dev/null
    fi
done

echo "------------------------------------------------"
echo "Done! Results saved to $(realpath "$OUTPUT_FILE")"
