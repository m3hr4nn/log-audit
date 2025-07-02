import os
import re
import socket
import time
import bz2
import gzip
import csv 

# Start timing
start = time.time()

# Output file setup
timestamp = time.strftime("%Y%m%d-%H%M")
hostname = socket.gethostname()
output_filename = f"{hostname}_{timestamp}_ParsedLines.csv"

# Fallback commands
fallback_commands = ['systemctl', 'reboot', 'shutdown']

# Suggest default command file if user presses Enter
command_file = input("Enter the path to the command list (.txt file) [press Enter to use 'commands.txt' in this directory]: ").strip()

if not command_file:
    default_path = os.path.join(os.path.dirname(__file__), 'commands.txt')
    if os.path.isfile(default_path):
        use_default = input("Found 'commands.txt' in script directory. Use it? (y/n): ").strip().lower()
        if use_default in ['y', 'yes']:
            command_file = default_path
        else:
            print("No command file selected. Using default critical commands.\n")
            commands = fallback_commands
    else:
        print("No 'commands.txt' found. Using default critical commands.\n")
        commands = fallback_commands

if command_file:
    try:
        with open(command_file, 'r') as f:
            commands = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\nFile '{command_file}' not found.")
        use_fallback = input("Use default critical commands (systemctl, reboot, shutdown)? (y/n): ").strip().lower()
        if use_fallback in ['y', 'yes']:
            commands = fallback_commands
        else:
            print("Exiting.")
            exit(1)

# Build regex pattern
escaped_commands = [re.escape(cmd) for cmd in commands]
regex_pattern = r'\b(?:' + '|'.join(escaped_commands) + r')\b'

# Prepare output storage
results = []

# Extract date
def extract_date(line):
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\b', line)
    if date_match:
        return date_match.group(1)
    date_match2 = re.search(r'\b([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2})\b', line)
    if date_match2:
        return date_match2.group(1)
    return ''

# Parse log lines
def log_parser(lines, current_file):
    for line in lines:
        line_str = line.decode('utf-8', errors='ignore') if isinstance(line, bytes) else str(line)
        if re.search(regex_pattern, line_str):
            found_cmds = '|'.join(re.findall(regex_pattern, line_str))
            results.append({
                'date': extract_date(line_str),
                'command': found_cmds,
                'file': current_file,
                'logs': line_str.strip()
            })

# File scanner
def file_checker():
    log_dir = input('Enter the path to the directory containing log files (press Enter for default: /var/log): ').strip()
    if not log_dir:
        log_dir = '/var/log'
    if not os.path.isdir(log_dir):
        print(f"Directory '{log_dir}' is invalid.")
        exit(1)

    log_files = []
    for root, _, files in os.walk(log_dir):
        for file in files:
            if file.endswith(('.bz2', '.gz', '.log')):
                log_files.append(os.path.join(root, file))

    print(f"\nFound {len(log_files)} log files. Starting scan...\n")

    for index, file_path in enumerate(log_files, 1):
        print(f"[{index}/{len(log_files)}] Scanning: {file_path}")
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

# Run scanner
file_checker()

# Write results manually to CSV
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date', 'command', 'file', 'logs'])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Parsing complete. Results saved to: {output_filename}")
print(f"⏱️ Duration: {round(time.time() - start, 2)} seconds")
