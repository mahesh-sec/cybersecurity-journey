# Week 3, Day 4 — Bash Scripting for Security Tasks

## Focus
Bash scripting fundamentals applied to real security/SOC-relevant tasks: subnet scanning, log parsing, and system reporting.

## Theory covered
- Shebang line (`#!/bin/bash`) and its role in telling the kernel which interpreter to use
- Variables and quoting (`"$var"` vs unquoted `$var`, and why quoting matters for word-splitting)
- Conditionals (`if`/`elif`/`else`, exit-code-based tests)
- Loops (`for`, `while`, brace expansion)
- Positional parameters (`$1`–`$9`, `${10}+`, `$0`, `$#`, `$@` vs `$*` and their quoted/unquoted behavior)
- Exit codes (`$?`, and `&&`/`||` command chaining)

## Labs / Scripts written

### 1. `scripts/localnet.sh` — Subnet Ping Scanner
Sweeps the `192.168.56.0/24` Host-Only VirtualBox range and reports live hosts. Confirmed it correctly identifies Metasploitable2 at `192.168.56.101` as up.

### 2. `scripts/auth_parser.sh` — Failed SSH Login Parser
Parses failed SSH login attempts and counts them by source IP — a real SOC triage pattern for spotting brute-force behavior. Used `journalctl` instead of `/var/log/auth.log` since this system logs via `systemd-journald` rather than a flat file. Verified against manually generated failed logins (`ssh wronguser@localhost`), correctly showing `3 ::1` after three failed local attempts.

### 3. `scripts/disk_report.sh` — Disk / Process / User Usage Report
Generates a timestamped report combining `df -h`, `ps aux --sort=-%mem | head`, and `w` into a single output file, using `>>` (append) rather than `>` (overwrite) so each section is added in order without erasing the previous one.

## Tools / CTF
- OverTheWire Bandit Levels 11–12 (encoded/rotated data: ROT13, hex/gzip/bzip2 decode chains)
- OverTheWire Bandit Levels 13–15 (SSH private key auth, `ssh -i keyfile`, port-specific connections)

## Key concepts / gotchas learned
- `$0` is the script name, not a positional argument — actual arguments start at `$1`
- `$10` doesn't work as expected past single digits; requires `${10}` and up
- `"$@"` preserves arguments as separate items; `"$*"` merges them into one string — matters when iterating over arguments that may contain spaces
- VSZ (virtual memory reserved) vs RSS (physical memory actually in use) — `ps aux --sort=-%mem` sorts by RSS-based `%MEM`, the more meaningful figure for real usage
- Unquoted shell execution can silently fall back to `/bin/sh` if a shebang is missing and the kernel's direct exec fails — a reminder that a shebang isn't optional even if a script "still runs"

## Notes
All scripts tested on Kali 2026.1 against a Host-Only VirtualBox lab (host: `mpati`) with Metasploitable2 at `192.168.56.101`. Variables are quoted throughout (`"$x"`, `"$OUTFILE"`) as a defensive habit against word-splitting bugs.
