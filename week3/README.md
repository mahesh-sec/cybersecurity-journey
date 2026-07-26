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
All scripts are in [`day4/`](./day4/):
- **[`Localnet.sh`](./day4/Localnet.sh)** — local network information gathering
- **[`Auth parser.sh`](./day4/Auth%20parser.sh)** — parses authentication logs for relevant events
- **[`Disk report.sh`](./day4/Disk%20report.sh)** — disk usage and space reporting
## Labs Completed
- Manual privilege escalation enumeration on Metasploitable (`sudo -l`, SUID hunting, cron audit)
- SUID bit experiments on personal Kali VM
- GTFOBins exploitation chains applied to real findings, including using `nmap`'s interactive mode (a known SUID-exploitable binary) to escalate to root on Metasploitable
- `/etc/shadow` hash format analysis (yescrypt `$y$`)
- Conceptual preview of `linpeas` for automated enumeration
## Bandit Progress
OverTheWire Bandit levels solved: **through Level 10**, each documented with its solution path — see [`day1/Bandit solutions.md`](./day1/Bandit%20solutions.md), [`day2/Bandit solutions day2.md`](./day2/Bandit%20solutions%20day2.md), and [`day3/Bandit 8 10.md`](./day3/Bandit%208%2010.md).
## Sub-Documents
- [`day2/permissions-cheatsheet.md`](./day2/permissions-cheatsheet.md) — permission bits, octal notation, SUID/SGID/sticky bit reference
- [`day2/Suid findings.md`](./day2/Suid%20findings.md) — SUID binary hunting results
- [`day3/Users and auth.md`](./day3/Users%20and%20auth.md) — user/group management, `/etc/passwd`/`/etc/shadow` structure, sudoers configuration
- [`day3/Sudo privesc find.md`](./day3/Sudo%20privesc%20find.md) — sudoers misconfiguration enumeration
- [`day5/Logging and cron.md`](./day5/Logging%20and%20cron.md) — logging systems (`journald`/`rsyslog`) and cron job structure/security implications
- [`day5/Ssh log triage notes.md`](./day5/Ssh%20log%20triage%20notes.md) — SSH authentication log analysis
- [`day6/gtfobins-practice.md`](./day6/gtfobins-practice.md) — GTFOBins exploitation practice
- [`day6/sudo-misconfiguration.md`](./day6/sudo-misconfiguration.md) — sudoers misconfiguration deep dive
- [`day6/suid-deep-dive.md`](./day6/suid-deep-dive.md) — SUID binary deep dive with compiled C examples
## Checkpoint
- [x] Bandit progress documented through Level 10
- [x] 3 bash scripts on GitHub with READMEs
- [x] Permissions cheatsheet complete
- [x] Manual privilege escalation enumeration checklist internalized
- [x] Root escalation on Metasploitable via SUID `nmap` documented
## Next
Week 4 — Python for security tooling (port scanner, hash checker, log parser, banner grabber) and continued GitHub portfolio buildout.
