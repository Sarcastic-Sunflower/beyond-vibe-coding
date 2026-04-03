#python3 -m venv .venv
#source .venv/bin/activate
import lizard
import os

def generate_communal_report(root_dir, output_file):
    if not os.path.exists(root_dir):
        print(f"Error: Directory not found -> {os.path.abspath(root_dir)}")
        return

    subfolders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f)) and f.startswith('run_D')]
    subfolders.sort()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("COMMUNAL LIZARD ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n\n")

        for folder in subfolders:
            folder_path = os.path.join(root_dir, folder)
            py_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.py')]

            if not py_files:
                continue

            f.write(f"FOLDER: {folder}\n")
            f.write(f"{'#' * (len(folder) + 8)}\n")

            # Analyze the files in the folder
            file_analyses = lizard.analyze(py_files)

            total_nloc = 0
            total_complexity = 0
            func_count = 0

            # file_analyses is a generator of 'FileInformation' objects
            for file_info in file_analyses:
                fname = os.path.basename(file_info.filename)
                
                # Each file_info has a 'function_list'
                for func in file_info.function_list:
                    f.write(f"  [{fname}]: {func.name}\n")
                    f.write(f"    Complexity: {func.cyclomatic_complexity} | LOC: {func.nloc} | Params: {func.parameter_count}\n")

                    total_nloc += func.nloc
                    total_complexity += func.cyclomatic_complexity
                    func_count += 1

            if func_count > 0:
                avg_complexity = total_complexity / func_count
                f.write(f"\n  > FOLDER SUMMARY: {folder}\n")
                f.write(f"    Total Functions: {func_count}\n")
                f.write(f"    Total NLOC:      {total_nloc}\n")
                f.write(f"    Avg Complexity:  {avg_complexity:.2f}\n")

            f.write("\n" + "-"*40 + "\n\n")

    print(f"Report successfully generated: {output_file}")

# --- CONFIGURATION ---
TARGET_PATH = '../../experiments/runs'
REPORT_NAME = 'summary_lizard.txt'

if __name__ == "__main__":
    generate_communal_report(TARGET_PATH, REPORT_NAME)
#deactivate
