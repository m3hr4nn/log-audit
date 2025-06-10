import os
import re
import socket
import time
import bz2
import pandas as pd

start = time.time()

# Setup output filename
timestamp = time.strftime("%Y%m%d-%H%M")
hostname = socket.gethostname()
output_filename = os.path.normpath(f"{hostname}_{timestamp}_ParsedLines.csv")

# Load high-risk commands from external file
def load_commands(file_path):
    commands = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                cmd = line.strip()
                if cmd:
                    commands.append(cmd)
    except FileNotFoundError:
        print(f"Command file '{file_path}' not found.")
        exit(1)
    return commands

# Convert commands to regex pattern
def build_regex_pattern(commands):
    commands = [re.escape(cmd) + r"\b" if "*" not in cmd else cmd for cmd in commands]
    return r'\b' + r'|\b'.join(commands)

# Log parser
data = {'command': [], 'logs': []}
def log_parser(input_lines, regex_pattern):
    for line in input_lines:
        line_str = str(line)
        if re.search(regex_pattern, line_str):
            found = "|".join(re.findall(regex_pattern, line_str))
            data['command'].append(found)
            data['logs'].append(line_str)

# Process files
def file_checker(regex_pattern):
    directory = input('Please enter a directory: ')
    if not os.path.isdir(directory):
        print("It is not a valid directory.")
        return

    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                print(file_path)
                if filename.endswith(".bz2"):
                    with bz2.BZ2File(file_path, "rb") as f:
                        input_lines = f.readlines()
                else:
                    with open(file_path, "rb") as f:
                        input_lines = f.readlines()
                log_parser(input_lines, regex_pattern)
            except Exception as e:
                print(f"An error occurred with file {filename}: {e}")

# Run the full flow
command_file = "commands.txt"  # <- change this if you use another filename
high_risk_commands = load_commands(command_file)
regex_pattern = build_regex_pattern(high_risk_commands)

file_checker(regex_pattern)

# Save results to CSV
df = pd.DataFrame.from_dict(data)
df.to_csv(output_filename, index=False)

print("Finished in", round(time.time() - start, 2), "seconds")
