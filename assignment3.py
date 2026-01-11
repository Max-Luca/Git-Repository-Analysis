import os
import subprocess
import pandas as pd
from pydriller import Repository

REPO_PATH = "."   # local git repo path

# PART 1: output_1.txt

def generate_output_1():
    commits = list(Repository(REPO_PATH).traverse_commits())
    commits.reverse()  # Oldest → newest

    with open("output_1.txt", "w") as f:
        for i in range(1, len(commits)):
            prev_commit = commits[i - 1].hash
            curr_commit = commits[i].hash

            result = subprocess.run(
                ["git", "diff", "--name-status", prev_commit, curr_commit],
                capture_output=True, text=True
            )

            added, deleted, modified = [], [], []

            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                status, path = line.split("\t", 1) # Process each line of git diff output

                if status == "A":
                    added.append(path)
                elif status == "D":
                    deleted.append(path)
                elif status == "M":
                    modified.append(path) # Check file status

            f.write(f"Commit ID: {curr_commit} Added files: {added}\n")
            f.write(f"Commit ID: {curr_commit} Deleted files: {deleted}\n")
            f.write(f"Commit ID: {curr_commit} Modified files: {modified}\n\n")

# PART 2: output_2.csv

def generate_output_2():
    data = []

    repo = Repository(REPO_PATH)
    file_metrics = {}

    for commit in repo.traverse_commits():
        for file in commit.modified_files:
            path = file.new_path or file.old_path
            if not path:
                continue

            if path not in file_metrics:
                file_metrics[path] = {
                    "commits": 0,
                    "churn": [],
                    "authors": set()
                }

            file_metrics[path]["commits"] += 1
            churn = abs(file.added_lines + file.deleted_lines)
            file_metrics[path]["churn"].append(churn)
            file_metrics[path]["authors"].add(commit.author.name)

    for path, values in file_metrics.items():
        file_name = os.path.basename(path)
        avg_churn = sum(values["churn"]) / len(values["churn"])
        contributors = len(values["authors"])

        data.append([
            file_name,
            path,
            values["commits"],
            round(avg_churn, 2),
            contributors
        ])

    df = pd.DataFrame(data, columns=[
        "File",
        "Path",
        "Commit Count",
        "Code Churn",
        "Contributors"
    ]) # Create a DataFrame and write it to output_2.csv

    df.to_csv("output_2.csv", index=False)

# MAIN

if __name__ == "__main__":
    print("Generating output_1.txt")
    generate_output_1()

    print("Generating output_2.csv")
    generate_output_2() # The 2 files are created