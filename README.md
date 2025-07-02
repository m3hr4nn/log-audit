# 🛡️ LogPatrol — Lightweight Log Audit Tool

**LogPatrol** is a fast, dependency-free Python script that scans system log files for suspicious or critical command usage like `reboot`, `shutdown`, `systemctl`, or any custom-defined commands — even in compressed logs!

> 💡 Ideal for DevOps, sysadmins, and incident responders who need quick visibility into system-level actions across logs.

---

## 🔍 Features

- ✅ **Find dangerous or suspicious commands** like `reboot`, `rm`, or `systemctl`
- 🧠 **Scans plain & compressed logs** (`.log`, `.gz`, `.bz2`) — even extensionless logs like `/var/log/syslog`
- 📦 **No external dependencies** — only Python standard library
- 📁 **Includes the source filename** and **timestamp** for every match
- 📊 **Exports to clean CSV** you can open in Excel for filtering/sorting
- 🚀 **Fast** and optimized — skips files without matches
- 🧩 **Customizable** — define your own command list in `commands.txt`

---

## ⚙️ How It Works

1. Place a list of commands (one per line) in a `commands.txt` file (optional)
2. Run the script:
   ```bash
   python3 logpatrol.py
   ```
3. Choose a log directory (default: /var/log)
4. Review the results in a neatly structured CSV file like:
   
   ```bash
   hostname_20250702-1420_ParsedLines.csv
   ```
## 📁 Output Example

| date                | command   | file               | logs                                |
|---------------------|-----------|--------------------|--------------------------------------|
| 2025-07-01 04:12:30 | reboot    | /var/log/syslog    | system reboot initiated by root      |
| Jul 1 02:01:05      | systemctl | /var/log/messages  | systemctl restart nginx.service      |

*Note: Matched time patterns include YYYY-MM-DD HH:MM:SS or common syslog formats.*

---

## 🧩 Custom Commands

Define your own suspicious or tracked commands by creating a `commands.txt` file next to the script:

- reboot
- shutdown
- systemctl
- iptables
- rm -rf
- ...
  
If no file is found, LogPatrol will use a default list of critical commands.

---

## 💼 Use Cases

- 🔍 **Security Audits**: Find unauthorized reboots or shutdowns  
- 🔧 **Debugging**: Trace command-triggered issues  
- 📊 **Compliance**: Record actions for reporting and accountability  
- 🛡️ **Forensics**: Triage after incidents  

---

## 🧰 Requirements

- Python 3.x  
- No third-party modules required  

---

## 🚀 Why Use LogPatrol?

✅ Faster than grepping multiple files manually  
✅ Works with compressed logs  
✅ Clean Excel-ready output  
✅ Fully portable — works anywhere Python does  

---

## 📃 License

MIT License © 2025

