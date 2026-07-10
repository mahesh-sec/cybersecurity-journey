# Week 3 / Day 5 — Logging, Cron & Process Monitoring

## Overview
Day 5 focused on two core Linux subsystems that matter heavily for security monitoring and persistence detection: **logging** (journald, rsyslog, logrotate) and **cron** (scheduled task execution). The day tied both together under the lens of "how attackers persist, and how logs help you catch it."

## Topics Covered

### 1. Logging architecture
- Where logs live: `/var/log/auth.log`, `/var/log/syslog`, and the binary systemd journal (`/var/log/journal/`)
- **journald**: collects and stores nearly all system activity in structured binary format; queried via `journalctl` (not human-readable directly)
- **rsyslog**: the traditional syslog daemon; can receive forwarded messages from journald and write them out as plain text log files
- **Direct app writes**: many services (Apache, dpkg, custom scripts) write their own log files directly, bypassing journald/rsyslog entirely
- **logrotate**: a maintenance utility (not a logger) that manages plain text log files in `/var/log/` — rotates, compresses, and deletes old logs on a schedule, itself triggered daily via cron. Config lives in `/etc/logrotate.conf` (global) + `/etc/logrotate.d/*` (per-service rule files, each pointing at a log file path elsewhere on disk)

### 2. Cron
- Cron daemon wakes every minute and checks scheduled jobs against the current time
- 5-field crontab syntax: `minute hour day-of-month month day-of-week`
- Three places jobs can live:
  - **User crontabs** (`crontab -e`, stored at `/var/spool/cron/crontabs/<user>`) — no username field, runs as that user
  - **`/etc/crontab`** — system-wide, includes an extra **username field** since it's shared/root-owned
  - **`/etc/cron.d/`** — same format as `/etc/crontab`, but split into one file per package/service (mirrors the `logrotate.d` design pattern)
  - **`/etc/cron.daily|weekly|monthly/`** — plain executable scripts, no crontab syntax; run-parts executes everything inside on schedule
- **Persistence angle**: attackers commonly plant cron jobs to maintain access after initial compromise; `/etc/cron.d/` is a commonly overlooked spot in manual triage

### 3. Deep Dive — Cron-based privilege escalation (concept only)
- Pattern: root-owned cron job → references a **world-writable** script → low-priv user overwrites script contents → next cron run executes attacker code as root
- Checked Metasploitable's `/etc/crontab`, `/etc/cron.d/*`, and `msfadmin`'s user crontab for this pattern — **no world-writable scripts found**, and `msfadmin` has no crontab configured. Valid negative result; concept understood via GTFOBins reference even though not demonstrable on this target's default config.

## Hands-On Work
- Scheduled `disk_report.sh` (from Day 4) to run every 5 minutes via user crontab; confirmed execution live via `journalctl -u cron -f`
- Practiced `journalctl -xe`, `journalctl --since "1 hour ago"`, `journalctl -u ssh`
- Simulated failed SSH logins against own Kali VM; captured and interpreted the full auth chain: `unix_chkpwd` → PAM `authentication failure` (with `rhost=` source IP) → `Failed password` → `Accepted password` → `pam_unix(sshd:session): session opened`
- Confirmed no `journalctl -u ssh` socket-activation naming quirk this session (unlike Day 4)

## Files in this folder
- `logging-and-cron.md` — full reference notes: cron syntax cheatsheet, journalctl cheatsheet, logrotate/journald/rsyslog architecture, writable-cron-script escalation pattern
- `ssh-log-triage-notes.md` — annotated breakdown of a real simulated failed/successful SSH login capture from journalctl

## Key Takeaway
Understood that logrotate and journald are fundamentally different systems solving different problems (housekeeping vs. querying), and that cron's three storage locations exist for a clear structural reason (personal vs. shared vs. per-package scheduling). Also reinforced the "check, don't assume" principle — a clean cron permissions check on Metasploitable is still a valid, documented finding.
