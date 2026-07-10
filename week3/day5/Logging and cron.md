# Logging & Cron — Reference Notes

## Part 1: Logging Architecture

### The two logging worlds

**1. systemd-journald**
- A daemon that captures nearly all system activity (kernel messages, every systemd service's stdout/stderr, boot events, auth events) and stores it in a **binary** structured format
- Storage: `/var/log/journal/*.journal` — not human-readable directly, must be queried
- Manages its own size limits internally (caps itself at a % of disk space, purges oldest entries when full) — does **not** need logrotate
- Query tool: `journalctl`

**2. Plain text logs + rsyslog**
- Traditional text files under `/var/log/` (`auth.log`, `syslog`, `mail.log`, etc.)
- Written either:
  - **Directly by the application itself** (e.g. Apache writes `access.log`/`error.log` directly; dpkg writes `dpkg.log` directly) — no journald/rsyslog involved
  - **Via rsyslog**, which can receive a forwarded copy of journald's data (`ForwardToSyslog=yes`) and write it out as readable text, routed by rules in `/etc/rsyslog.conf`
- These text files are exactly what **logrotate** manages

### journalctl — query cheatsheet
```bash
journalctl -xe                      # recent logs with extra context for warnings/errors
journalctl --since "1 hour ago"     # time-filtered
journalctl -u ssh                   # logs for a specific systemd unit
journalctl -u ssh --since "10 minutes ago"
journalctl -u cron -f               # follow cron unit logs live
journalctl -n 20                    # last 20 entries
```

### logrotate — what it actually does
Not a logger — a **housekeeper** for plain text log files. Its only job: prevent `/var/log/*.log` files from growing forever and filling the disk.

Actions per rotation cycle:
1. Rename current log (`auth.log` → `auth.log.1`)
2. Start a fresh empty file with the original name
3. Compress the old one (`auth.log.1` → `auth.log.1.gz`)
4. Delete oldest rotated copies once the configured count is exceeded

**Config structure:**
- `/etc/logrotate.conf` — global defaults
- `/etc/logrotate.d/*` — one rule file per service; each contains an **absolute path** to the actual log file elsewhere on disk (e.g. `/var/log/apache2/*.log { weekly rotate 52 compress ... }`)
- The config directory does **not** contain the log data itself — it's purely a rulebook pointing outward at real file paths
- Triggered by cron — typically via `/etc/cron.daily/logrotate`

**Mental model:**
```
/etc/logrotate.d/apache2   ← RULE (points to a path + schedule)
        │
        ▼
/var/log/apache2/access.log   ← ACTUAL LOG DATA (written directly by Apache)
```

### Quick comparison

| | journald / journalctl | logrotate |
|---|---|---|
| What it manages | Binary structured journal | Plain text log files |
| Writes log content? | Yes (collects it) | No — never touches content |
| Self-cleaning? | Yes, built-in size cap | No — needs cron-triggered runs |
| Human-readable directly? | No — needs journalctl | Yes — plain text |

---

## Part 2: Cron

### What cron is
A daemon (`cron`/`crond`) that wakes once per minute and checks whether any scheduled job's time fields match the current time. If so, it runs that job, then goes back to sleep. Nothing more complex than a clock-matching loop.

### 5-field crontab syntax
```
* * * * * command-to-run
│ │ │ │ │
│ │ │ │ └── day of week (0-6, Sunday=0)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

Syntax variants:
- `*` — any value
- `*/5` — every 5th unit (step value)
- `1,15` — list of specific values
- `9-17` — range

Example used in Day 5 lab:
```
*/5 * * * * /home/kali/scripts/disk_report.sh
```
Runs every 5 minutes.

### The three (four) places cron jobs live

**1. User crontab**
- `crontab -e` / `crontab -l` / `crontab -r`
- Stored at `/var/spool/cron/crontabs/<username>`
- No username field — implicit from file ownership
- Runs as that user

**2. `/etc/crontab`**
- System-wide, root-editable directly
- Has an **extra username field** after the time fields:
```
*/5 * * * * root /usr/local/bin/backup-check.sh
```

**3. `/etc/cron.d/`**
- Directory of individual files, one per package/service — same design pattern as `logrotate.d`
- Same format as `/etc/crontab` (includes username field)
- Example: `/etc/cron.d/sysstat` → `*/10 * * * * root /usr/lib/sysstat/debian-sa1 1 1`

**4. `/etc/cron.daily/`, `/etc/cron.weekly/`, `/etc/cron.monthly/`**
- Not crontab syntax at all — just executable scripts dropped into the directory
- Cron runs everything inside via `run-parts` on the matching schedule
- This is where logrotate's own trigger script lives: `/etc/cron.daily/logrotate`

### Comparison table

| Type | Location | Format | Editor |
|---|---|---|---|
| User crontab | `/var/spool/cron/crontabs/<user>` | 5 fields + command | `crontab -e` |
| System crontab | `/etc/crontab` | 5 fields + username + command | root, direct edit |
| cron.d files | `/etc/cron.d/*` | 5 fields + username + command | root/packages |
| cron.daily/weekly/monthly | `/etc/cron.daily/` etc. | plain executable script | root/packages |

---

## Part 3: Persistence & Privilege Escalation Angle

### Cron as a persistence mechanism
Attackers who gain a shell can plant a cron job to reconnect periodically, surviving reboots and session kills. `/etc/cron.d/` is a commonly overlooked triage spot since it's a directory of small files rather than one obvious location.

**Triage commands:**
```bash
crontab -l                    # own user's jobs
sudo crontab -u <user> -l     # another user's jobs
cat /etc/crontab              # system-wide file
ls -la /etc/cron.d/           # dropped-in rule files
cat /etc/cron.d/*
```

### Writable cron script → privilege escalation (concept)
Pattern: a **root-owned cron job** references a script that is **world-writable**. A low-privilege user can overwrite the script's contents. On the next scheduled run, the attacker's injected code executes with **root** privileges.

Checked on Metasploitable:
- `/etc/crontab` — reviewed for root-run scripts
- `/etc/cron.d/*` — no world-writable files found
- `msfadmin` user crontab — none configured

**Result:** No demonstrable instance of this escalation path on this target's default configuration. Concept understood via GTFOBins reference (`gtfobins.github.io`, search "cron privilege escalation") even without a live example — this is a valid, documented negative finding, not a failed check.
