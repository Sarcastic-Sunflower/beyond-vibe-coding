kk#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 X Y Z"
    exit 1
fi

X=$1; Y=$2; Z=$3
TARGET_FILE="../../experiments/runs/run_D${X}_C${Y}.${Z}/output.txt"
TRUE_FILE="../../datasets/ground_truth/true_moves${X}.txt"
SUMMARY_FILE="summary${X}.txt"

if [[ ! -f "$TRUE_FILE" || ! -f "$TARGET_FILE" ]]; then
    echo "Error: Files missing."
    exit 1
fi

# Initialize global counters
run_correct=0
run_total=0

{
    echo "--- Mismatch Report for Run D${X}_C${Y}.${Z} ---"
    
    for i in {1..4}; do
        # 1. Clean strings (Essential for WSL/Ubuntu on Windows)
        true_raw=$(sed -n "${i}p" "$TRUE_FILE" | tr -d '\r')
        test_raw=$(sed -n "${i}p" "$TARGET_FILE" | tr -d '\r')

        # 2. Parse semicolon lists
        true_list=$(echo "$true_raw" | awk -F': ' '{print $NF}' | tr ';' '\n' | sed '/^$/d' | sort)
        test_list=$(echo "$test_raw" | awk -F': ' '{print $NF}' | tr ';' '\n' | sed '/^$/d' | sort)

        # 3. Calculate Counts (Forcing 0 if empty)
        c_true=$(echo "$true_list" | grep -v '^$' | wc -l)
        c_correct=$(comm -12 <(echo "$true_list") <(echo "$test_list") | grep -v '^$' | wc -l)
        c_missing=$(comm -23 <(echo "$true_list") <(echo "$test_list") | grep -v '^$' | wc -l)
        c_extra=$(comm -13 <(echo "$true_list") <(echo "$test_list") | grep -v '^$' | wc -l)

        # 4. Arithmetic with Fallbacks
        mismatches=$(( ${c_missing:-0} + ${c_extra:-0} ))
        run_correct=$(( ${run_correct:-0} + ${c_correct:-0} ))
        run_total=$(( ${run_total:-0} + ${c_true:-0} ))

        if [ "$mismatches" -eq 0 ]; then
            echo "Line $i: MATCH (0 mismatches)"
        else
            echo "Line $i: MISMATCH ($mismatches total: $c_missing missing, $c_extra extra)"
        fi
    done

    echo "Line 5 (Ref): $(sed -n '5p' "$TRUE_FILE" | tr -d '\r')"

    # 5. Accuracy Calculation
    if [ "$run_total" -gt 0 ]; then
        accuracy=$(echo "scale=4; ($run_correct / $run_total) * 100" | bc | xargs printf "%.2f")
        echo "--------------------------------------"
        echo "TOTAL ACCURACY: $accuracy%"
        echo "MATH: ($run_correct correct / $run_total expected) * 100"
    else
        echo "Error: No ground truth moves found."
    fi
    echo -e "\n"
} | tee -a "$SUMMARY_FILE"
