# Log Command Extractor

A Python script to recursively parse log files (including `.bz2` compressed files) in a given directory and extract lines containing specific system or application commands. The script aggregates these lines along with the matched commands and exports the results to a CSV file.

---

## Features

- Supports both plain text and bz2 compressed log files.
- Searches log lines for a wide list of system, network, and application commands.
- Recursively processes all files in the provided directory and its subdirectories.
- Outputs results in CSV format with matched commands and corresponding log lines.
- Prints processing time for performance insights.

---

## How it works

1. The script asks for the path to the directory containing your log files.
2. It scans all files and subdirectories.
3. Each file is opened and read (decompressing if needed).
4. Each line is checked against a regex pattern for specific commands or keywords.
5. Matching lines are saved with their detected commands.
6. A CSV file is generated with columns: `command` and `logs`.

---

## Requirements

- Python 3.x
- pandas (`pip install pandas`)

---

## Usage

1. Save the script to a file, e.g., `log_command_extractor.py`.
2. Run the script:
```bash
   python log_command_extractor.py
```
3. When prompted, enter the full path to the directory with your log files.
4. The script will process the logs and generate a CSV output file named like:
```php
<hostname>_YYYYMMDD-HHMMParsedLines.csv
```

---

If you want, I can also help you **refactor** the script for better clarity or add command-line argument support. 
Just let me know!
