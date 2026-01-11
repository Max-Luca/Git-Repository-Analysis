# Git Repository Analysis

A Python script that analyzes Git repository history to generate file change metrics and statistics.

## Features

- Tracks added, deleted, and modified files across commits
- Calculates code churn (lines added + deleted) per file
- Counts commits per file and number of contributors
- Generates two output files with analysis results

## Requirements

```bash
pip install pydriller pandas
```

## Usage

Run the script in your Git repository:

```bash
python assignment3.py
```

This generates:
- `output_1.txt` - File changes per commit (added/deleted/modified)
- `output_2.csv` - File metrics (commit count, code churn, contributors)

## Output Files

**output_1.txt**: Lists file changes for each commit with commit IDs

**output_2.csv**: Contains columns:
- File name
- Path
- Commit Count
- Code Churn (average)
- Contributors
