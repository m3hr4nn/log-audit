import os
import re
import socket
import time
import bz2
import gzip
import pandas as pd
from tqdm import tqdm  # for progress bar

# Start timing
start = time.time()

# Output file setup
timestamp = time.strftime("%Y%m%d-%H%M")
hostname = socket.gethostname()
output_filename = f"{hostname}_{timestamp}_ParsedLines.csv"

# Ask user for command file path
command_file = input("Enter the path to the command list (.txt file): ")

# Fallback commands
fallback_commands = ['systemctl', 'reboot', 'shutdown']

# Read command list
try:
    with open(command_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"\nFile '{command_file}' not found.")
    use_fallback = input("Use default critical commands (systemctl, reboot, shutdown)? (y/n): ")
    if use_fallback.lower() in ['y', 'yes']:
        commands = fallback_commands
    else:
        print("Exiting.")
        exit(1)

# Build regex pattern (exact command match using \b word boundaries)
escaped_commands = [re.escape(cmd) for cmd in commands]
regex_pattern = r'\b(?:' + '|'.join(escaped_commands) + r')\b'

# Prepare output data with added 'file' and 'date'
data = { 'date': [], 'command': [], 'file': [], 'logs': [] }

# Function to extract date from a log line
def extract_date(line):
    # Example patterns: YYYY-MM-DD HH:MM:SS or similar
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\b', line)
    if date_match:
        return date_match.group(1)
    # Try other common syslog formats if needed
    # For example: 'Jul 28 15:30:01'
    date_match2 = re.search(r'\b([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2})\b', line)
    if date_match2:
        return date_match2.group(1)
    return ''  # Empty if no date found

# Log parsing logic
def log_parser(lines, current_file):
    for line in lines:
        line_str = line.decode('utf-8', errors='ignore') if isinstance(line, bytes) else str(line)
        if re.search(regex_pattern, line_str):
            found_cmds = '|'.join(re.findall(regex_pattern, line_str))
            data['command'].append(found_cmds)
            data['logs'].append(line_str.strip())
            data['file'].append(current_file)
            data['date'].append(extract_date(line_str))

# File scanning and parsing logic
def file_checker():
    log_dir = input('Enter the path to the directory containing log files (press Enter for default: /var/log): ').strip()
    if not log_dir:
        log_dir = '/var/log'
    if not os.path.isdir(log_dir):
        print(f"Directory '{log_dir}' is invalid.")
    exit(1)

    # Collect all relevant files first to have a progress bar
    log_files = []
    for root, _, files in os.walk(log_dir):
        for file in files:
            if file.endswith(('.bz2', '.gz', '.log')):
                log_files.append(os.path.join(root, file))

    # Use tqdm progress bar over log_files
    for file_path in tqdm(log_files, desc="Scanning log files"):
        try:
            if file_path.endswith('.bz2'):
                with bz2.BZ2File(file_path, 'rb') as f:
                    lines = f.readlines()
                    log_parser(lines, file_path)

            elif file_path.endswith('.gz'):
                with gzip.open(file_path, 'rb') as f:
                    lines = f.readlines()
                    log_parser(lines, file_path)

            elif file_path.endswith('.log'):
                with open(file_path, 'rb') as f:
                    lines = f.readlines()
                    log_parser(lines, file_path)

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Run the file checker
file_checker()

# Export results with new columns
df = pd.DataFrame.from_dict(data)
df.to_csv(output_filename, index=False)
print(f"\n✅ Parsing complete. Results saved to: {output_filename}")
print(f"⏱️ Duration: {round(time.time() - start, 2)} seconds")

