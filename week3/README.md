# Week 3 — Linux Fundamentals for Security

**Goal:** Reach intermediate Linux proficiency, since Linux powers 90%+ of security tooling.

## Command Categories Mastered

- **Filesystem hierarchy & navigation** — absolute vs relative paths, core directory structure (`/etc`, `/var/log`, `/proc`), piping and redirection
- **File permissions & ownership** — `rwx`/octal notation, `chmod`/`chown`, SUID/SGID bits, the sticky bit, and exploiting SUID misconfigurations via GTFOBins
- **Users, groups & authentication internals** — `/etc/passwd` and `/etc/shadow` structure, password hash formats, sudoers file and `visudo`, user/group management commands
- **Bash scripting for security tasks** — positional parameters, exit codes, conditionals and loops in shell scripts
- **Logging & cron** — `journald`, `rsyslog`, reading and correlating log entries, cron job structure and the cron-based privilege escalation pattern
- **Manual privilege escalation enumeration** — `sudo -l` misconfiguration checks, SUID binary hunting (`find / -perm -4000`), cron job auditing, and the real vs. effective UID distinction

## Scripts Written

All scripts are in [`scripts/`](./scripts/):

- **`localnet.sh`** — local network information gathering
- **`auth_parser.sh`** — parses authentication logs for relevant events
- **`disk_report.sh`** — disk usage and space reporting

## Labs Completed

- Manual privilege escalation enumeration on Metasploitable (`sudo -l`, SUID hunting, cron audit)
- SUID bit experiments on personal Kali VM
- GTFOBins exploitation chains applied to real findings, including using `nmap`'s interactive mode (a known SUID-exploitable binary) to escalate to root on Metasploitable
- `/etc/shadow` hash format analysis (yescrypt `$y$`)
- Conceptual preview of `linpeas` for automated enumeration

## Bandit Progress

OverTheWire Bandit levels solved: **through Level 20+**, each documented with its solution path.

## Sub-Documents

- [`permissions-cheatsheet.md`](./day2/permissions-cheatsheet.md) — permission bits, octal notation, SUID/SGID/sticky bit reference
- [`users-and-auth.md`](./users-and-auth.md) — user/group management, `/etc/passwd`/`/etc/shadow` structure, sudoers configuration
- [`logging-and-cron.md`](./logging-and-cron.md) — logging systems (`journald`/`rsyslog`) and cron job structure/security implications
- [`scripts/`](./scripts/) — all three bash scripts with individual usage notes

## Checkpoint

- [x] Bandit progress documented through Level 20+
- [x] 3 bash scripts on GitHub with READMEs
- [x] Permissions cheatsheet complete
- [x] Manual privilege escalation enumeration checklist internalized
- [x] Root escalation on Metasploitable via SUID `nmap` documented

## Next

Week 4 — Python for security tooling (port scanner, hash checker, log parser, banner grabber) and continued GitHub portfolio buildout.
