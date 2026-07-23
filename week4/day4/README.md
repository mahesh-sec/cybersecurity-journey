# Week 4 Day 4: SSH Auth Log Parser & Brute-Force Detector

## Overview
Theory + lab day covering log parsing, Python regex, and building a CLI tool
that parses SSH auth logs and flags brute-force-style failed login activity.

## Files
- `theory_notes.md` — regex, journalctl/auth.log structure, brute-force concepts
- `log_parser.py` — initial version (hardcoded file path, threshold=5)
- `auth_logcli.py` — final version with argparse CLI flags
- `auth_sample.log` — sample log data generated on a local Kali VM (loopback)

## Usage
```bash
# Export SSH logs (modern Kali uses journald, not /var/log/auth.log)
journalctl -u ssh --since "1 month ago" -o short-iso --no-pager > auth_sample.log

# Run the CLI version
python3 auth_logcli.py -f auth_sample.log -t 5
```

## What it detects
- Parses both "invalid user X" (nonexistent account) and "X" (real account,
  wrong password) log line formats
- Tallies failed attempts per username
- Flags any username crossing the failure threshold as possible brute-force activity

## Lab environment
Data generated via repeated SSH connection attempts against localhost
(127.0.0.1 / ::1) on a Kali VM — wrong usernames, wrong passwords, and one
successful login per test user, to validate both the "Failed" and "Accepted"
regex branches.
