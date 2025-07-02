import os
import re
import socket
import time
import bz2
import gzip
import pandas as pd

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

# Prepare output data
data = {'command': [], 'logs': []}

# Log parsing logic
def log_parser(lines):
    for line in lines:
        line_str = line.decode('utf-8', errors='ignore') if isinstance(line, bytes) else str(line)
        if re.search(regex_pattern, line_str):
            found_cmds = '|'.join(re.findall(regex_pattern, line_str))
            data['command'].append(found_cmds)
            data['logs'].append(line_str)

# File scanning and parsing logic
def file_checker():
    log_dir = input('Enter the path to the directory containing log files: ')
    if not os.path.isdir(log_dir):
        print("Invalid directory.")
        exit(1)

    for root, _, files in os.walk(log_dir):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                if file.endswith('.bz2'):
                    print(f"Reading BZ2: {file_path}")
                    with bz2.BZ2File(file_path, 'rb') as f:
                        lines = f.readlines()
                        log_parser(lines)

                elif file.endswith('.gz'):
                    print(f"Reading GZ: {file_path}")
                    with gzip.open(file_path, 'rb') as f:
                        lines = f.readlines()
                        log_parser(lines)

                elif file.endswith('.log'):
                    print(f"Reading LOG: {file_path}")
                    with open(file_path, 'rb') as f:
                        lines = f.readlines()
                        log_parser(lines)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Run the file checker
file_checker()

# Export results
df = pd.DataFrame.from_dict(data)
df.to_csv(output_filename, index=False)
print(f"\n✅ Parsing complete. Results saved to: {output_filename}")
print(f"⏱️ Duration: {round(time.time() - start, 2)} seconds")

