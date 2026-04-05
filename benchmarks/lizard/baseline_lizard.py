import lizard
import os

def generate_flat_report(target_dir, output_file):
    if not os.path.exists(target_dir):
        print(f"Error: Directory not found -> {os.path.abspath(target_dir)}")
        return

    # Filter only for python files in the target directory
    py_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith('.py')]
    py_files.sort()

    if not py_files:
        print("No Python files found in the target directory.")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("BASELINE SCRIPT ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n\n")

        for file_path in py_files:
            file_name = os.path.basename(file_path)
            
            f.write(f"SCRIPT: {file_name}\n")
            f.write(f"{'#' * (len(file_name) + 8)}\n")

            file_info = lizard.analyze_file(file_path)

            file_nloc = 0
            file_complexity = 0
            func_count = 0

            for func in file_info.function_list:
                f.write(f" : {func.name}\n")
                f.write(f"     Complexity: {func.cyclomatic_complexity} | LOC: {func.nloc} | Params: {func.parameter_count}\n")

                file_nloc += func.nloc
                file_complexity += func.cyclomatic_complexity
                func_count += 1

            if func_count > 0:
                avg_complexity = file_complexity / func_count
                f.write(f"\n  > SCRIPT SUMMARY: {file_name}\n")
                f.write(f"    Functions:       {func_count}\n")
                f.write(f"    Total NLOC:      {file_nloc}\n")
                f.write(f"    Avg Complexity:  {avg_complexity:.2f}\n")
            else:
                f.write("\n  (No functions detected in this script)\n")

            f.write("\n" + "-"*40 + "\n\n")

    print(f"Baseline report successfully generated: {output_file}")


TARGET_PATH = '../../datasets/input'
REPORT_NAME = 'baseline_lizard.txt'

if __name__ == "__main__":
    generate_flat_report(TARGET_PATH, REPORT_NAME)
