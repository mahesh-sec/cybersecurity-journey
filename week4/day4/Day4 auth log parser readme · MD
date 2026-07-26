# SSH Auth Log Parser & Brute-Force Detector

## What It Does
Parses an SSH `auth.log`-style file with regex, extracts every login attempt (timestamp, username, source IP, source port, and whether it succeeded or failed), prints each parsed event, and flags any username that racks up failed attempts past a configurable threshold — a simple brute-force detection rule.

## How It Works
- A single regex captures the timestamp, `Failed`/`Accepted` status, username (handling both normal and `invalid user <name>` log formats), source IP, and source port from each line.
- Failed attempts are tallied per-username in a dictionary as the file is read.
- After parsing finishes, any username at or above `--threshold` failed attempts triggers an `ALERT` line.

## Usage
```bash
python auth_logcli.py [-f <log_file>] [-t <threshold>]
```

| Flag | Description | Default |
|---|---|---|
| `-f`, `--file` | Path to the log file to parse | `/home/kali/auth_sample.log` |
| `-t`, `--threshold` | Failed-attempt count that triggers an alert | `5` |

**Example:**
```bash
python auth_logcli.py -f /var/log/auth.log -t 5
```

## Example Output
```
The time is 2026-07-20T03:14:11 , the username is root,the ip is 203.0.113.42 from port 51422
The time is 2026-07-20T03:14:13 , the username is root,the ip is 203.0.113.42 from port 51430
The time is 2026-07-20T03:14:15 , the username is admin,the ip is 203.0.113.42 from port 51441
ALERT: 'root' had 6 failed login attempts - possible brute-force activity
```

## Security Concept
This script demonstrates **log analysis and correlation-rule alerting** — the bread-and-butter task of a SOC Tier 1 analyst. Real SIEMs (Splunk, Wazuh, Elastic) run the same fundamental logic at scale: parse structured/semi-structured log lines, extract fields, count events per key over a window, and fire an alert when a threshold is crossed. This is exactly the pattern behind brute-force and credential-stuffing detection rules in production security monitoring.

## Possible Improvements
- Only accepted logins currently print but aren't counted toward anything — consider tracking successful logins after repeated failures (a classic "brute-force success" indicator).
- Add a time window (e.g. failures within 60 seconds) rather than counting failures across the entire file, to better match real-world rate-based detection.
